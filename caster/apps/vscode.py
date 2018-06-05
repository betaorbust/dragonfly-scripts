from dragonfly import (Grammar, AppContext, Dictation,
                       Key, Text, Repeat, Function)

from caster.lib import control
from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


def select_lines(x, y):
    '''Selects line x through y inclusive.'''
    if x < 1:
        return
    if y < 1:
        y = x
    if y < x:
        x, y = y, x

    Key("c-g").execute()
    Text("%(n)d").execute({"n": x})
    Key("enter").execute()
    Key("c-i").execute()  # Selects entire line
    Key("s-down:%(n)d").execute({"n": y - x})  # Select y-x following lines


def delete_lines(x, y):
    '''Deletes between line x and the line y inclusive.'''
    select_lines(x, y)
    Key("del").execute()


def copy_lines(x, y):
    '''Copy content from line x through y, inclusive.'''
    select_lines(x, y)
    Key("c-c").execute()


def cut_lines(x, y):
    '''Cut content from line x through y, inclusive.'''
    select_lines(x, y)
    Key("c-x").execute()


def find_nth_token(text, n, direction):
    Key("c-f").execute()
    Text("%(text)s").execute({"text": text})
    if direction == "reverse":
        Key("s-enter:%(n)d").execute({"n": n})
    else:
        Key("enter:%(n)d").execute({"n": n})
        Key('escape').execute()


class VisualStudioCodeRule(MergeRule):
    pronunciation = "visual studio code"

    mapping = {
        # ported from my dragonfly scripts
        # File management
        "[open] command palette": R(Key("cs-p"), rdescript="Visual Studio Code: Command Palette"),
        "(Open [file] | Go to [tab]) [<text>]": R(Key("c-p") + Text("%(text)s"), rdescript="Visual Studio Code: Go To File"),
        "Close (tab|file)": R(Key("c-w"), rdescript="Visual Studio Code: Close Tab"),
        "Save file": R(Key("c-s"), rdescript="Visual Studio Code: Save File"),
        "Save and close": R(Key("c-s/10, c-w"), rdescript="Visual Studio Code: Save And Close File"),

        # Search
        "(search | find in) [all] (files | codebase)": R(Key("cs-f"), rdescript="Visual Studio Code: Find in Codebase"),
        "(search | find) [file]": R(Key("c-f"), rdescript="Visual Studio Code: Find in File"),
        "(Find | Jump [to]) next <text>": R(Function(find_nth_token, n=1, direction="forward"), rdescript="Visual Studio Code: Find Next"),
        "(Find | Jump [to]) previous <text>": R(Function(find_nth_token, n=1, direction="reverse"), rdescript="Visual Studio Code: Find Previous"),

        # Tab management
        # These would be next and previous tab but i have a conflict with chrome
        "nexta [<n>]": R(Key("c-pgdown"), rdescript="Visual Studio Code: Next Tab") * Repeat(extra="n"),
        "prexta [<n>]": R(Key("c-pgup"), rdescript="Visual Studio Code: Previous Tab") * Repeat(extra="n"),
        "Close tab": R(Key("c-f4"), rdescript="Visual Studio Code: Close Tab"),
        "Exit preview": R(Key("space, c-z"), rdescript="Visual Studio Code: Exit Preview"),

        # moving around a file
        "(go to | jump | jump to) line <n>": R(Key("c-g") + Text("%(n)d") + Key("enter"), rdescript="Visual Studio Code: Go to Line"),
        "Go to definition": R(Key("f12"), rdescript="Visual Studio Code: Go to Definition"),
        "Go to required definition": R(Key("c-f12:2, c-right:5, left/50, f12"), rdescript="Visual Studio Code: Go to Required Definition"),
        "Go to (top | first line)": R(Key("c-home"), rdescript="Visual Studio Code: Go to Top"),
        "Go to ( bottom | last line)": R(Key("c-end"), rdescript="Visual Studio Code: Go to Bottom"),
        "ee-ol": R(Key("end"), rdescript="Visual Studio Code: End Of Line"),
        "beol": R(Key("home"), rdescript="Visual Studio Code: Beginning of Line"),
        "Go back [<n>]": R(Key("a-left"), rdescript="Visual Studio Code: Go Back") * Repeat(extra="n"),
        "Go forward [<n>]": R(Key("a-right"), rdescript="Visual Studio Code: Go Forward") * Repeat(extra="n"),

        # Formatting
        "indent [<n>]": R(Key("tab"), rdescript="Visual Studio Code: Indent") * Repeat(extra="n"),
        "Unindent [<n>]": R(Key("s-tab"), rdescript="Visual Studio Code: Unindent") * Repeat(extra="n"),
        "Comment": R(Key("c-slash"), rdescript="Visual Studio Code: Line Comment"),
        "Block comment": R(Key("sa-a"), rdescript="Visual Studio Code: Block Comment"),
        "format document": R(Key("sa-f"), rdescript="Format the entire document"),
        "format selection": R(Key("c-k") + Key("c-k"), rdescript="Format only the selected lines"),

        # Editing
        "select (line|lines) <x> [through <y>]": R(Function(select_lines), rdescript="VSC: Select lines"),
        "copy (lines|line) <x> [through <y>]":   R(Function(copy_lines), rdescript="VSC: Copy lines"),
        "cut (lines|line) <x> [through <y>]":    R(Function(cut_lines), rdescript="VSC: Cut lines"),
        "delete (lines|line) <x> [through <y>]": R(Function(delete_lines), rdescript="VSC: Delete Lines"),
        "expand selection [<n> [(times|time)]]": R(Key("sa-right"), rdescript="VSC: expand selection") * Repeat(extra="n"),
        "shrink selection [<n> [(times|time)]]": R(Key("sa-left"), rdescript="VSC: shrink selection") * Repeat(extra="n"),

        # Window Management
        "[toggle] full screen":         R(Key("f11"), rdescript="Visual Studio Code:Fullscreen"),
        "[toggle] Zen mode":            R(Key("c-k/3, z")),

        # Debugging
        "[toggle] breakpoint":          R(Key("f9"), rdescript="Visual Studio Code:Breakpoint"),
        "step over [<n>]":              R(Key("f10/50") * Repeat(extra="n"), rdescript="Visual Studio Code:Step Over"),
        "step into":                    R(Key("f11"), rdescript="Visual Studio Code:Step Into"),
        "step out [of]":                R(Key("s-f11"), rdescript="Visual Studio Code:Step Out"),
        "resume":                       R(Key("f5"), rdescript="Visual Studio Code:Resume"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
        IntegerRefST("x", -1, 10000),
        IntegerRefST("y", -1, 10000)
    ]
    defaults = {
        "n": 1,
        "x": -1,
        "y": -1,
        "mim": "",
        "text": ""
    }

# ---------------------------------------------------------------------------


context = AppContext(executable="code")
grammar = Grammar("Visual Studio Code", context=context)
if settings.SETTINGS["apps"]["visualstudiocode"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(VisualStudioCodeRule())
    else:
        rule = VisualStudioCodeRule(name="visualstudiocode")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
