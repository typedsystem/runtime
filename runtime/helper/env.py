
def _read(trm):
    from typed import term
    from utils import require
    from utils.path import File
    from runtime.mods.env.checker import env_require
    require.path.isfile(trm)
    lines = term(trm, File).linesof()
    envs = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        equals_index = line.find('=')
        if equals_index == -1:
            continue
        key = line[:equals_index].strip()
        env_require.isenv(key)
        value = line[equals_index + 1:].strip()
        envs.update({key: value})
    return envs

def _is_envfile(trm):
    try:
        envs = _read(trm)
        return True
    except:
        return False
