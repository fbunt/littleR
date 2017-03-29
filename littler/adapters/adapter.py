class InputAdapter(object):
    """Base adapter class that wraps an input source

    Handles the source's specifics and exposes the source's data.
    Implementations should not take ownership of the source if it is
    an open file.
    """

    def __init__(self):
        self.count = 0
        self.levels = []
        self._start_date = None
        self._src_name = ''
        self._src_id = ''
        self._src_source = ''

    def set_source_str(self, src_str):
        """Set the string representing the source of the data"""
        self._src_source = src_str

    def set_id(self, id_):
        """Set the id of the data set"""
        self._src_id = id_

    def set_datetime(self, dt):
        """Set the datetime for the start of the data set"""
        self._start_date = dt

    def set_name(self, name):
        """Set the name to be used for the data set"""
        self._src_name = name

    def parse_data_source(self, src):
        """Parse the data source that the adapter wraps
        
        If the source is 
        """
        pass

    def getlevel(self, pos):
        """Return a `Level` container with the data for the level at `pos`"""
        return None
