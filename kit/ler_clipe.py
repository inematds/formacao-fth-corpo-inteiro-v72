"""ler_clipe.py — lê o cabeçalho e o movimento de um arquivo BVH (captura de movimento) sem biblioteca extra.

BVH = HIERARCHY (esqueleto: juntas, OFFSET de cada osso, canais de rotação/posição) + MOTION (um quadro
por linha, um número por canal). Este script conta juntas, canais, quadros e fps, e confere que toda
linha de movimento tem o número certo de valores.
Uso: python3 kit/ler_clipe.py <arquivo.bvh>
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fth  # noqa: E402


def ler(p):
    linhas = Path(p).read_text(encoding="utf-8", errors="replace").splitlines()
    if not linhas or linhas[0].strip() != "HIERARCHY":
        raise ValueError("a 1ª linha não é HIERARCHY")
    juntas, pontas, canais, ordem, offsets = [], 0, 0, None, []
    i = 0
    while i < len(linhas) and linhas[i].strip() != "MOTION":
        t = linhas[i].split()
        if t and t[0] in ("ROOT", "JOINT"):
            juntas.append(t[1])
        elif t and t[0] == "End":
            pontas += 1
        elif t and t[0] == "CHANNELS":
            canais += int(t[1])
            if int(t[1]) == 3 and ordem is None:
                ordem = " ".join(t[2:])
        elif t and t[0] == "OFFSET":
            offsets.append(max(abs(float(x)) for x in t[1:4]))
        i += 1
    if i >= len(linhas):
        raise ValueError("não achei a seção MOTION")
    quadros = int(re.search(r"Frames:\s*(\d+)", linhas[i + 1]).group(1))
    dt = float(re.search(r"Frame Time:\s*([\d.eE+-]+)", linhas[i + 2]).group(1))
    dados = [ln for ln in linhas[i + 3:] if ln.strip()]
    certas = sum(1 for ln in dados if len(ln.split()) == canais)
    return dict(raiz=juntas[0], juntas=len(juntas), pontas=pontas, canais=canais, ordem=ordem,
                quadros=quadros, linhas=len(dados), certas=certas, fps=1 / dt, maior=max(offsets))


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    p = Path(sys.argv[1]).expanduser()
    if not p.exists():
        print(f"ERRO: arquivo não encontrado: {sys.argv[1]}")
        return 1
    try:
        c = ler(p)
    except (ValueError, AttributeError, IndexError) as e:
        print(f"ERRO: {p.name} não parece um BVH ({e})")
        return 1
    unidade = "cm" if c["maior"] > 3 else "m"
    print(f"arquivo: {p.name}")
    print(f"raiz: {c['raiz']} · juntas: {c['juntas']} · pontas (End Site): {c['pontas']} · canais por quadro: {c['canais']}")
    print(f"ordem de rotação: {c['ordem']} · unidade provável: {unidade} (maior OFFSET {c['maior']:.1f})")
    print(f"quadros: {c['quadros']} · fps: {c['fps']:.0f} · duração: {c['quadros'] / c['fps']:.1f} s")
    ok = c["linhas"] == c["quadros"] == c["certas"]
    print(f"linhas de movimento conferidas: {c['certas']}/{c['quadros']}")
    fth.gravar_etapa("1-clipe", {"arquivo": str(p), "quadros": c["quadros"], "fps": round(c["fps"]),
                                 "juntas": c["juntas"], "ok": ok})
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
