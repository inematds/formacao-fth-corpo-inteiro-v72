F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro && . $F/.venv/bin/activate
head -n -249 $F/GMR/assets/xsens_bvh_test/251021_04_boxing_120Hz_cm_3DsMax.bvh > $F/movimentos/cortado.bvh
python3 kit/ler_clipe.py $F/movimentos/cortado.bvh; echo "saída: $?"
