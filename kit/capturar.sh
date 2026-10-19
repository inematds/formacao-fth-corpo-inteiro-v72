#!/usr/bin/env bash
# capturar.sh — roda cada bloco "Terminal" do curso (kit/blocos/*.sh) e grava a saída em kit/saidas/.
# É daqui que saem as abas "Saída capturada" das aulas.
# Uso: FTH=<pasta de ensaio> bash kit/capturar.sh [bloco...]
#   A pasta de ensaio faz o papel de ~/fth: recebe .venv, mujoco_menagerie, GMR, .venv-gmr e o link "corpo-inteiro" para este repo.
#   O caminho da pasta de ensaio é trocado por ~/fth nas saídas, para a aba mostrar o que o aluno vê.
set -uo pipefail
K=$(cd "$(dirname "$0")" && pwd)
: "${FTH:?defina FTH=<pasta de ensaio>}"
mkdir -p "$FTH" "$K/saidas"
[ -e "$FTH/corpo-inteiro" ] || ln -s "$(dirname "$K")" "$FTH/corpo-inteiro"
alvos=("$@"); [ ${#alvos[@]} -eq 0 ] && alvos=($(cd "$K/blocos" && ls *.sh | sed 's/\.sh$//'))
for b in "${alvos[@]}"; do
  ( cd /tmp && FTH="$FTH" bash "$K/blocos/$b.sh" ) 2>&1 | sed "s#$FTH#~/fth#g" > "$K/saidas/$b.txt"
  echo "$b: $(wc -l < "$K/saidas/$b.txt") linhas"
done
