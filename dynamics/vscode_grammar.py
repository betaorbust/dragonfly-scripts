from dragonfly import (
    Function,
    MappingRule,
    Grammar,
    Dictation,
    IntegerRef,
    Key,
    Text
)

import lib.format
from lib.text import SCText

DYN_MODULE_TYPE = "programming_language"
DYN_MODULE_NAME = "vscode"
INCOMPATIBLE_MODULES = [

]

def findNthToken(text, n, direction):
        Key("c-f").execute()
        Text("%(text)s").execute({"text": text})
        if direction == "reverse":
            Key("s-enter:%(n)d").execute()
        else:
            Key("enter:%(n)d").execute()
        Key('escape').execute()


rules = MappingRule(
    mapping={
        # File management
        "[open] command palette": Key("cs-p"),
        "(Open [file] | Go to [tab]) [<text>]": Key("c-p") + Text("%(text)s"),
        "Close tab": Key("c-w"),
        "Save file": Key("c-s"),
        "Save and close": Key("c-s/10, c-w"),
       
        # Search
        "(search | find in) [all] (files | codebase)": Key("cs-f"),
        "(search | find) [file]": Key("c-f"),
        "(Find | Jump [to]) next <text>": Function(findNthToken, n=1, direction="forward"),
        "(Find | Jump [to]) previous <text>": Function(findNthToken, n=1, direction="reverse"),

        # Tab management       
        "nexta": Key("c-pgdown"),  # These would be next and previous tab but i have a conflict with chrome
        "prexta": Key("c-pgup"),
        "Close tab": Key("c-f4"),
        "Exit preview": Key("space, c-z"),

        # moving around a file
        "(go to | jump | jump to) line <n>": Key("c-g") + Text("%(n)d") + Key("enter"),
        "Go to definition": Key("f12"),
        "Go to required definition": Key("c-f12:2, c-right:5, left/50, f12"),
        "Go to (top | first line)": Key("c-home"),
        "Go to ( bottom | last line)": Key("c-end"),
        "ee-ol": Key("end"),
        "beol": Key("home"),
        "Go back": Key("a-left"),
        "Go forward": Key("a-right"),

        # Formatting
        "indent": Key("tab"),
        "Unindent": Key("s-tab"),
        "Comment": Key("c-slash"),
        "Block comment": Key("sa-a")
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
    ],
    defaults={
        "n": 1,
        "text": ""
    }
)

grammar = Grammar("VSCode grammar")
grammar.add_rule(rules)
grammar.load()
grammar.disable()


def dynamic_enable():
    global grammar
    if grammar.enabled:
        return False
    else:
        grammar.enable()
        return True


def dynamic_disable():
    global grammar
    if grammar.enabled:
        grammar.disable()
        return True
    else:
        return False


def is_enabled():
    global grammar
    if grammar.enabled:
        return True
    else:
        return False


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
