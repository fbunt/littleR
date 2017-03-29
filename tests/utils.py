import os
from StringIO import StringIO


def get_data_filename(datafname):
    dfname = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     os.path.join('data', datafname))
    )
    return dfname


class MyStringIO(StringIO):
    """A StringIO subclass that can be used in a 'with' statement"""
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        return False
