import numpy as np
import pandas as pd

from .adapter import InputAdapter, Level


class GrawAdapter(InputAdapter):
    def __init__(self, src=None):
        super().__init__()
        if src is not None:
            self._parse(src)

    def _parse(self, src):
        pass
