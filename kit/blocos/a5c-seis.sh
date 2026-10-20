F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro && . $F/.venv/bin/activate
sed 's/"dx": 0.60/"dx": 0.25/' kit/passos.json > $F/movimentos/passos-meu.json
python3 kit/teleop_sim.py --roteiro $F/movimentos/passos-meu.json | tail -1
