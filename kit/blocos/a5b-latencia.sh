F=${FTH:-$HOME/fth}; cd $F/corpo-inteiro && . $F/.venv/bin/activate
for ms in 0 80 300 450 550; do
  echo "$ms ms → $(python3 kit/teleop_sim.py --roteiro kit/passos.json --latencia-ms $ms | tail -1)"
done
