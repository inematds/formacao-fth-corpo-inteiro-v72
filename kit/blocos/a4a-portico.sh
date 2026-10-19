F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro && . $F/.venv/bin/activate
python3 kit/reproduzir.py $F/movimentos/boxe_g1.npz; echo "saída: $?"
