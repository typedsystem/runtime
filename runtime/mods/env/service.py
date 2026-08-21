from typed import Str, Dict, Bool
from typed.func import service, action
from runtime.mods.env.types import Envs, EnvValue, EnvFile, Env
from runtime.mods.env.err import EnvErr

@service(err=EnvErr)
class EnvValueService(EnvValue):
    @action
    def serialize(trm: EnvValue) -> Str:
        if isinstance(trm, (dict, list, tuple)):
            import json
            formatted_value = json.dumps(trm)
        elif isinstance(trm, bool):
            formatted_value = str(trm).lower()
        elif trm is None:
            formatted_value = ""
        else:
            formatted_value = str(trm)

        formatted_value = (
            formatted_value.replace("\\", "\\\\")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
            .replace('"', '\\"')
        )

        if " " in formatted_value and not (
            formatted_value.startswith('"') and formatted_value.endswith('"')
        ):
            formatted_value = f'"{formatted_value}"'

        return formatted_value

    @action
    def parse(trm: Str):
        import json
        value = str(trm)
        from typed import term, Int, Float, List, Set

        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]

        try:
            processed_value = value.replace("'", '"')
            parsed_value = json.loads(processed_value)
            if isinstance(parsed_value, (list, dict)) or (
                isinstance(parsed_value, (int, float, bool))
                and not value.isdigit()
                and not (value.count('.') == 1 and value.replace('.', '').isdigit())
            ):
                return parsed_value
            elif isinstance(parsed_value, str) and parsed_value != value:
                return term(parsed_value, Str)
            elif isinstance(parsed_value, (int, float, bool)) and (
                value.isdigit() or (value.count('.') == 1 and value.replace('.', '').isdigit())
            ):
                return term(parsed_value, Float)
            elif isinstance(parsed_value, list) and value.startswith('[') and value.endswith(']'):
                return term(parsed_value, List)
            elif isinstance(parsed_value, dict) and value.startswith('{') and value.endswith('}'):
                return term(parsed_value, Dict)
            elif isinstance(parsed_value, list) and value.startswith('{') and value.endswith('}'):
                return term(parsed_value, Set)
        except json.JSONDecodeError:
            pass
        if value.isdigit():
            try:
                return term(value, Int)
            except ValueError:
                pass
        if value.count('.') == 1 and value.replace('.', '').isdigit():
            try:
                return term(value, Float)
            except ValueError:
                pass

        return value

@service(err=EnvErr)
class EnvService(Envs):
    @action
    def get(trm: Env, default=None) -> EnvValue:
        import os
        value = os.getenv(trm)
        if value is None:
            from typed import term
            return term(default, EnvValueService)

        return EnvValueService.parse(value)

    @action
    def set(trm: Env, value: EnvValue) -> Env:
        import os
        os.environ[trm] = value
        from typed import term
        return term(trm, Env)

    @action
    def typeof(trm: Env):
        value = EnvService.get(trm)
        from typed import prop
        return prop.typeof(value)

    @action
    def match(trm: Env, value: EnvValue) -> Bool:
        value_ = EnvService.get(trm)
        return value_ == value

@service
class EnvsService:
    @action
    def serialize(trm: Envs) -> Dict(Str):
        from runtime.mods.env.checker import env_require
        serialized_envs = {}
        for key, value in trm.items():
            env_require.isenv(key)
            serialized_envs[key] = EnvValueService.serialize(value)
        return serialized_envs

@service
class EnvFileService(EnvFile):
    @action
    def read(trm: EnvFile) -> Envs:
        from runtime.helper.env import _read

        raw_envs = _read(trm)
        parsed_envs = {key: EnvValueService.parse(value) for key, value in raw_envs.items()}

        return parsed_envs

    @action
    def write(trm: EnvFile, envs=Envs):
        from typed import term

        serialized_data = EnvsService.serialize(envs)
        content = "\n".join([f"{key}={value}" for key, value in serialized_data.items()])
        with open(trm, 'w') as envfile:
            envfile.write(content)

        return term(trm, ...)

    @action
    def load(trm: EnvFile) -> EnvFile:
        envs = EnvFileService.read(trm)
        for key, value in envs.items():
            EnvService.set(key, EnvValueService.serialize(value))

        return trm

class env:
    parse = EnvValueService.parse
    serialize = EnvValueService.serialize
    get = EnvService.get
    set = EnvService.set
    match = EnvService.match

    class file:
        read = EnvFileService.read
        write = EnvFileService.write
        load = EnvFileService.load
