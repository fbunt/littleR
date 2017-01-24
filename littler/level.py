DEFAULT_FLOAT = -888888.0
UNUSED_INT = -888888


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
        self.seq_num = 0
        self.bogus = False
        # YYYY-MM-DD-hh:mm:ss
        self.date = '19700101000000'
        # Value and quality indicator pairs
        # Surface level pressure?
        # TODO: review necessity
        self.slp = (_DEFAULT_FLOAT, 0)
        # Surface pressure
        self.sfc_pres = (_DEFAULT_FLOAT, 0)
        # Precipitable water
        self.perfip_h2o = (_DEFAULT_FLOAT, 0)

        # Number of record fields below that are utilized
        self.valid_fields = 0

        # RECORD VALUES
        # Value and quality indicator pairs
        self.pres = (_DEFAULT_FLOAT, 0)  # Pa
        self.height = (_DEFAULT_FLOAT, 0)  # m
        self.temp = (_DEFAULT_FLOAT, 0)  # K
        self.dewpoint = (_DEFAULT_FLOAT, 0)  # K
        self.windspd = (_DEFAULT_FLOAT, 0)  # m/s
        self.winddir = (_DEFAULT_FLOAT, 0)  # deg
        self.windu = (_DEFAULT_FLOAT, 0)  # m/s
        self.windv = (_DEFAULT_FLOAT, 0)  # m/s
        self.rh = (_DEFAULT_FLOAT, 0)  # %
        self.thickness = (_DEFAULT_FLOAT, 0)   # m
