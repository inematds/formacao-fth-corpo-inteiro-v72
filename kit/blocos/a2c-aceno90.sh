F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro && . $F/.venv/bin/activate
python3 kit/bvh_minimo.py --quadros 90 && python3 kit/ler_clipe.py $F/movimentos/aceno.bvh | grep quadros
