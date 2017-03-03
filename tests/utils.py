import os

def get_data_filename(datafname):
    dfname = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     os.path.join('data', datafname))
    )
    return dfname

