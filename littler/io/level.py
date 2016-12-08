class Level:
    """Container class for passing LITTLE_R level data"""

    def __init__(self):
        # TODO: pull out default (-888888.0) value
        # HEADER VALUES
        self.lat = 0.0
        self.lon = 0.0
        self.id = ''
        self.name = ''
        self.platform = 'FM-35 TEMP'
        self.alt = 0.0
        self.seq_num = 0
        self.bogus = False
        # YYYY-MM-DD-hh:mm:ss
        self.date = '19700101000000'
        # Value and quality indicator pairs
        # TODO: determine what SLP stands for...
        self.slp = (-888888.0, 0)
        # Surface pressure
        self.sfc_pres = (-888888.0, 0)
        # Precipitable water
        self.perfip_h2o = (-888888.0, 0)

        # RECORD VALUES
        # Value and quality indicator pairs
        self.pres = (-888888.0, 0)  # Pa
        self.height = (-888888.0, 0)  # m
        self.temp = (-888888.0, 0)  # K
        self.dewpoint = (-888888.0, 0)  # K
        self.windspd = (-888888.0, 0)  # m/s
        self.winddir = (-888888.0, 0)  # deg
        self.windu = (-888888.0, 0)  # m/s
        self.windv = (-888888.0, 0)  # m/s
        self.rh = (-888888.0, 0)  # %
        self.thickness = (-888888.0, 0)   # m
