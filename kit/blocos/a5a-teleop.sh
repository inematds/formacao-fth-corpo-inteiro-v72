F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro && . $F/.venv/bin/activate
python3 kit/teleop_sim.py --roteiro kit/passos.json; echo "saída: $?"
