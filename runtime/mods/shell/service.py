from typed import service, action, Str, Bool, List, Union
from utils.path import Path
from utils.number import Nat
from runtime.mods.env.enriched import Envs, Env
from runtime.mods.shell.types import ShellCmd
from runtime.mods.shell.err import ShellErr

@service(err=ShellErr)
class ShellService:
    @action
    def __split__(trm) -> List(Str):
        import shlex
        return shlex.split(str(trm))

    @action
    def run(
        trm: ShellCmd, 
        cwd: Path=None, 
        envs: Union(List(Env), Envs)={},
        terminate: Bool=True
    ):
        trm_list = ShellService.__split__(trm)

        shell_envs = {}
        if envs in List:
            import os
            for env in envs:
                shell_envs.update({env: os.getenv(env)})

        else:
            from runtime.mods.env.enriched import EnvValue
            for env, value in envs.items():
                shell_envs.update({env: EnvValue.serialize(value)})

        import subprocess
        if terminate:
            process = subprocess.run(
                trm_list,
                cwd=cwd,
                capture_output=True,
                text=True,
                env=shell_envs,
                check=False
            )
            return process.returncode, process.stderr, process.stdout
        else:
            try:
                process = subprocess.Popen(
                    trm_list,
                    cwd=cwd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    env=shell_envs
                )
                for line in process.stdout:
                    print(line, end='')
                process.wait()
                return None, None
            except Exception as e:
                print(f"Error in Popen: {e}", file=sys.stderr)
                return str(e), None

    @action
    def sleep(seconds: Nat=1):
        import time
        return time.sleep(seconds)

    @action
    def exit(code: Nat=0):
        import sys
        return sys.exit(code)
