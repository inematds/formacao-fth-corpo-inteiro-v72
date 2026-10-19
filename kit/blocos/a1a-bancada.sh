F=${FTH:-$HOME/fth}; mkdir -p $F && cd $F
[ -d .venv ] || python3.12 -m venv .venv
. .venv/bin/activate && pip install -q mujoco==3.16.0 numpy
[ -d corpo-inteiro ] || git clone -q --depth 1 https://github.com/inematds/formacao-fth-corpo-inteiro-v72 corpo-inteiro
[ -d mujoco_menagerie ] || git clone -q --filter=blob:none --sparse https://github.com/google-deepmind/mujoco_menagerie
cd mujoco_menagerie && git sparse-checkout add unitree_g1
git checkout -q 62ab00f && git log -1 --format='menagerie %h (%ad)' --date=short
python3 -c "import mujoco, numpy; print('mujoco', mujoco.__version__, '· numpy', numpy.__version__)"
