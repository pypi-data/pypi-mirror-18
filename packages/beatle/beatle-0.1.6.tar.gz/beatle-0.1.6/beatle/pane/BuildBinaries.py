"""Subclass of BuildBinaries, which is generated by wxFormBuilder."""

import app
import ctx


# Implementing BuildBinaries
class BuildBinaries(app.BuildBinaries):
    """Pane for binaries"""
    def __init__(self, parent):
        """Initialization"""
        super(BuildBinaries, self).__init__(parent)
        #read configuration
        self._config = ctx.theContext.config


