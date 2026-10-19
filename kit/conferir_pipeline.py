"""conferir_pipeline.py — confere a cadeia mocap → retargeting → rastreio → segurança de ponta a ponta.

Cada script do kit grava um resumo em ~/fth/movimentos/etapas/. Este script lê os quatro e confere que
cada etapa passou E que as etapas 2, 3 e 4 falam do MESMO arquivo de movimento (senão a cadeia está
quebrada: você conferiu um movimento e vai mandar outro).
Uso: python3 kit/conferir_pipeline.py [--erro-max-graus 2]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fth  # noqa: E402

ETAPAS = [("1-clipe", "mocap (BVH lido)"), ("2-retarget", "retargeting"),
          ("3-rastreio-portico", "rastreio no simulador"), ("4-seguranca", "checagem de segurança")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--erro-max-graus", type=float, default=2.0)
    a = ap.parse_args()
    pasta = fth.MOV / "etapas"
    e = {}
    for nome, _ in ETAPAS:
        p = pasta / f"{nome}.json"
        e[nome] = json.loads(p.read_text(encoding="utf-8")) if p.exists() else None
    teste = {
        "1-clipe": lambda x: (x["ok"], f"{x['quadros']} quadros a {x['fps']} Hz"),
        "2-retarget": lambda x: (x["violacoes"] == 0, f"{x['quadros']} quadros, {x['violacoes']} violações de limite"),
        "3-rastreio-portico": lambda x: (x["erro_medio_graus"] <= a.erro_max_graus and not x["queda"],
                                         f"erro médio {x['erro_medio_graus']}° (máx {a.erro_max_graus:g}°), queda: {'sim' if x['queda'] else 'não'}"),
        "4-seguranca": lambda x: (x["regras_ok"] == 4, f"{x['regras_ok']}/4 regras"),
    }
    ok = 0
    for nome, rotulo in ETAPAS:
        if e[nome] is None:
            print(f"FALHA · {rotulo}: não rodou (falta etapas/{nome}.json)")
            continue
        passou, txt = teste[nome](e[nome])
        print(f"{'ok   ' if passou else 'FALHA'} · {rotulo}: {txt}")
        ok += passou
    movs = {Path(e[n].get("arquivo") or e[n].get("movimento")).name for n in ("2-retarget", "3-rastreio-portico", "4-seguranca") if e[n]}
    if e["1-clipe"] and e["2-retarget"] and Path(e["1-clipe"]["arquivo"]).name != Path(e["2-retarget"].get("fonte", "")).name:
        print(f"FALHA · cadeia: o BVH lido ({Path(e['1-clipe']['arquivo']).name}) não é o que foi retargeted")
        ok = min(ok, 3)
    if len(movs) > 1:
        print(f"FALHA · cadeia: as etapas falam de arquivos diferentes ({', '.join(sorted(movs))})")
        ok = min(ok, 3)
    elif movs:
        print(f"cadeia: um só movimento ({movs.pop()})")
    print(f"{ok} etapas ok" if ok == 4 else f"{ok} de 4 etapas ok")
    return 0 if ok == 4 else 1


if __name__ == "__main__":
    sys.exit(main())
