import logging
import shutil
import sys


from rich.console import Console
from stevedore import driver
import yaml

from microlat import exceptions
from microlat.log import setup_log

class Runner(object):
    def __init__(self, state):
        self.state = state
        self.console = Console(color_system=None)
        self.logging = logging.getLogger(__name__)
        self.workspace = self.state.workspace
        self.config = None

    def run(self):
        """Run microlat"""
        setup_log()

        self.logging.info("Running microlat.")
        self.logging.info("Loading confguration file")

        if not self.state.config.exists():
            exceptions.ConfigError("Faile to load find configuration file")

        with open(self.state.config, "r") as f:
            try:
                self.config = yaml.safe_load(f)
            except yaml.YAMLError as e:
                msg = "Failed to load %s" \
                        %(self.state.config)
                self.logging.error(msg)
                raise exceptions.ConfigError(msg)
        
        name = self.config.get("name", None)
        if name is None:
            raise exceptions.ConfigError("Workspace name is not specified")

        self.create_workspace(name)

        actions = self.config.get("actions")

        for action in actions:
            mgr = driver.DriverManager(
                    namespace='microlat.actions',
                    name=action,
                    invoke_on_load=True,
                    invoke_args=(self.state,),
                  )
            mgr.driver.run_actions()

    def create_workspace(self, name):
        """Create the workspace directory where the build takes place."""
        self.workspace = self.workspace.joinpath(name)
        if self.workspace.exists():
            shutil.rmtree(self.workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
