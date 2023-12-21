import logging
import shutil
import sys


from rich.console import Console
from stevedore import driver
import yaml

from microlat.config import Config
from microlat import exceptions
from microlat.log import setup_log

class Runner(object):
    def __init__(self, state):
        self.state = state
        self.console = Console(color_system=None)
        self.logging = logging.getLogger(__name__)
        self.workspace = self.state.workspace
        self.config = Config(state)

    def run(self):
        """Run microlat"""
        setup_log()

        self.logging.info("Running microlat.")
        self.logging.info("Loading confguration file.")

        if not self.state.config.exists():
            exceptions.ConfigError("Faile to load find configuration file.")

        config = self.config.get_config()
        name = config.get("name", None)
        if name is None:
            raise exceptions.ConfigError("Workspace name is not specified.")

        self.create_workspace(name)

        actions = self.config.get_actions()

        for action in actions:
            mgr = driver.DriverManager(
                    namespace='microlat.actions',
                    name=action,
                    invoke_on_load=True,
                    invoke_args=(self.state,
                                 self.workspace),
                  )
            mgr.driver.run_actions()

    def create_workspace(self, name):
        """Create the workspace directory where the build takes place."""
        self.workspace = self.workspace.joinpath(name)
        if self.workspace.exists():
            shutil.rmtree(self.workspace)
        self.logging.info("Copying configuration to workspace.")
        shutil.copytree(
            self.state.config.parent,
            self.workspace)
