from typed import Enriched
from runtime.mods.shell.types import ShellCmd
from runtime.mods.shell.service import ShellService

Shell = Enriched(ShellCmd, service=ShellService)
