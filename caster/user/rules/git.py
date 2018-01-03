from dragonfly import Key, Text, Function, Dictation, Choice
from dragonfly.actions.action_base import Repeat

from caster.lib import control
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

def tab_if_text(text):
    if text!="":
        Key("tab").execute()

class Git(MergeRule):
    pronunciation = "Git"
    mapping = {
        "(git|get) status":                 R(Text("git status") + Key("enter"), rdescript="git status"),
        "(git|get) add":                    R(Text("git add -A"), rdescript="git add"),
        "(git|get) commit":                 R(Text("git commit -m \"\"") + Key("left"), rdescript="git commit"),
        "(git|get) commit (amend|and)":     R(Text("git commit --amend"), rdescript="git commit amend"),
        "(git|get) pull [<pull_flag>]":     R(Text("git pull %(pull_flag)s"), rdescript="git pull"),
        "(git|get) stash":                  R(Text("git stash"), rdescript="git stash"),
        "(git|get) stash pop":              R(Text("git stash pop"), rdescript="git stash pop"),
        "(git|get) new branch [<text>]":    R(Text("git checkout -b %(text)s"), rdescript="git new branch"),
        "(git|get) check out [<text>]":     R(Text("git checkout %(text)s") + Function(tab_if_text), rdescript="git checkout"),
        "(git|get) rebase [<rebase_flag>]": R(Text("git rebase %(rebase_flag)s"), rdescript="git rebase"),
    }
    
    extras   = [
        IntegerRefST("n", 1, 50),
        Dictation("text"),
        Choice("rebase_flag", {
            "interactive": "--interactive HEAD~1"
        }),
        Choice("pull_flag", {
            "rebase": "--rebase "
        }),
    ]

    defaults = {
        "n": 1,
        "text": "",
        "rebase_flag": "",
        "pull_flag": "",
    }
    
control.nexus().merger.add_global_rule(Git())
