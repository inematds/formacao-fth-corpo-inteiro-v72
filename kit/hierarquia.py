"""hierarquia.py — as três camadas de um humanoide de corpo inteiro, contadas num laço de simulação.

S2 (comando de alto nível, ~5 Hz) troca o alvo da mão direita; S1 (controle de corpo inteiro, 50 Hz)
transforma o alvo em ângulos de junta por IK; S0 (PD de junta + física, 500 Hz) é o passo do MuJoCo com
os atuadores de posição do G1 do Menagerie (kp=500). As pernas seguram a pose "stand" do modelo.
Uso: python3 kit/hierarquia.py [--segundos 2] [--s2-hz 5] [--s1-hz 50]
"""
import argparse
import sys
from pathlib import Path

import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fth  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--segundos", type=float, default=2.0)
    ap.add_argument("--s2-hz", type=float, default=5.0)
    ap.add_argument("--s1-hz", type=float, default=50.0)
    a = ap.parse_args()
    m = fth.carregar()
    d = mujoco.MjData(m)
    fth.em_pe(m, d)
    s0_hz = round(1 / m.opt.timestep)
    if s0_hz % a.s1_hz or s0_hz % a.s2_hz:
        print(f"ERRO: S1 ({a.s1_hz:g} Hz) e S2 ({a.s2_hz:g} Hz) precisam dividir o passo de {s0_hz} Hz.")
        return 1
    k1, k2 = int(s0_hz // a.s1_hz), int(s0_hz // a.s2_hz)
    braco = fth.juntas_por_prefixo(m, "right_shoulder") + fth.juntas_por_prefixo(m, "right_elbow") \
        + fth.juntas_por_prefixo(m, "right_wrist")
    mao = mujoco.mj_name2id(m, fth.B, "right_wrist_yaw_link")
    inicio = d.xpos[mao].copy()
    alvos = [inicio + np.array(v) for v in ([0.20, 0, 0.15], [0.25, 0.05, 0.30], [0.15, -0.05, 0.20])]
    aux = mujoco.MjData(m)
    n0 = n1 = n2 = 0
    alvo = inicio
    for i in range(int(round(a.segundos * s0_hz))):
        if i % k2 == 0:  # S2: decide "o quê" (aqui, um roteiro de alvos)
            alvo = alvos[n2 % len(alvos)]
            n2 += 1
        if i % k1 == 0:  # S1: decide "como" o corpo inteiro chega lá
            aux.qpos[:] = d.qpos
            fth.ik_mao(m, aux, "right_wrist_yaw_link", alvo, braco, passos=20)
            for j in braco:
                a_ = [k for k in range(m.nu) if m.actuator_trnid[k][0] == j][0]
                d.ctrl[a_] = aux.qpos[m.jnt_qposadr[j]]
            n1 += 1
        mujoco.mj_step(m, d)  # S0: PD de junta (atuador de posição) + física
        n0 += 1
    mujoco.mj_kinematics(m, d)
    erro = np.linalg.norm(d.xpos[mao] - alvo) * 100
    print(f"simulado: {a.segundos:g} s · passo de física {m.opt.timestep * 1000:g} ms")
    print(f"S2 comando de alto nível : {n2:4d} chamadas ({n2 / a.segundos:g} Hz)")
    print(f"S1 corpo inteiro (IK)    : {n1:4d} chamadas ({n1 / a.segundos:g} Hz)")
    print(f"S0 PD de junta + física  : {n0:4d} passos   ({n0 / a.segundos:g} Hz)")
    print(f"mão direita a {erro:.1f} cm do último alvo · pelve a {d.qpos[2]:.2f} m · de pé: {'não' if fth.caiu(d) else 'sim'}")
    print("3 camadas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
