
import logging
import os
import subprocess

from microlat import exceptions

LOG = logging.getLogger(__name__)


def run_command(cmd,
                debug=False,
                stdin=None,
                stdout=None,
                stderr=None,
                check=True,
                env=None,
                cwd=None):
    """Run a command in a shell."""
    _env = os.environ.copy()
    if env:
        _env.update(env)
    try:
        return subprocess.run(
            cmd,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            env=_env,
            cwd=cwd,
            check=check,
        )
    except FileNotFoundError:
        msg = "%s is not found in $PATH" % cmd[0]
        LOG.error(msg)
        raise exceptions.CommandError(msg)
    except subprocess.CalledProcessError as e:
        msg = "Shell execution error: %s, Output: %s" \
            % (e.returncode, e.stderr.decode("utf-8"))
        LOG.error(msg)
        raise exceptions.CommandError(msg)
