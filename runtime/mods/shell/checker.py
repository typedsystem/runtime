from typed.checker import Checker

class ShellChecker(Checker):
    def iscmd(self, entity: object) -> bool:
        from utils.mods.shell.types import Cmd
        if self.explode:
            from typed import require
            require.isterm(entity, Cmd)
        from typed import check
        return check.isterm(entity, Cmd)

    def isscript(self, entity: object) -> bool:
        from utils.mods.shell.types import Script
        if self.explode:
            from typed import require
            require.isterm(entity, Script)
        from typed import check
        return check.isterm(entity, Script)

    def isshell(self, entity: object) -> bool:
        from utils.mods.shell.types import Shell
        if self.explode:
            from typed import require
            require.isterm(entity, Shell)
        from typed import check
        return check.isterm(entity, Shell)

    def exists(self, entity: object) -> bool:
        cmd = self.isshell(entity)
        from shutil import which
        exists_ = which(cmd)
        if exists_:
            return True
        if self.explode:
            from utils.mods.err import NotExists
            raise NotExists(
                message="The provided command does not exists",
                cmd=cmd
            )
        return False

shell_check   = ShellChecker(quantifier=None, explode=False)
shell_require = ShellChecker(quantifier=None, explode=True)
