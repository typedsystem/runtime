from typed import Regex, Union, Null, Str, Int, Float, List, Dict, Filtered, prop, Nill
from utils.path import File
from runtime.helper.env import _is_envfile

Env      = Union(Regex(r"^[A-Z0-9_]+$"), Null(Str))
EnvValue = Union(Str, Int, Float, List, Dict, Nill)
Envs = Dict(EnvValue, key=Env)
EnvFile  = Filtered(File, _is_envfile)

prop.set.nameof(Env, "Env")
prop.set.nameof(Envs, "EnvsDict")
prop.set.nameof(EnvFile, "EnvFile")

prop.set.nullof(Env, "")
prop.set.nullof(Envs, {})
