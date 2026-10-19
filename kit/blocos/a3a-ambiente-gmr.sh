F=${FTH:-$HOME/fth}; cd $F/GMR
git sparse-checkout add general_motion_retargeting scripts assets/unitree_g1
cd $F && [ -d .venv-gmr ] || python3.12 -m venv .venv-gmr
. .venv-gmr/bin/activate
pip install -q --index-url https://download.pytorch.org/whl/cpu torch==2.14.1
pip install -q mujoco==3.16.0 numpy==2.5.4 scipy==1.18.1 mink==1.3.0 qpsolvers==4.13.0 daqp==0.10.3 rich tqdm loop_rate_limiters imageio
pip install -q --no-deps -e GMR
python3 -c "from importlib.metadata import version as v; print(*[f'{p} {v(p)}' for p in ('torch', 'mink', 'mujoco', 'general_motion_retargeting')], sep=' · ')"
