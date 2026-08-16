from typed import Filtered, Union, Str, Null, prop
from utils.path import File
from runtime.helper.shell import _is_cmd, _is_script

ShellCmd    = Union(Filtered(Str, _is_cmd), Null(Str))
ShellScript = Filtered(File, _is_script)

prop.set.nameof(ShellCmd,    "ShellCmd")
prop.set.nameof(ShellScript, "ShellScript")

prop.set.nullof(ShellCmd, "")
