F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro && . $F/.venv/bin/activate
python3 kit/comando_wbc.py --comandos kit/comandos-ruins.json; echo "saída: $?"
