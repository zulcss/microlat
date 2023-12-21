"""
- bootstrap:
"""
import logging
import sys
import shutil
import subprocess

from microlat import exceptions
from microlat.config import Config
from microlat.actions.base import Base
from microlat.utils import run_command

class BootstrapPlugin(Base):
    def __init__(self, state, workspace):
        self.logging = logging.getLogger(__name__)
        self.workspace = workspace
        self.state = state
        self.config = Config(self.state)

    def run_actions(self):
        """Run mmdebstrap."""
        self.logging.info("Creating rootfs")

        config = self.config.get_actions()["bootstrap"]
        if config is None:
            raise exceptions.ConfigErrror("Unable to determine bootstrap.")
        
        if not shutil.which("mmdebstrap"):
            exceptions.CommandNotFound("mmdebstrap is not found.")
            sys.exit(1)
        
        cmd = [ "mmdebstrap"]
        if self.state.debug:
            cmd += ["--debug"]
        else:
            cmd += ["-v"]

        suite = config.get("suite", None)
        if suite is None:
            raise exceptions.ConfigError("Suite is not found.")
        cmd += [ suite ]

        target = config.get("target", None)
        if target is None:
            raise exceptions.ConfigError("Target is not specified.")
        self.rootfs = self.workspace.joinpath(target)
        cmd += [str(self.rootfs)]

        variant = config.get("variant", None)
        if variant:
            cmd += [f"--variant={variant}"]

        packages = config.get("packages", None)
        if packages:
            cmd += [f"--include={', '.join(packages)}"]

        components = config.get("components", None)
        if components:
            cmd += [f"--components={', '.join(components)}"]

        setup_hooks = config.get("setup-hooks", None)
        if setup_hooks:
            cmd += [f"--setup-hook={hook}" for hook in setup_hooks]
        extract_hooks = config.get("extract-hook", None)
        if extract_hooks:
            cmd += [f"--extract-hook={hook}" for hook in extract_hooks]
        customize_hooks = config.get("customize-hooks", None)
        if customize_hooks:
            cmd += [f"--customize-hook={hook}" for hook in customize_hooks]

        self.logging.info("Running mmdebstrap.")
        run_command(cmd, cwd=self.workspace)