class MicrolatError(Exception):
    """Base class for microtlat exceptions."""

    def __init__(self, message=None):
        super(MicrolatError, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message or ""

class ConfigError(MicrolatError):
    """Microlat cofiguration error."""
    pass

class CommandNotFound(MicrolatError):
    """Command not found."""
    pass

class CommandFail(MicrolatError):
    """Command failure."""
    pass
