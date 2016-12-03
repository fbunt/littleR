class InputAdapter:
    """Base adapter class that wraps an input source

    Handles the source's specifics and exposes the source's data.
    """

    def __init__(self):
        self.count = 0

    def set_src(self, src):
        """Set the adapter's source"""
        pass

    def getlevel(self, pos):
        """Return a `Level` container with the data for the level at `pos`"""
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

