"""bvh_minimo.py — escreve um BVH pequeno e sintético (um aceno), feito do zero por este script.

Serve para ver o formato por dentro e para ter um clipe cuja licença é sua. Não é um humano capturado:
o esqueleto tem só tronco e braço direito, e o movimento é uma senoide.
Uso: python3 kit/bvh_minimo.py [--quadros 60] [--fps 30]   →   ~/fth/movimentos/aceno.bvh
"""
import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fth  # noqa: E402

ESQUELETO = """HIERARCHY
ROOT Hips
{
  OFFSET 0.0 0.0 0.0
  CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation
  JOINT Spine
  {
    OFFSET 0.0 25.0 0.0
    CHANNELS 3 Zrotation Xrotation Yrotation
    JOINT Head
    {
      OFFSET 0.0 30.0 0.0
      CHANNELS 3 Zrotation Xrotation Yrotation
      End Site
      {
        OFFSET 0.0 18.0 0.0
      }
    }
    JOINT RightArm
    {
      OFFSET -18.0 25.0 0.0
      CHANNELS 3 Zrotation Xrotation Yrotation
      JOINT RightForeArm
      {
        OFFSET -28.0 0.0 0.0
        CHANNELS 3 Zrotation Xrotation Yrotation
        End Site
        {
          OFFSET -25.0 0.0 0.0
        }
      }
    }
  }
}
MOTION
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quadros", type=int, default=60)
    ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()
    linhas = [f"Frames: {a.quadros}", f"Frame Time: {1 / a.fps:.6f}"]
    for f in range(a.quadros):
        t = f / a.fps
        ombro = -60.0 * min(1.0, t / 0.5)          # levanta o braço em 0,5 s
        cotovelo = 30.0 * math.sin(2 * math.pi * 1.5 * t)  # acena a 1,5 Hz
        v = [0.0, 95.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ombro, 0, 0, cotovelo, 0, 0]
        linhas.append(" ".join(f"{x:.3f}" for x in v))
    fth.MOV.mkdir(parents=True, exist_ok=True)
    p = fth.MOV / "aceno.bvh"
    p.write_text(ESQUELETO + "\n".join(linhas) + "\n", encoding="utf-8")
    print(f"gravado: {p} ({a.quadros} quadros a {a.fps} Hz)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
