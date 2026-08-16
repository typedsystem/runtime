from runtime.mods.env.checker import env_check, env_require
from runtime.mods.shell.checker import shell_check, shell_require

class check:
    env   = env_check
    shell = shell_check

class require:
    env   = env_require
    shell = shell_require
