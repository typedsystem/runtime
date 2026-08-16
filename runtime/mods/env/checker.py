from typed.checker import Checker

class EnvChecker(Checker):
    def isenv(self, entity: object) -> bool:
        from runtime.mods.env.types import Env
        if self.explode:
            from typed import require
            require.isterm(entity, Env)
        from typed import check
        return check.isterm(entity, Env)

    def exists(self, entity: object) -> bool:
        from runtime.mods.env.types import Env
        if self.explode:
            from typed import require
            require.isterm(entity, Env)
            import os
            if os.getenv(entity) is None:
                from runtime.mods.env.err import EnvErr
                raise EnvErr(
                    message="The received env does not exists",
                    env=entity
                )
        import os
        return os.getenv(entity) is not None
