F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro; B=$F/GMR/assets/xsens_bvh_test/251021_04_boxing_120Hz_cm_3DsMax.bvh
. $F/.venv/bin/activate && python3 kit/ler_clipe.py $B > /dev/null
( . $F/.venv-gmr/bin/activate && python3 kit/retarget.py $B --fim 1200 --nome boxe_g1 > /dev/null )
python3 kit/reproduzir.py $F/movimentos/boxe_g1.npz > /dev/null && python3 kit/checar_seguranca.py $F/movimentos/boxe_g1.npz | tail -1
( . $F/.venv-gmr/bin/activate && python3 kit/retarget.py $B --fim 600 --nome boxe_curto | grep violações )
python3 kit/reproduzir.py $F/movimentos/boxe_curto.npz | grep "erro médio"
python3 kit/conferir_pipeline.py; echo "saída: $?"
