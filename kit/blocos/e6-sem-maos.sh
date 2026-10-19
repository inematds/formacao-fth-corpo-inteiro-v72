F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro && . $F/.venv/bin/activate
python3 kit/mao.py --modelo unitree_g1/scene.xml; echo "saída: $?"
