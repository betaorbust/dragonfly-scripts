from dragonfly import (Grammar, AppContext, MappingRule,
                       Key, Text, Dictation)

from caster.lib import control
from caster.lib import settings
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class TerminalRule(MergeRule):
    pronunciation = "terminal"

    mapping = {
        "C drive":          R(Text("cd C:/")+Key("enter"), rdescript="Terminal: Go To C:"),
        "D drive":          R(Text("cd D:/")+Key("enter"), rdescript="Terminal: Go To D:"),
        "CD up":            R(Text( "cd .." )+Key("enter"), rdescript="Terminal: Up Directory"),
        "CD [<text>]":      R(Text( "cd %(text)s" ), rdescript="Terminal: Navigate Directory"),
        "make (directory|dir) [<text>]": R(Text( "mkdir %(text)s" ), rdescript="Terminal: Make directory"),
        "(l s|list)":        R(Text( "ls -al" )+Key("enter"), rdescript="Terminal: List All"),
        "exit":             R(Text( "exit" )+Key("enter"), rdescript="Terminal: Exit"),
        "previous":         R(Key("up") + Key("enter"), rdescript="Terminal: run previous"),
        "search history":   R(Key("c-r"), "Terminal: serach history"),
        "kill":             R(Key("c-c"), "Terminal: serach history"),
        }
    extras = [ 
        Dictation("text"),
        ]
    defaults ={
        "text": ""
    }

context = AppContext(executable="powershell") |  AppContext(executable="cmd")
grammar = Grammar("terminal", context=context)

if settings.SETTINGS["apps"]["terminal"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(TerminalRule())
        print("added terminal")
    else:
        rule = TerminalRule(name="terminal")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()