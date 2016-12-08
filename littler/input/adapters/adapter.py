class InputAdapter:
    """Base adapter class that wraps an input source

    Handles the source's specifics and exposes the source's data.
    """

    def __init__(self):
        self.count = 0

    def getlevel(self, pos):
        """Return a `Level` container with the data for the level at `pos`"""
        pass