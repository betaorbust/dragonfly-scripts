from dragonfly import Key, Text, Pause, Choice

from caster.lib import control
from caster.lib.ccr.standard import SymbolSpecs
from caster.lib.dfplus.additions import SelectiveAction
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

_AUTOCOMPLETE_WAIT_CS = "10"

class JavascriptCode(MergeRule):
    pronunciation = "Javascript in VS Code"
    mapping = {
        
        # CCR PROGRAMMING STANDARD
        SymbolSpecs.IF:                 R(Text("if") + Pause(_AUTOCOMPLETE_WAIT_CS) + Key("tab"), rdescript="Javascript: If"),
        SymbolSpecs.ELSE:               R(Text("else") + Pause(_AUTOCOMPLETE_WAIT_CS) + Key("tab"), rdescript="Javascript: Else"),
        #
        SymbolSpecs.SWITCH:             R(Text("switch") + Pause(_AUTOCOMPLETE_WAIT_CS) + Key("tab"), rdescript="Javascript: Switch"),
        SymbolSpecs.CASE:               R(Text("case :") + Key("left"), rdescript="Javascript: Case"),
        SymbolSpecs.BREAK:              R(Text("break;") + Key("enter"), rdescript="Break"),
        SymbolSpecs.DEFAULT:            R(Text("default:") + Key("enter"), rdescript="Javascript: Default"),
        #
        SymbolSpecs.DO_LOOP:            R(Text("dowhile") + Pause(_AUTOCOMPLETE_WAIT_CS) + Key("tab"), rdescript="Javascript: Do Loop"),
        SymbolSpecs.WHILE_LOOP:         R(Text("while") + Pause(_AUTOCOMPLETE_WAIT_CS) + Key("tab"), rdescript="Javascript: While"),
        SymbolSpecs.FOR_LOOP:           R(Text("for") + Pause(_AUTOCOMPLETE_WAIT_CS) + Key("tab"), rdescript="Javascript: For i Loop"),
        SymbolSpecs.FOR_EACH_LOOP:      R(Text("forin") + Pause(_AUTOCOMPLETE_WAIT_CS), rdescript="Javascript: For Each Loop"),
        #
        SymbolSpecs.TO_INTEGER:         R(Text("parseInt()") + Key("left"), rdescript="Javascript: Convert To Integer"),
        SymbolSpecs.TO_FLOAT:           R(Text("parseFloat()") + Key("left"), rdescript="Javascript: Convert To Floating-Point"),
        SymbolSpecs.TO_STRING:          R(Text("\"\" + "), rdescript="Javascript: Convert To String"),
        #
        SymbolSpecs.AND:                R(Text(" && "), rdescript="Javascript: And"),
        SymbolSpecs.OR:                 R(Text(" || "), rdescript="Javascript: Or"),
        SymbolSpecs.NOT:                R(Text("!"), rdescript="Javascript: Not"),
        #
        SymbolSpecs.SYSOUT:             R(Text("console.log()") + Key("left"), rdescript="Javascript: Print"),
        #
        # (no imports in javascript)
        # 
        SymbolSpecs.FUNCTION:           R(Text("function") + Pause(_AUTOCOMPLETE_WAIT_CS) + Key("tab"), rdescript="Javascript: Function"),
        # (no classes in javascript yet)
        #
        SymbolSpecs.COMMENT:            R(Text("//"), rdescript="Javascript: Add Comment"),
        SymbolSpecs.LONG_COMMENT:       R(Text("/**/") + Key("left,left"), rdescript="Javascript: Long Comment"),
        #
        SymbolSpecs.NULL:               R(Text("null"), rdescript="Javascript: Null"),
        #
        SymbolSpecs.RETURN:             R(Text("return "), rdescript="Javascript: Return"),
        #
        SymbolSpecs.TRUE:               R(Text("true"), rdescript="Javascript: True"),
        SymbolSpecs.FALSE:              R(Text("false"), rdescript="Javascript: False"),
        
        
        # JavaScript specific
        "anon funk":                    R(Text("anon") + Pause(_AUTOCOMPLETE_WAIT_CS) + Key("tab"), rdescript="Javascript: Anonymous Function"),
        "short anon funk":              R(Text("short anon") + Pause(_AUTOCOMPLETE_WAIT_CS) + Key("tab"), rdescript="Javascript: Anonymous Function"),
        "set interval":                 R(Text("setInterval()") + Key("left"), rdescript="Javascript: Timer"),
        "set timeout":                  R(Text("setTimeout()") + Key("left"), rdescript="Javascript: Timeout"),
        "document":                     R(Text("document"), rdescript="Javascript: Document"),
        "index of":                     R(Text("indexOf()") + Key("left"), rdescript="Javascript: Index Of"),
        "has own property":             R(Text("hasOwnProperty()") + Key("left"), rdescript="Javascript: Has Own Property"),
        "length":                       R(Text("length"), rdescript="Javascript: Length"),
        "self":                         R(Text("self"), rdescript="Javascript: Self"),
        "push":                         R(Text("push"), rdescript="Javascript: Push"),
        "inner HTML":                   R(Text("innerHTML"), rdescript="Javascript: InnerHTML"),
        "new new":                      R(Text("new "), rdescript="Javascript: New"),
        "continue":                     R(Text("continue"), rdescript="Javascript: Continue"),

        "this":                         R(Text("this"), rdescript="Javascript: This"),
        "try":                          R(Text("trycatch") + Pause(_AUTOCOMPLETE_WAIT_CS) + Key("tab"), rdescript="Javascript: Try"),

        "throw":                        R(Text("throw "), rdescript="Javascript: Throw"),
        "instance of":                  R(Text("instanceof "), rdescript="Javascript: Instance Of"),
        
        "var":                          R(Text("var "), rdescript="Javascript: Var"),
        "const":                        R(Text("const "), rdescript=" JavaScript: Const"),
        "Let":                          R(Text("let "), rdescript=" JavaScript: Let"),

        "else if":                      R(Text("else if") + Pause(_AUTOCOMPLETE_WAIT_CS) + Key("tab"), rdescript="Javascript: Else If"),
        
        "(object|obj) (property | prop)":  R(Text(": ") + Key("left:2"), rdescript="Javascript: object method"),
        "(object|obj) [dot] <objectMethods>":    R( Text ("object.%(objectMethods)s()") + Key("left"), rdescript="JavaScript: Object prototype methods"),
        "(object|obj) [dot] <objectProperties>": R( Text ("object.%(objectProperties)s"), rdescript="JavaScript: Object prototype properties"),
        "assign":                       R(Text(" = "), rdescript="Javascript: assign"),
        "identity":                     R(Text(" === "), rdescript="Javascript: equals"),
        "Semi":                         R( Text(";"), rdescript="JavaScript: semicolon"),
        "Doc block":                    R( Text("/**") + Pause(_AUTOCOMPLETE_WAIT_CS) + Key("tab"), rdescript="JavaScript: Document block"),
        "Doc this":                     R(Text("/** Document This") + Pause(_AUTOCOMPLETE_WAIT_CS) + Key("tab"), rdescript="JavaScript: Document This"),
        "console [dot] <logType>":       R( Text("console.%(logType)s()") + Key("left"), rdescript="JavaScript: Console output"),
    }
    
    extras   = [
        Choice("logType", {
            "debug": "debug",
            "error": "error",
            "info": "info",
            "log": "log",
            "warn": "warn",
            "dir": "dir",
            "dir xml": "dirxml",
            "table": "table",
            "trace": "trace",
            "group": "group",
            "group collapsed": "groupCollapsed",
            "group end": "groupEnd",
            "clear": "clear",
            "count": "count",
            "assert": "assert",
            "mark timeline": "markTimeline",
            "profile": "profile",
            "profile and": "profileEnd",
            "timeline": "timeline",
            "timeline and": "timelineEnd",
            "time": "time",
            "time end": "timeEnd",
            "time stamp": "timeStamp",
            "context": "context",
            "memory": "memory"
        }),
        Choice("objectMethods",{
            "assign": "assign",
            "getOwnPropertyDescriptor": "getOwnPropertyDescriptor",
            "getOwnPropertyDescriptors": "getOwnPropertyDescriptors",
            "getOwnPropertyNames": "getOwnPropertyNames",
            "getOwnPropertySymbols": "getOwnPropertySymbols",
            "is": "is",
            "preventExtensions": "preventExtensions",
            "seal": "seal",
            "create": "create",
            "defineProperties": "defineProperties",
            "defineProperty": "defineProperty",
            "freeze": "freeze",
            "getPrototypeOf": "getPrototypeOf",
            "setPrototypeOf": "setPrototypeOf",
            "isExtensible": "isExtensible",
            "isFrozen": "isFrozen",
            "isSealed": "isSealed",
            "keys": "keys",
            "entries": "entries",
            "values": "values"
        }),
        Choice("objectProperties",{
            "length": "length",
            "name": "name",
            "prototype": "prototype"
        })
    ]
    defaults = {}
    
control.nexus().merger.add_global_rule(JavascriptCode())
