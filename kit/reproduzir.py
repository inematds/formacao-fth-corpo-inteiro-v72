"""reproduzir.py — tenta seguir um movimento retargeted no G1 do MuJoCo só com o PD das juntas.

Modos:
  --modo portico (padrão): a pelve segue a referência presa a um pórtico virtual; as juntas seguem a
                           referência pelo PD do atuador de posição (kp=500 do Menagerie). Mede o erro.
  --modo livre           : mesma coisa sem o pórtico. Mostra por que seguir ângulos não basta: sem uma
                           política que cuide do equilíbrio (BeyondMimic, GMT, SONIC), o robô cai.
Uso: python3 kit/reproduzir.py <movimento.npz> [--modo portico|livre]
"""
import argparse
import sys
from pathlib import Path

import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fth  # noqa: E402


def referencia(qref, fps, t):
    """Interpola a referência no instante t (juntas e posição linear; quatérnio por nlerp)."""
    x = min(t * fps, len(qref) - 1.000001)
    i = int(x)
    w = x - i
    q = (1 - w) * qref[i] + w * qref[i + 1]
    q[3:7] /= np.linalg.norm(q[3:7])
    return q


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("movimento")
    ap.add_argument("--modo", choices=["portico", "livre"], default="portico")
    a = ap.parse_args()
    p = Path(a.movimento).expanduser()
    if not p.exists():
        print(f"ERRO: não achei {a.movimento}. Rode o retarget da aula 3 antes.")
        return 1
    z = np.load(p)
    qref, fps = z["qpos"], float(z["fps"])
    m = fth.carregar()
    if qref.shape[1] != m.nq:
        print(f"ERRO: o movimento tem {qref.shape[1]} valores por quadro e o modelo pede nq={m.nq}.")
        return 1
    d = mujoco.MjData(m)
    d.qpos[:] = qref[0]
    mujoco.mj_forward(m, d)
    juntas = fth.articuladas(m)
    adr = np.array([m.jnt_qposadr[j] for j in juntas])
    mot = [[k for k in range(m.nu) if m.actuator_trnid[k][0] == j][0] for j in juntas]
    dur = (len(qref) - 1) / fps
    n = int(dur / m.opt.timestep)
    erros, queda = [], None
    for i in range(n):
        t = i * m.opt.timestep
        r = referencia(qref, fps, t)
        if a.modo == "portico":
            fth.portico(d, r[:7])
        d.ctrl[mot] = r[adr]
        mujoco.mj_step(m, d)
        erros.append(np.abs(d.qpos[adr] - referencia(qref, fps, t + m.opt.timestep)[adr]))
        if queda is None and fth.caiu(d):
            queda = t
            if a.modo == "livre":
                break
    e = np.rad2deg(np.array(erros))
    pior = int(np.argmax(e.mean(axis=0)))
    print(f"movimento: {p.name} · {len(qref)} quadros a {fps:g} Hz · {dur:.1f} s · modo {a.modo}")
    print(f"passos de física: {len(erros)} ({m.opt.timestep * 1000:g} ms cada)")
    print(f"erro médio de junta: {e.mean():.1f}° · pior junta: {fth.nome(m, fth.J, juntas[pior])} ({e.mean(axis=0)[pior]:.1f}°)")
    print(f"queda: {'não' if queda is None else f'sim, em t = {queda:.2f} s'}")
    fth.gravar_etapa("3-rastreio-" + a.modo, {"movimento": str(p), "erro_medio_graus": round(float(e.mean()), 1),
                                              "queda": queda is not None})
    return 0


if __name__ == "__main__":
    sys.exit(main())
