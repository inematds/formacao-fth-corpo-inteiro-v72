F=${FTH:-$HOME/fth}; cd $F/mujoco_menagerie && git sparse-checkout add wonik_allegro
cd $F/corpo-inteiro && . $F/.venv/bin/activate
python3 kit/mao.py --so-contar | grep -c "7 GDL"
python3 kit/mao.py --modelo wonik_allegro/right_hand.xml | tail -1
