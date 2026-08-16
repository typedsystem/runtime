from typed import Enriched
from runtime.mods.env.types import (
    Env as EnvType,
    Envs as EnvsType,
    EnvValue as EnvValueType,
    EnvFile as EnvFileType
)
from runtime.mods.env.service import (
    EnvService,
    EnvsService,
    EnvValueService,
    EnvFileService
)

Env      = Enriched(EnvType,      service=EnvService)
Envs     = Enriched(EnvsType,     service=EnvsService)
EnvValue = Enriched(EnvValueType, service=EnvValueService)
EnvFile  = Enriched(EnvFileType,  service=EnvFileService)
