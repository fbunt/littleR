import numpy as np
import pandas as pd

from .adapter import InputAdapter, Level


class GrawAdapter(InputAdapter):
    def __init__(self, src=None):
        if src is not None:
            self.src = src
            self._parse_src()

    def _parse_src(self):
        pass
