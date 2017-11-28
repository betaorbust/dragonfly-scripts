from dragonfly import Key, Text, Pause, Choice, Function
from dragonfly.actions.action_base import Repeat

from caster.lib import control
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

def go_direction(direction):
    Key(direction).execute()


def select_characters(prev_next, n):
    Key("shift:down, %(direction)s:%(n)d, shift:up").execute({
        "direction": "right" if prev_next is "next" else "left",
        "n": n
    })



class Generic(MergeRule):
    pronunciation = "Generic"
    mapping = {
        "<direction> <n>": R(Function(go_direction), rdescript="move direction") * Repeat(extra="n"),
        "thin arrow":      R(Text(" -> "), rdescript="thin arrow"),
        "thick arrow":     R(Text(" => "), rdescript="thick arrow"),
        "dub quotes":      R(Text("") + Key("left"), rdescript="Double quotes"),
        "double quote":    R(Text("\""), rdescript="Double quote"),
        "quotes":          R(Text("''") + Key("left"), rdescript="Single quotes"),
        "single quote":    R(Text("'"), rdescript="Single quote"),

        "select <prev_next> <n>": R(Function(select_characters), rdescript="select characters"),
        # "select <prev_next> <n> words": R(Function(select_words), rdescript="select words"),
    }
    
    extras   = [
        Choice("direction", {
            "up": "up",
            "down": "down",
            "left": "left",
            "right": "right"
        }),
        Choice("prev_next", {
            "previous": "previous",
            "next": "next"
        }),
        IntegerRefST("n", 1, 50),
    ]

    defaults = {
        "n": 1
    }
    
control.nexus().merger.add_global_rule(Generic())
