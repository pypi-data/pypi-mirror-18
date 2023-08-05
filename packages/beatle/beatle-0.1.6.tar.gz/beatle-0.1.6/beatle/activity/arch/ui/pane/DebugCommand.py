"""Subclass of DebugCommand, which is generated by wxFormBuilder."""
import wx
from activity.arch.ui import ui as ui


# Implementing DebugCommand
class DebugCommand(ui.DebugCommand):
    """aux pane for debug command"""

    def __init__(self, parent, handler):
        """init"""
        self._handler = handler
        super(DebugCommand, self).__init__(parent)

    def UpdateData(self, response):
        """Add data from debugger"""
        self.m_debugOutput.AppendText(response)
        if self.m_debugOutput.GetNumberOfLines() > 250:
            s = self.m_debugOutput.GetValue().splitlines()
            s = '\n'.join(s[50:])
            self.m_debugOutput.SetValue(s)


    def OnEnter(self, event):
        """Send command to debugger"""
        cmd = self.m_debugCommand.GetValue().strip()
        self.m_debugCommand.SetValue(wx.EmptyString)
        self._handler.send_command('#{0}'.format(cmd))
