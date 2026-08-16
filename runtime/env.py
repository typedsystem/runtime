from typed import lazy

__imports__ = {
    "runtime.mods.env.enriched": [
        "Env", "Envs", "EnvValue", "EnvFile"
    ],
    "runtime.mods.env.err": [
        "EnvErr"
    ]
}

if lazy(__imports__):
    from runtime.mods.env.enriched import (
        Env, Envs, EnvValue, EnvFile
    )
    from runtime.mods.env.err import EnvErr
