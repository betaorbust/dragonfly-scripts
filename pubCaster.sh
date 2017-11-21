while inotifywait -r -e modify,create,delete /home/jfavreau/code/caster; do
    rsync -avz /home/jfavreau/code/caster/caster/ /home/jfavreau/code/dragonfly-scripts/caster/
    rsync -avz /home/jfavreau/code/caster/_caster.py /home/jfavreau/code/dragonfly-scripts/_caster.py
done