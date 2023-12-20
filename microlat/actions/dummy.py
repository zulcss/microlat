"""
- bootstrap:
"""
import logging
import sys
import shutil
import subprocess

from microlat import exceptions
from microlat.actions.base import Base

class DummyPlugin(Base):
    def __init__(self, state):
        self.state = state

    def run_actions(self):
        """Run mmdebstrap."""
        print("in dummy plugin")
