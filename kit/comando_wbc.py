"""comando_wbc.py — comandos de alto nível (o que um VLA mandaria) executados por um controle de corpo inteiro.

A camada de cima diz O QUÊ ("alcançar com a mão direita este ponto", "girar o tronco 20°"); este script faz
o papel da camada de baixo, desacoplada como no GR00T WBC: as pernas seguram a pose "stand" (aqui por PD;
no robô real seria uma política de RL) e os braços vão por IK. Antes de mexer, ele CONFERE o comando
(ação conhecida, junta dentro do limite, alvo ao alcance) e recusa o que não dá para fazer.
Uso: python3 kit/comando_wbc.py [--comandos kit/comandos.json]
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
ACOES = ("alcancar", "girar_tronco", "voltar")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comandos", default=str(Path(__file__).resolve().parent / "comandos.json"))
    a = ap.parse_args()
    try:
        cmds = json.loads(Path(a.comandos).expanduser().read_text(encoding="utf-8"))["comandos"]
    except (OSError, ValueError, KeyError) as e:
        print(f"ERRO no arquivo de comandos: {e}")
        return 1
    m = fth.carregar()
    d = mujoco.MjData(m)
    fth.em_pe(m, d)
    base = d.qpos[:7].copy()
    pose_pe = d.qpos.copy()
    qdes = d.qpos.copy()
    cintura = mujoco.mj_name2id(m, fth.J, "waist_yaw_joint")
    aux = mujoco.MjData(m)
    motor = {int(m.actuator_trnid[k][0]): k for k in range(m.nu)}
    recusados = 0
    for n, c in enumerate(cmds, 1):
        acao = c.get("acao")
        desc = f"comando {n} · {acao}"
        if acao not in ACOES:
            print(f"{desc} → recusado: ação desconhecida (conheço {', '.join(ACOES)})")
            recusados += 1
            continue
        novo = qdes.copy()
        alvo = mao = None
        if acao == "voltar":
            novo[:] = pose_pe
        elif acao == "girar_tronco":
            g = np.deg2rad(c["graus"])
            lo, hi = m.jnt_range[cintura]
            if not lo <= g <= hi:
                print(f"{desc} {c['graus']}° → recusado: fora do limite da cintura ({np.rad2deg(lo):.0f}° a {np.rad2deg(hi):.0f}°)")
                recusados += 1
                continue
            novo[m.jnt_qposadr[cintura]] = g
            desc += f" {c['graus']}°"
        else:  # alcancar
            lado = LADO.get(c.get("mao"))
            if lado is None:
                print(f"{desc} → recusado: mão '{c.get('mao')}' (use direita ou esquerda)")
                recusados += 1
                continue
            mao = f"{lado}_wrist_yaw_link"
            alvo = base[:3] + np.array(c["alvo_m"])
            desc += f" {c['mao']} {tuple(c['alvo_m'])}"
            corpo = {p: d.xpos[mujoco.mj_name2id(m, fth.B, f"{lado}_{p}_link")] for p in ("shoulder_pitch", "elbow", "wrist_yaw")}
            alcance = np.linalg.norm(corpo["elbow"] - corpo["shoulder_pitch"]) + np.linalg.norm(corpo["wrist_yaw"] - corpo["elbow"])
            dist = np.linalg.norm(alvo - corpo["shoulder_pitch"])
            if dist > alcance:
                print(f"{desc} → recusado: alvo a {dist:.2f} m do ombro; o braço alcança {alcance:.2f} m")
                recusados += 1
                continue
            juntas = [j for p in ("shoulder", "elbow", "wrist") for j in fth.juntas_por_prefixo(m, f"{lado}_{p}")]
            aux.qpos[:] = novo
            erro = fth.ik_mao(m, aux, mao, alvo, juntas, passos=300)
            if erro > 0.02:
                print(f"{desc} → recusado: a IK não chega ao alvo (fica a {erro * 100:.0f} cm) dentro dos limites de junta")
                recusados += 1
                continue
            novo[:] = aux.qpos
        # executa: rampa de 0,5 s até a nova pose; depois, 0,5 s de correção em malha fechada a 50 Hz
        # (a IK é refeita a partir do estado medido, como faz um controle de corpo inteiro)
        for i in range(500):
            s = min(1.0, i / 250)
            q = qdes + (novo - qdes) * s
            if alvo is not None and i >= 250 and i % 10 == 0:
                aux.qpos[:] = d.qpos
                fth.ik_mao(m, aux, mao, alvo, juntas, passos=20)
                for j in juntas:
                    novo[m.jnt_qposadr[j]] = aux.qpos[m.jnt_qposadr[j]]
                q = novo
            for j, k in motor.items():
                d.ctrl[k] = q[m.jnt_qposadr[j]]
            mujoco.mj_step(m, d)
        qdes = novo
        if fth.caiu(d):
            print(f"{desc} → executado: não (o robô caiu)")
            recusados += 1
            break
        if alvo is not None:
            mujoco.mj_kinematics(m, d)
            e = np.linalg.norm(d.xpos[mujoco.mj_name2id(m, fth.B, mao)] - alvo) * 100
            print(f"{desc} → executado: sim (mão a {e:.1f} cm do alvo)")
        else:
            print(f"{desc} → executado: sim")
    print(f"robô de pé: {'não' if fth.caiu(d) else 'sim'} · pelve a {d.qpos[2]:.2f} m")
    print(f"executado: {'sim' if recusados == 0 else f'não · {recusados} comando(s) recusado(s)'}")
    fth.gravar_etapa("comando-wbc", {"comandos": len(cmds), "recusados": recusados})
    return 0 if recusados == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
