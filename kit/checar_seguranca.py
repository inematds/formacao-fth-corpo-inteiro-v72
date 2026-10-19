"""checar_seguranca.py — confere um movimento retargeted ANTES de ele ir para uma política ou um robô.

Quatro regras, todas lidas do próprio movimento no G1 do Menagerie:
  1) limites de junta (folga 0,5°)            3) pés não atravessam o chão (até 1 cm abaixo da pose de pé)
  2) velocidade de junta abaixo do teto        4) pelve dentro da área de trabalho (raio em metros)
O teto de velocidade e o raio são SEUS (regra do laboratório): a pesquisa da formação não traz a velocidade
máxima por junta do G1, então o padrão é conservador. Ajuste com --teto-graus-s e --raio-m.
Uso: python3 kit/checar_seguranca.py <movimento.npz> [--teto-graus-s 400] [--raio-m 1.5]
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
    ap.add_argument("movimento")
    ap.add_argument("--teto-graus-s", type=float, default=400)
    ap.add_argument("--raio-m", type=float, default=1.5)
    a = ap.parse_args()
    p = Path(a.movimento).expanduser()
    if not p.exists():
        print(f"ERRO: não achei {a.movimento}. Rode o retarget da aula 3 antes.")
        return 1
    z = np.load(p)
    qref, fps = z["qpos"], float(z["fps"])
    m = fth.carregar()
    d = mujoco.MjData(m)
    juntas = fth.articuladas(m)
    q = qref[:, 7:]
    lo = np.array([m.jnt_range[j][0] for j in juntas]) - np.deg2rad(0.5)
    hi = np.array([m.jnt_range[j][1] for j in juntas]) + np.deg2rad(0.5)
    n_lim = int(((q < lo) | (q > hi)).sum())
    vel = np.rad2deg(np.abs(np.diff(q, axis=0)) * fps)
    kv = int(np.argmax(vel.max(axis=0)))
    vmax = float(vel.max())
    pes = [mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_SITE, s) for s in ("left_foot", "right_foot")]
    fth.em_pe(m, d)
    z_apoio = min(float(d.site_xpos[s][2]) for s in pes)  # o site do pé fica no tornozelo, acima da sola
    zmin = np.inf
    for qp in qref:
        d.qpos[:] = qp
        mujoco.mj_kinematics(m, d)
        zmin = min(zmin, min(float(d.site_xpos[s][2]) for s in pes))
    raio = float(np.max(np.linalg.norm(qref[:, :2] - qref[0, :2], axis=1)))
    regras = [
        ("limites de junta", n_lim == 0, f"{n_lim} quadro×junta fora"),
        ("velocidade de junta", vmax <= a.teto_graus_s, f"máx {vmax:.0f}°/s em {fth.nome(m, fth.J, juntas[kv])} (teto {a.teto_graus_s:g}°/s)"),
        ("pés acima do chão", zmin >= z_apoio - 0.01, f"site do pé desce até {zmin * 100:.1f} cm (de pé: {z_apoio * 100:.1f} cm)"),
        ("área de trabalho", raio <= a.raio_m, f"pelve se afasta até {raio:.2f} m (raio {a.raio_m:g} m)"),
    ]
    for nome, ok, txt in regras:
        print(f"{'ok   ' if ok else 'FALHA'} · {nome}: {txt}")
    passou = sum(ok for _, ok, _ in regras)
    print(f"segurança: {passou}/4 regras")
    fth.gravar_etapa("4-seguranca", {"movimento": str(p), "regras_ok": passou,
                                     "teto_graus_s": a.teto_graus_s, "raio_m": a.raio_m})
    return 0 if passou == 4 else 1


if __name__ == "__main__":
    sys.exit(main())
