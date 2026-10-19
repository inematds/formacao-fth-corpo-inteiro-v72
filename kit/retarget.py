"""retarget.py — leva um clipe BVH de captura de movimento para o Unitree G1 com o GMR, sem janela.

Roda no ambiente do GMR (~/fth/.venv-gmr), não no .venv do MuJoCo: um ambiente por ferramenta.
Lê o BVH no formato Xsens "3DSM" como o scripts/xsens_bvh_to_robot.py do GMR faz, mas sem a interface
Qt (o editor de offsets só é usado quando existe um offsets.json; sem ele os offsets são zero).
Grava ~/fth/movimentos/<nome>.npz com qpos (N × 36, quatérnio wxyz como o MuJoCo usa) e confere cada
quadro contra os limites de junta do G1 do Menagerie.

Uso: python kit/retarget.py <clipe.bvh> [--inicio 0] [--fim 1200] [--nome boxe_g1]
Testado com GMR bb1bbe4 (02/04/2026), mink 1.3.0, mujoco 3.16.0, torch 2.14.1+cpu, 19/10/2026.
"""
import argparse
import contextlib
import io
import sys
import time
import warnings
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fth  # noqa: E402

FOLGA_GRAUS = 0.5  # o IK do mink respeita os limites com tolerância numérica: contamos violação acima disso


def carregar_bvh(arquivo, inicio, fim):
    """Mesmo resultado de general_motion_retargeting.utils.xsens.load_xsens_file, sem PyQt6."""
    from general_motion_retargeting.utils.xsens_vendor.BVHParser import BVHParser
    import general_motion_retargeting.utils.lafan_vendor.utils as utils

    parser = BVHParser(axis_order="zxy", scale=0.01)
    rot, _ = parser.parse(Path(arquivo).read_text(), start=inicio, end=fim, reset_to_zero=False)
    quats, pos, _, parents = parser._MOTION_data_post_processing(rot, np.copy(parser.positions), reset_to_zero=True)
    glob = utils.quat_fk(quats, pos, parents)
    quadros = []
    for f in range(pos.shape[0]):
        r = {b: (glob[1][f, i], glob[0][f, i]) for i, b in enumerate(parser.names)}
        r["LeftFootMod"] = (np.array(r["LeftAnkle"][0]), r["LeftAnkle"][1])
        r["RightFootMod"] = (np.array(r["RightAnkle"][0]), r["RightAnkle"][1])
        quadros.append(r)
    # altura como no GMR (que usa o dedo esquerdo duas vezes no min)
    altura = r["Head_end_site"][0][2] - min(r["LeftToe_end_site"][0][2], r["LeftToe_end_site"][0][2])
    return quadros, float(altura), parser.frame_time, len(parser.names)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bvh")
    ap.add_argument("--inicio", type=int, default=0)
    ap.add_argument("--fim", type=int, default=None)
    ap.add_argument("--nome", default=None)
    a = ap.parse_args()
    if not Path(a.bvh).expanduser().exists():
        sys.exit(f"ERRO: clipe não encontrado: {a.bvh}")
    warnings.filterwarnings("ignore")  # aviso de depreciação do torch.jit, sem efeito aqui
    try:
        with contextlib.redirect_stdout(io.StringIO()):  # o GMR imprime tabelas e avisos ao importar
            from general_motion_retargeting import GeneralMotionRetargeting as GMR
    except ModuleNotFoundError as e:
        print(f"ERRO: o GMR não está neste ambiente ({e}). Ative ~/fth/.venv-gmr (aula 3).")
        return 2

    with contextlib.redirect_stdout(io.StringIO()):
        quadros, altura, dt, njuntas = carregar_bvh(Path(a.bvh).expanduser(), a.inicio, a.fim)
        gmr = GMR(src_human="bvh_xsens", tgt_robot="unitree_g1", actual_human_height=altura)
    fps = round(1 / dt)
    print(f"clipe: {Path(a.bvh).name} · {len(quadros)} quadros a {fps} Hz ({len(quadros) / fps:.1f} s) · {njuntas} pontos do esqueleto")
    print(f"altura do humano no clipe: {altura:.2f} m · robô: unitree_g1 (GMR, config bvh_xsens_to_g1.json)")
    t0 = time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        qpos = np.array([gmr.retarget(q) for q in quadros])
    seg = time.time() - t0

    m = fth.carregar(fth.G1)
    juntas = fth.articuladas(m)
    lo = np.array([m.jnt_range[j][0] for j in juntas])
    hi = np.array([m.jnt_range[j][1] for j in juntas])
    q = qpos[:, 7:]
    folga = np.deg2rad(FOLGA_GRAUS)
    fora = (q < lo - folga) | (q > hi + folga)
    margem = np.minimum(q - lo, hi - q).min(axis=0)
    k = int(np.argmin(margem))
    print(f"qpos: {qpos.shape[0]} × {qpos.shape[1]} (base 7 + {q.shape[1]} juntas, mesma ordem do Menagerie)")
    print(f"menor margem até o limite: {fth.nome(m, fth.J, juntas[k])} ({max(0.0, np.rad2deg(margem[k])):.1f}°, 0 = encostado)")
    print(f"violações de limite (Menagerie, folga {FOLGA_GRAUS}°): {int(fora.sum())}")
    if seg < 60:
        print("tempo de retargeting: menos de 1 min em CPU")

    nome = a.nome or Path(a.bvh).stem
    fth.MOV.mkdir(parents=True, exist_ok=True)
    saida = fth.MOV / f"{nome}.npz"
    np.savez(saida, qpos=qpos, fps=fps, fonte=str(Path(a.bvh).name))
    fth.gravar_etapa("2-retarget", {"arquivo": str(saida), "fonte": str(Path(a.bvh).expanduser()), "quadros": int(qpos.shape[0]), "fps": fps,
                                    "violacoes": int(fora.sum()), "folga_graus": FOLGA_GRAUS})
    print(f"gravado: {saida}")
    return 0 if not fora.any() else 1


if __name__ == "__main__":
    sys.exit(main())
