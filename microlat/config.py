import yaml

from microlat import exceptions

class Config:
    def __init__(self, state):
        self.state = state
    
    def get_config(self):
        """Load the configuration file."""
        with open(self.state.config, "r") as f:
            try:
               return yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise exceptions.ConfigError(
                    "Unable to parse configuration file.")

    def get_actions(self):
        config = self.get_config()
        actions = config.get("actions", None)
        if actions is None:
            raise exceptions.ConfigError("Unable to parse actions.")
        return actions
