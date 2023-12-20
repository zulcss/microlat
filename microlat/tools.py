import logging
import subprocess

from microlat import exceptions

def run(
    cmd
    ):
    """Run the specified command."""

    try:
        output = subprocess.run(
                    cmd,
                    check=True
                )
    except subprocess.CalledProcessError as e:
        msg = "Failed to run %s error code: %s, output: %s" \
                % (cmd[:0], e.returncode, e.stderr)
        exceptions.CommandFail(msg)
        
