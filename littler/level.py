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
        self.source = ''
        self.alt = 0.0
        self.seq_num = 0
        self.is_sounding = False
        self.bogus = False
        # YYYY-MM-DD-hh:mm:ss
        self.date = '19700101000000'
        # Value and quality indicator pairs
        # Surface level pressure?
        # TODO: review necessity
        self.slp = (DEFAULT_FLOAT, 0)
        # Surface pressure
        self.sfc_pres = (DEFAULT_FLOAT, 0)
        # Precipitable water
        self.perfip_h2o = (DEFAULT_FLOAT, 0)

        # Number of record fields below that are utilized
        self.valid_fields = 0

        # RECORD VALUES
        # Value and quality indicator pairs
        # Pa
        self.pres = (DEFAULT_FLOAT, 0)
        # m
        self.height = (DEFAULT_FLOAT, 0)
        # K
        self.temp = (DEFAULT_FLOAT, 0)
        # K
        self.dewpoint = (DEFAULT_FLOAT, 0)
        # m/s
        self.windspd = (DEFAULT_FLOAT, 0)
        # deg
        self.winddir = (DEFAULT_FLOAT, 0)
        # m/s
        self.windu = (DEFAULT_FLOAT, 0)
        # m/s
        self.windv = (DEFAULT_FLOAT, 0)
        # %
        self.rh = (DEFAULT_FLOAT, 0)
        # m
        self.thickness = (DEFAULT_FLOAT, 0)
