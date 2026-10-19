F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro && . $F/.venv-gmr/bin/activate
python3 kit/retarget.py $F/GMR/assets/xsens_bvh_test/251021_04_boxing_120Hz_cm_3DsMax.bvh --fim 1200 --nome boxe_g1; echo "saída: $?"
