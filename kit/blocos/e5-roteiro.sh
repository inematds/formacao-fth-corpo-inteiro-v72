F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro && . $F/.venv/bin/activate
sed 's/"esquerda"/"esquerdo"/' kit/passos.json > $F/movimentos/passos-erro.json
python3 kit/teleop_sim.py --roteiro $F/movimentos/passos-erro.json; echo "saída: $?"
