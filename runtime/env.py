from typed import lazy

__imports__ = {
    "runtime.mods.env.enriched": [
        "Env", "Envs", "EnvValue", "EnvFile"
    ],
    "runtime.mods.env.err": [
        "EnvErr"
    ],
    "runtime.mods.env.service": [
        "env"
    ]
}

if lazy(__imports__):
    from runtime.mods.env.enriched import (
        Env, Envs, EnvValue, EnvFile
    )
    from runtime.mods.env.err import EnvErr
    from runtime.mods.env.service import env
