"""mao.py — a mão do G1 (Dex3-1 no modelo do Menagerie): graus de liberdade, limites e um aperto simulado.

1) Conta as juntas de cada mão em unitree_g1/scene_with_hands.xml e mostra os limites e o torque declarado.
2) Põe um cilindro fixo (raio 2 cm) entre o polegar e os dedos da mão direita, fecha a mão pelo PD dos
   atuadores e lê a força normal de contato de cada dedo. É uma estimativa do MODELO (kp=500, torque
   limitado pelo actuatorfrcrange), não uma medida do robô: a Unitree não publica força de preensão na
   página do G1 lida em 19/10/2026.
Uso: python3 kit/mao.py [--modelo unitree_g1/scene_with_hands.xml] [--so-contar]
"""
import argparse
import sys
from pathlib import Path

import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fth  # noqa: E402

FECHAR = {"right_hand_index_0_joint": 1.57, "right_hand_index_1_joint": 1.75,
          "right_hand_middle_0_joint": 1.57, "right_hand_middle_1_joint": 1.75,
          "right_hand_thumb_0_joint": 0.0, "right_hand_thumb_1_joint": -1.05, "right_hand_thumb_2_joint": -1.75}
DEDOS = ("thumb", "index", "middle")
NOME = {"thumb": "polegar", "index": "indicador", "middle": "médio"}


def contar(m):
    maos = {}
    for j in fth.articuladas(m):
        n = fth.nome(m, fth.J, j)
        if "_hand_" in n:
            maos.setdefault(n.split("_hand_")[0], []).append(j)
    return maos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", default="unitree_g1/scene_with_hands.xml")
    ap.add_argument("--so-contar", action="store_true")
    a = ap.parse_args()
    m = fth.carregar(a.modelo)
    maos = contar(m)
    print(f"modelo: {a.modelo} · nu={m.nu}")
    if not maos:
        if m.nq > len(fth.articuladas(m)):  # tem base livre: é o robô inteiro, mas sem mãos
            print("ERRO: este modelo não tem juntas de mão. No G1, use unitree_g1/scene_with_hands.xml.")
            return 1
        # mão avulsa (leap_hand, shadow_hand...): conta as juntas articuladas
        print(f"mão avulsa: {len(fth.articuladas(m))} GDL · {m.nu} atuadores")
        return 0
    for lado, js in maos.items():
        por = {dd: sum(dd in fth.nome(m, fth.J, j) for j in js) for dd in DEDOS}
        print(f"mão {lado}: {len(js)} GDL ({', '.join(f'{NOME[k]} {v}' for k, v in por.items())})")
    tmax = [m.jnt_actfrcrange[j][1] for j in maos["right"]]
    print(f"torque declarado por junta da mão: {min(tmax):.2f} a {max(tmax):.2f} N·m (actuatorfrcrange)")
    if a.so_contar:
        return 0

    sp = mujoco.MjSpec.from_file(str(fth.caminho(a.modelo)))
    g = sp.worldbody.add_geom()
    g.name, g.type = "objeto", mujoco.mjtGeom.mjGEOM_CYLINDER
    g.size, g.pos, g.quat = [0.02, 0.03, 0], [0.0, -0.232, 0.57], [0.7071068, 0, 0.7071068, 0]
    m = sp.compile()
    d = mujoco.MjData(m)
    fth.em_pe(m, d)
    base = d.qpos[:7].copy()
    obj = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_GEOM, "objeto")
    mot = {fth.nome(m, fth.A, k): k for k in range(m.nu)}
    for i in range(1000):  # 2 s: fecha em 0,5 s e segura
        fth.portico(d, base)
        s = min(1.0, i / 250)
        for n, alvo in FECHAR.items():
            d.ctrl[mot[n]] = s * alvo
        mujoco.mj_step(m, d)
    forca = {dd: 0.0 for dd in DEDOS}
    f6 = np.zeros(6)
    for k in range(d.ncon):
        c = d.contact[k]
        if obj in (c.geom1, c.geom2):
            outro = c.geom2 if c.geom1 == obj else c.geom1
            corpo = fth.nome(m, fth.B, m.geom_bodyid[outro])
            mujoco.mj_contactForce(m, d, k, f6)
            for dd in DEDOS:
                if f"right_hand_{dd}" in corpo:
                    forca[dd] += abs(f6[0])
    print("aperto simulado num cilindro fixo de 4 cm (mão direita, 2 s):")
    for dd in DEDOS:
        print(f"  {NOME[dd]:9s}: {forca[dd]:5.1f} N")
    tocando = sum(v > 0.5 for v in forca.values())
    print(f"dedos tocando o objeto: {tocando}/3 · estimativa do modelo, não medida no robô")
    return 0


if __name__ == "__main__":
    sys.exit(main())
