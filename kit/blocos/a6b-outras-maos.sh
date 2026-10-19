F=${FTH:-$HOME/fth}; cd $F/mujoco_menagerie && git sparse-checkout add leap_hand shadow_hand
cd $F/corpo-inteiro && . $F/.venv/bin/activate
for h in leap_hand/right_hand.xml shadow_hand/right_hand.xml; do python3 kit/mao.py --modelo $h | tail -1 | sed "s#^#$h: #"; done
