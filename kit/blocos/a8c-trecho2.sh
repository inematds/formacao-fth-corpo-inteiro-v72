F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro; B=$F/GMR/assets/xsens_bvh_test/251021_04_boxing_120Hz_cm_3DsMax.bvh
( . $F/.venv-gmr/bin/activate && python3 kit/retarget.py $B --inicio 1200 --fim 2400 --nome boxe_trecho2 | grep violações )
. $F/.venv/bin/activate && python3 kit/reproduzir.py $F/movimentos/boxe_trecho2.npz | grep "erro médio"
python3 kit/checar_seguranca.py $F/movimentos/boxe_trecho2.npz
python3 kit/conferir_pipeline.py | tail -2
