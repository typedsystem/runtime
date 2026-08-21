from typed import service, action, Str, Int, Bool, List, Union, Maybe
from utils.path import Path
from utils.number import Nat
from runtime.mods.env.enriched import Envs, Env
from runtime.mods.shell.meta import OUTPUT
from runtime.mods.shell.err import ShellErr

@service(err=ShellErr)
class ShellService:
    @action
    def __split__(trm) -> List(Str):
        import shlex
        return shlex.split(str(trm))

    @action
    def run(
        trm, 
        cwd: Path=".", 
        envs: Union(List(Env), Envs)={},
        terminate: Bool=True,
        timeout: Maybe(Int)=None
    ) -> OUTPUT:
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
        from runtime.mods.shell.types import Output

        if terminate:
            try:
                process = subprocess.run(
                    trm_list,
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    env=shell_envs,
                    check=False,
                    timeout=timeout
                )
                return Output(
                    code=process.returncode,
                    stdout=process.stdout,
                    stderr=process.stderr
                )
            except subprocess.TimeoutExpired as e:
                return Output(
                    code=124,
                    stdout=str(e.stdout) if e.stdout else "",
                    stderr=f"Command timed out after {timeout} seconds"
                )
        else:
            import sys
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
                stdout_lines = []
                for line in process.stdout:
                    print(line, end='')
                    stdout_lines.append(line)

                process.wait(timeout=timeout)
                return Output(
                    code=process.returncode,
                    stdout="".join(stdout_lines),
                    stderr=""
                )
            except subprocess.TimeoutExpired:
                process.kill()
                return Output(
                    code=124,
                    stdout="".join(stdout_lines),
                    stderr=f"Command timed out after {timeout} seconds"
                )
            except Exception as e:
                print(f"Error in Popen: {e}", file=sys.stderr)
                return Output(
                    code=1,
                    stdout="",
                    stderr=str(e)
                )

    @action
    def sleep(seconds: Nat=1):
        import time
        return time.sleep(seconds)

    @action
    def exit(code: Nat=0):
        import sys
        return sys.exit(code)

shell = ShellService
