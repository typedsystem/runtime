from typed import service, action, Bool, Dict
from utils.mods.path.types import Path

@service
class shell:
    @action
    def run(
        trm, 
        cwd: Path=None, 
        envs: Union(List(Env), Dict(Str, keys=Env))={},
        terminate: Bool=True, 
        **kargs: Dict
    ):
        if not trm in Union(List, Tuple):
            if trm in File:
                trm_list = file.read(trm)
            else:
                trm_list = shlex.split(str(trm))
        else:
            trm_list = [str(x) for x in trm]

        env = os.environ.copy()
        if envs in List:
            for env_var in envs:
                if env_var in os.environ:
                    env[env_var] = os.environ[env_var]
        if envs in Dict:
            env.update(envs)

        if terminate:
            process = subprocess.run(
                trm_list,
                cwd=cwd,
                capture_output=True,
                text=True,
                env=env,
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
                    env=env
                )
                for line in process.stdout:
                    print(line, end='')
                process.wait()
                return None, None
            except Exception as e:
                print(f"Error in Popen: {e}", file=sys.stderr)
                return str(e), None

    @action
    def sleep(seconds: Pos=1) -> Nill:
        import time
        return time.sleep(seconds)

    @action
    def exit(code: Nat=0) -> Nill:
        import sys
        return sys.exit(code)
