from typed.checker import Checker

class ShellChecker(Checker):
    def iscmd(self, entity: object) -> bool:
        from runtime.mods.shell.types import ShellCmd
        if self.explode:
            from typed import require
            require.isterm(entity, ShellCmd)
        from typed import check
        return check.isterm(entity, ShellCmd)

    def isscript(self, entity: object) -> bool:
        from runtime.mods.shell.types import ShellScript
        if self.explode:
            from typed import require
            require.isterm(entity, ShellScript)
        from typed import check
        return check.isterm(entity, ShellScript)

    def exists(self, entity: object) -> bool:
        cmd = self.iscmd(entity)
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

shell_check   = ShellChecker(explode=False)
shell_require = ShellChecker(explode=True)
