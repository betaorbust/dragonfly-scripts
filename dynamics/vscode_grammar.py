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

def define_function(text):
    Text("function ").execute()
    lib.format.camel_case_text(text)
    Text("() {").execute()
    Key("left:3").execute()


rules = MappingRule(
    mapping={
        # File management
        "[open] command palette": Key("cs-p"),
        "open file": Key("c-p"),
        "Close code tab": Key("c-w"),
        "Save file": Key("c-s"),
       
        # Search
        "(search | find in) [all] (files | codebase)": Key("cs-f"),
        "(search | find) [file]": Key("c-f"),

        # Tab management       
        "Next tab": Key("c-pgdown"),
        "Previous tab": Key("c-pgup"),
        "Close tab": Key("c-f4"),

        # moving around a file
        "(go to | jump | jump to) line <n>": Key("c-g") + Text("%(n)d") + Key("enter"),
        "Go to definition": Key("f12"),
        "Go to required definition": Key("c-f12:2") + Key("c-right:5") + Key("left/50") + Key("f12"),
        "Go to (top | first line)": Key("c-home"),
        "Go to ( bottom | last line)": Key("c-end")
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
    ],
    defaults={
        "n": 1
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
