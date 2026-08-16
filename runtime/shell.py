from typed import lazy

__imports__ = {
    "runtime.mods.shell.types": [
        "ShellCmd", "ShellScript"
    ],
    "runtime.mods.shell.enriched": [
        "Shell"
    ],
    "runtime.mods.shell.err": [
        "ShellErr"
    ]
}

if lazy(__imports__):
    from runtime.mods.shell.types import ShellCmd, ShellScript
    from runtime.mods.shell.enriched import Shell
    from runtime.mods.shell.err import ShellErr
