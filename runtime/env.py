from typed import lazy

__imports__ = {
    "runtime.mods.env.enriched": [
        "Env", "Envs", "EnvValue", "EnvFile"
    ]
}

if lazy(__imports__):
    from runtime.mods.env.enriched import (
        Env, Envs, EnvValue, EnvFile
    )
