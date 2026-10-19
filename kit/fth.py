"""fth.py — funções comuns do kit do curso FTH 3 (Corpo inteiro: imitar, teleoperar e obedecer).

Mesma bancada do curso 0: acha o MuJoCo Menagerie em $FTH/mujoco_menagerie (padrão: a pasta acima do
repositório do curso, ou seja ~/fth) e grava o que cada etapa produz em $FTH/movimentos/.
Testado com mujoco 3.16.0 + numpy 2.5.4, Menagerie 62ab00f (15/10/2026), em 19/10/2026.
"""
import json
import os
import sys
from pathlib import Path

import mujoco
import numpy as np

KIT = Path(__file__).resolve().parent
RAIZ = Path(os.environ.get("FTH", KIT.parents[1]))
MENAGERIE = RAIZ / "mujoco_menagerie"
MOV = RAIZ / "movimentos"
G1 = "unitree_g1/scene.xml"
J = mujoco.mjtObj.mjOBJ_JOINT
B = mujoco.mjtObj.mjOBJ_BODY
A = mujoco.mjtObj.mjOBJ_ACTUATOR


def caminho(p):
    q = Path(p).expanduser()
    if q.exists():
        return q
    r = MENAGERIE / p
    if r.exists():
        return r
    sys.exit(f"ERRO: não achei {p} (nem em {MENAGERIE}). Monte a bancada da aula 1.")


def carregar(p=G1):
    return mujoco.MjModel.from_xml_path(str(caminho(p)))


def nome(m, tipo, i):
    return mujoco.mj_id2name(m, tipo, i) or f"#{i}"


def articuladas(m):
    """Índices das juntas de 1 grau (hinge), sem a base flutuante."""
    return [j for j in range(m.njnt) if int(m.jnt_type[j]) == int(mujoco.mjtJoint.mjJNT_HINGE)]


def em_pe(m, d):
    """Pose 'stand' do Menagerie (keyframe 0), com o ctrl copiado do keyframe."""
    mujoco.mj_resetDataKeyframe(m, d, 0)
    mujoco.mj_forward(m, d)


def portico(d, base_qpos):
    """Pórtico virtual: segura a base (pelve) numa pose dada, como o robô suspenso no 1º teste."""
    d.qpos[:7] = base_qpos
    d.qvel[:6] = 0.0


def caiu(d, altura_min=0.5):
    return float(d.qpos[2]) < altura_min


def gravar_etapa(nome_etapa, dados):
    """Cada script grava um resumo em ~/fth/movimentos/etapas/<etapa>.json (a aula 8 confere a cadeia)."""
    p = MOV / "etapas"
    p.mkdir(parents=True, exist_ok=True)
    (p / f"{nome_etapa}.json").write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return p / f"{nome_etapa}.json"


def ik_mao(m, d, corpo, alvo, juntas, passos=200, amort=0.05, tol=0.01):
    """IK de posição por mínimos quadrados amortecidos (Jacobiano do MuJoCo) só nas juntas dadas.
    Mexe em d.qpos dessas juntas (respeitando jnt_range) e devolve o erro final em metros."""
    bid = mujoco.mj_name2id(m, B, corpo)
    cols = [int(m.jnt_dofadr[j]) for j in juntas]
    adr = [int(m.jnt_qposadr[j]) for j in juntas]
    jacp = np.zeros((3, m.nv))
    erro = np.inf
    for _ in range(passos):
        mujoco.mj_kinematics(m, d)
        mujoco.mj_comPos(m, d)
        e = np.asarray(alvo) - d.xpos[bid]
        erro = float(np.linalg.norm(e))
        if erro < tol:
            break
        mujoco.mj_jacBody(m, d, jacp, None, bid)
        Jm = jacp[:, cols]
        dq = Jm.T @ np.linalg.solve(Jm @ Jm.T + amort**2 * np.eye(3), e)
        for k, j in enumerate(juntas):
            lo, hi = m.jnt_range[j]
            d.qpos[adr[k]] = float(np.clip(d.qpos[adr[k]] + dq[k], lo, hi))
    return erro


def juntas_por_prefixo(m, prefixo):
    return [j for j in articuladas(m) if nome(m, J, j).startswith(prefixo)]


def ctrl_da_pose(m, d):
    """Para atuadores de posição (o G1 do Menagerie): ctrl = qpos da junta de cada motor."""
    for a in range(m.nu):
        j = m.actuator_trnid[a][0]
        d.ctrl[a] = d.qpos[m.jnt_qposadr[j]]
