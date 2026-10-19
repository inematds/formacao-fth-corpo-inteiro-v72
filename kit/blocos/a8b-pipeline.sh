F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro; B=$F/GMR/assets/xsens_bvh_test/251021_04_boxing_120Hz_cm_3DsMax.bvh
. $F/.venv/bin/activate && python3 kit/ler_clipe.py $B | tail -1
( . $F/.venv-gmr/bin/activate && python3 kit/retarget.py $B --fim 1200 --nome boxe_g1 | grep violações )
python3 kit/reproduzir.py $F/movimentos/boxe_g1.npz | grep "erro médio"
python3 kit/checar_seguranca.py $F/movimentos/boxe_g1.npz | tail -1
python3 kit/conferir_pipeline.py; echo "saída: $?"
