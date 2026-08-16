from typed import Regex, Union, Null, Str, List, Dict, prop

Env = Union(Regex(r"^[A-Z0-9_]+$"), Null(Str))
EnvsList = List(Env)
EnvsDict = Dict(key=Env)
Envs = Union(EnvsList, EnvsDict)

prop.set.nameof(Env, "Env")
prop.set.nameof(EnvsList, "EnvsList")
prop.set.nameof(EnvsDict, "EnvsDict")
prop.set.nameof(Envs, "Envs")

prop.set.nullof(Env, "")
prop.set.nullof(EnvsList, [])
prop.set.nullof(EnvsDict, {})
prop.set.nullof(Envs, {})
