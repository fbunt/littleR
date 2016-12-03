class InputAdapter:
    """Base wrapper class for a data input"""

    def __init__(self, src=None, *args, **kwargs):
        self.src = src
        self.count = 0

    def getlevel(self, pos):
        """Return the `Level` container the information for the level at `pos`"""
        pass


class Level:
    """Container class for passing LITTLE_R level data"""

    def __init__(self):
        # HEADER VALUES
        self.lat = 0.0
        self.lon = 0.0
        self.id = ''
        self.name = ''
        self.platform = 'FM-35 TEMP'
        self.alt = 0.0
        self. seq_num = 0
        self.bogus = False
        # YYYY-MM-DD-hh:mm:ss
        self.date = '19700101000000'
        # Value and quality indicator pairs
        # TODO: determine what SLP stands for...
        self.slp = (0.0, 0)
        # Surface pressure
        self.sfc_pres = (0.0, 0)
        # Precipitable water
        self.perfip_h2o = (0.0, 0)

        # RECORD VALUES
        # Value and quality indicator pairs
        self.pres = (0.0, 0)  # Pa
        self.height = (0.0, 0)  # m
        self.temp = (0.0, 0)  # K
        self.dewpoint = (0.0, 0)  # K
        self.windspd = (0.0, 0)  # m/s
        self.winddir = (0.0, 0)  # deg
        self.windu = (0.0, 0)  # m/s
        self.windv = (0.0, 0)  # m/s
        self.rh = (0.0, 0)  # %
        self.thickness = (0.0, 0)   # m

