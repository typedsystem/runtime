from typed import lazy

__imports__ = {
    "runtime.mods.checker": [
        "check", "require"
    ],
    "runtime.mods.prop": [
        "prop"
    ],
    "runtime.mods.runtime_": [
        "runtime"
    ]
}

if lazy(__imports__):
    from runtime.mods.checker import check, require
    from runtime.mods.prop import prop
    from runtime.mods.runtime_ import runtime
