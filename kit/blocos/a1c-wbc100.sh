F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro && . $F/.venv/bin/activate
python3 kit/hierarquia.py --wbc-hz 100 | grep S0
