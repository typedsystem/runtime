def _read(trm):
    import os
    import re
    from runtime.mods.env.checker import env_require

    if not os.path.isfile(trm):
        raise ValueError(f"File not found: {trm}")

    envs = {}
    with open(trm, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = re.compile(
        r'^[ \t]*([a-zA-Z0-9_]+)[ \t]*=[ \t]*(?:'
        r'\'((?:[^\'\\]|\\.)*)\'|'
        r'"((?:[^"\\]|\\.)*)"|'
        r'([^#\n\r]*)'
        r')',
        re.MULTILINE
    )

    for match in pattern.finditer(content):
        key = match.group(1)
        env_require.isenv(key)

        val = match.group(2)
        if val is None:
            val = match.group(3)

        if val is None:
            val = match.group(4).strip()
        else:
            val = val.replace('\\"', '"').replace("\\'", "'").replace('\\n', '\n')

        envs[key] = val

    return envs

def _is_envfile(trm):
    try:
        envs = _read(trm)
        return True
    except:
        return False
