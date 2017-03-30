import numpy as np


def uv_from_met(spd, metang):
    """Convert the wind direction/angle to u, v components

    This assumes that the given angle is direction FROM which the
    wind originates.

    See: http://tornado.sfsu.edu/geosciences/classes/m430/Wind/WindDirection.html
    """
    # East
    u = -spd * np.sin(np.radians(metang))
    # North
    v = -spd * np.cos(np.radians(metang))
    return u, v


def uv_from_vect(spd, vectang):
    """Convert the wind direction/angle to u, v components

    This assumes that the given angle is the direction TO which the
    wind is blowing.

    See: http://tornado.sfsu.edu/geosciences/classes/m430/Wind/WindDirection.html
    """
    # East
    u = spd * np.sin(np.radians(vectang))
    # North
    v = spd * np.cos(np.radians(vectang))
