from typed import Filtered, Union, Str, Null, prop
from utils.path import File
from runtime.helper.shell import _is_cmd, _is_script
from runtime.mods.shell.meta import OUTPUT

ShellCmd    = Union(Filtered(Str, _is_cmd), Null(Str))
ShellScript = Filtered(File, _is_script)

class Output(metaclass=OUTPUT):
    __name__ = "Output"
    __display__ = "Output"

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypeVar, Type
    T = TypeVar('T')
    class Output:
        def __new__(cls: Type[T], code: int, stderr: str, stdout: str) -> Type[T]:
            cls.code = code
            cls.stderr = stderr
            cls.stdout = stdout
            ...

prop.set.nameof(ShellCmd,    "ShellCmd")
prop.set.nameof(ShellScript, "ShellScript")

prop.set.nullof(ShellCmd, "")
