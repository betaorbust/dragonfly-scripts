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
        "(git|get) branch":                 R(Text("git branch") + Key("enter"), rdescript="git branch"),
        "(git|get) status":                 R(Text("git status") + Key("enter"), rdescript="git status"),
        "(git|get) diff":                   R(Text("git diff"), rdescript="git diff"),
        "(git|get) add":                    R(Text("git add -A"), rdescript="git add"),
        "(git|get) commit":                 R(Text("git commit -m \"\"") + Key("left"), rdescript="git commit"),
        "(git|get) commit (amend|and)":     R(Text("git commit --amend"), rdescript="git commit amend"),
        "(git|get) push [<push_flag>] [<push_flag_2>]": R(Text("git push %(push_flag)s %(push_flag_2)s"), rdescript="git push"),
        "(git|get) pull [<pull_flag>]":     R(Text("git pull %(pull_flag)s"), rdescript="git pull"),
        "(git|get) stash [<text>]":         R(Text("git stash save \"%(text)s\"") + Key("left"), rdescript="git stash"),
        "(git|get) stash pop":              R(Text("git stash pop"), rdescript="git stash pop"),
        "(git|get) new branch [<text>]":    R(Text("git checkout -b %(text)s"), rdescript="git new branch"),
        "(git|get) check out [<text>]":     R(Text("git checkout %(text)s") + Function(tab_if_text), rdescript="git checkout"),
        "(git|get) rebase [<rebase_flag>]": R(Text("git rebase %(rebase_flag)s"), rdescript="git rebase"),
        "(git|get) reset":                  R(Text("git reset "), rdescript="git reset"),
    }
    

    gitPushMap = {
        "force": "--force",
        "no verify": "--no-verify"
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
        Choice("push_flag", gitPushMap),
        Choice("push_flag_2", gitPushMap)
    ]

    defaults = {
        "n": 1,
        "text": "",
        "rebase_flag": "",
        "pull_flag": "",
        "push_flag": "",
        "push_flag_2": "" 
    }
    
control.nexus().merger.add_global_rule(Git())
