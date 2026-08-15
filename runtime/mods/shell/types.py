from typed import Filtered, Union, Str, prop
from utils.mods.types import Null
from utils.helper.shell import _is_cmd, _is_script
from utils.mods.path.types import File

Cmd    = Union(Filtered(Str, _is_cmd), Null(Str))
Script = Filtered(File, _is_script)
Shell  = Union(Cmd, Script)

prop.set.nameof(Cmd,    "Cmd")
prop.set.nameof(Script, "Script")
prop.set.nameof(Shell,  "Shell")

prop.set.nullof(Cmd, "")
prop.set.nullof(Shell, "")

