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
        "delete [<n>]":     R(Key("del:%(n)d"), rdescript="Delete"),
        "Line":             R(Key("enter"), rdescript="New line"), 
        "<direction> <n>":  R(Function(go_direction), rdescript="move direction"),
        "thin arrow":       R(Text(" -> "), rdescript="thin arrow"),
        "thick arrow":      R(Text(" => "), rdescript="thick arrow"),
        "dub quotes":       R(Text("\"\"") + Key("left"), rdescript="Double quotes"),
        "double quote":     R(Text("\""), rdescript="Double quote"),
        "sing quotes": R(Text("''") + Key("left"), rdescript="Single quotes"),
        "sing quote": R(Text("'"), rdescript="Single quote"),
        "Com-space":        R(Text(", "), rdescript="comma space"),
        "select <prev_next> <n>": R(Function(select_characters), rdescript="select characters"),
        "add":              R(Text(" + "), rdescript="Add"),
        "Subtract":         R(Text(" - "), rdescript="Subtract"),
        "(Copy|Cop) [This|That]": R(Key("c-c"), rdescript="Copy"),
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
