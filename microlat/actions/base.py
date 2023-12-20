from abc import ABC, abstractmethod

import logging

class Base(ABC):
    def __init__(self):
        self.workspace = None
        self.rootfs = None

    @abstractmethod
    def run_actions(self):
        pass
