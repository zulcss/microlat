import logging
import shutil
import sys

from microlat.log import complete_step
from microlat.log import log_step


def preflight_check():
    """Checking for required tools."""
    with complete_step("Checking for required tools"):
        log_step("Chekcking for mmdebstrap")
        if not shutil.which("mmdebstrap"):
            logging.info("mmdebstrop is not found")
            sys.exit(-1)

        log_step("Chekcing for debos")
        if not shutil.which("debos"):
            logging.info("debos is not found")
            sys.exit(-1)
