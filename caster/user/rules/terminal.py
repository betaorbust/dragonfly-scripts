from dragonfly import (Grammar, AppContext, MappingRule,
                       Key, Text)

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
        "CD":               R(Text( "cd " ), rdescript="Terminal: Navigate Directory"),
        "make directory":   R(Text( "mkdir " ), rdescript="Terminal: Make directory"),
        "(ls|list)":        R(Text( "ls -al" )+Key("enter"), rdescript="Terminal: List All"),
        "exit":             R(Text( "exit" )+Key("enter"), rdescript="Terminal: Exit"),
        }
    extras = [
              
             ]
    defaults ={}

context = AppContext(title="Windows PowerShell") |  AppContext(title="powershell") |  AppContext(title="Console Emulator (x64)")
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