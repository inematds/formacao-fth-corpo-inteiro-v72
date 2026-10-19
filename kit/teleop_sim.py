"""teleop_sim.py — teleoperação de corpo inteiro simulada: alvos de mão chegam com atraso e o controle segue.

O "operador" é um roteiro JSON (kit/passos.json): deslocamentos do controle de cada mão, como num óculos de
VR. Cada alvo chega ao robô depois da latência; o controle de corpo inteiro (50 Hz) resolve a IK dos dois
braços e o PD de junta (500 Hz) executa, com as pernas na pose "stand". Um alvo conta como atingido se a
mão chega a menos de tolerancia_cm dele dentro da janela.
Uso: python3 kit/teleop_sim.py --roteiro kit/passos.json [--latencia-ms 80]
"""
import argparse
import json
import sys
from pathlib import Path

import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fth  # noqa: E402

LADO = {"direita": "right", "esquerda": "left"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roteiro", required=True)
    ap.add_argument("--latencia-ms", type=float, default=80)
    a = ap.parse_args()
    try:
        rot = json.loads(Path(a.roteiro).expanduser().read_text(encoding="utf-8"))
        alvos = rot["alvos"]
        tol = rot.get("tolerancia_cm", 3) / 100
        for x in alvos:
            if x["mao"] not in LADO:
                raise ValueError(f"mão '{x['mao']}' (use direita ou esquerda)")
    except (OSError, ValueError, KeyError) as e:
        print(f"ERRO no roteiro: {e}")
        return 1
    m = fth.carregar()
    d = mujoco.MjData(m)
    fth.em_pe(m, d)
    lat = a.latencia_ms / 1000
    braco, mao, inicio, alvo_atual = {}, {}, {}, {}
    for lado, en in LADO.items():
        braco[lado] = [j for p in ("shoulder", "elbow", "wrist") for j in fth.juntas_por_prefixo(m, f"{en}_{p}")]
        mao[lado] = mujoco.mj_name2id(m, fth.B, f"{en}_wrist_yaw_link")
        inicio[lado] = d.xpos[mao[lado]].copy()
        alvo_atual[lado] = inicio[lado].copy()
    pos = [inicio[x["mao"]] + np.array([x["dx"], x["dy"], x["dz"]]) for x in alvos]
    melhor = [np.inf] * len(alvos)
    quando = [None] * len(alvos)
    aux = mujoco.MjData(m)
    fim = max(x["t"] + x["janela"] for x in alvos) + 0.2
    k1 = int(round(0.02 / m.opt.timestep))  # controle de corpo inteiro a 50 Hz
    for i in range(int(fim / m.opt.timestep)):
        t = i * m.opt.timestep
        for n, x in enumerate(alvos):  # o alvo só existe para o robô depois da latência
            if x["t"] + lat <= t < x["t"] + lat + m.opt.timestep:
                alvo_atual[x["mao"]] = pos[n]
        if i % k1 == 0:
            aux.qpos[:] = d.qpos
            for lado in LADO:
                fth.ik_mao(m, aux, f"{LADO[lado]}_wrist_yaw_link", alvo_atual[lado], braco[lado], passos=20)
                for j in braco[lado]:
                    d.ctrl[[k for k in range(m.nu) if m.actuator_trnid[k][0] == j][0]] = aux.qpos[m.jnt_qposadr[j]]
        mujoco.mj_step(m, d)
        for n, x in enumerate(alvos):
            if x["t"] <= t <= x["t"] + x["janela"]:
                e = float(np.linalg.norm(d.xpos[mao[x["mao"]]] - pos[n]))
                melhor[n] = min(melhor[n], e)
                if e < tol and quando[n] is None:
                    quando[n] = t - x["t"]
    print(f"latência do operador ao robô: {a.latencia_ms:g} ms · tolerância: {tol * 100:g} cm · controle a 50 Hz")
    for n, x in enumerate(alvos):
        if quando[n] is not None:
            res = f"atingido em {quando[n] * 1000:.0f} ms"
        else:
            res = f"não atingido (chegou a {melhor[n] * 100:.1f} cm)"
        print(f"alvo {n + 1} · t={x['t']:.1f} s · mão {x['mao']:8s} · {res}")
    ok = sum(q is not None for q in quando)
    print(f"robô de pé: {'não' if fth.caiu(d) else 'sim'}")
    print(f"alvos atingidos: {ok}/{len(alvos)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
