while inotifywait -r -e modify,create,delete /home/jfavreau/code/caster; do
    rsync -av --exclude '.git' --exclude 'bin' /home/jfavreau/code/caster/caster/ /home/jfavreau/code/dragonfly-scripts/caster/
    rsync -av /home/jfavreau/code/caster/_caster.py /home/jfavreau/code/dragonfly-scripts/_caster.py
done