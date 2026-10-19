F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro && . $F/.venv/bin/activate
python3 kit/hierarquia.py --s1-hz 30; echo "saída: $?"
