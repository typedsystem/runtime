from typed.meta import TYPED

class OUTPUT(TYPED):
    def __call__(typ, code: int=0, stdout: str="", stderr: str=""):
        from typed import require
        require.isinstance(code, int)
        require.isinstance(stdout, str)
        require.isinstance(stderr, str)

        typ.code = code
        typ.stdout = stdout
        typ.stderr = stderr

        vars = []
        if stderr:
            vars.append(f"stderr='{stderr.strip()}'")
        if stdout:
            vars.append(f"stdout='{stdout.strip()}'")
        vars.append(f"code='{str(code)}'")

        display_name = f"Output({", ".join(vars)})"

        class Output(metaclass=OUTPUT):
            __name__ = display_name
            __display__ = display_name
            code = typ.code
            stderr = typ.stderr
            stdout = typ.stdout

        return Output
