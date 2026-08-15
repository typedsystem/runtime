def _is_cmd(entity):
    try:
        import shlex
        cmd = entity if isinstance(entity, str) else " ".join(list(entity))
        parsed = shlex.split(cmd)
        return True
    except:
        return False

def _is_script(path):
    import os
    if not os.path.isfile(path):
        return False
    with open(path, 'r') as file:
        if _is_cmd(file.read()):
            return True
    return False
