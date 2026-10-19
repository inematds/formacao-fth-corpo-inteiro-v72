F=${FTH:-$HOME/fth}; cd $F
[ -d GMR ] || git clone -q --filter=blob:none --sparse https://github.com/YanjieZe/GMR
cd GMR && git sparse-checkout set assets/xsens_bvh_test
git checkout -q bb1bbe4 && git log -1 --format='GMR %h (%ad)' --date=short
cd $F/corpo-inteiro && . $F/.venv/bin/activate
python3 kit/ler_clipe.py $F/GMR/assets/xsens_bvh_test/251021_04_boxing_120Hz_cm_3DsMax.bvh; echo "saída: $?"
