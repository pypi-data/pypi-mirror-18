"""Subclass of NewFile, which is generated by wxFormBuilder."""

import os
import wx
import wxx
import model
from activity.arch.ui import ui as ui


# Implementing NewFile
class NewFile(ui.NewFile):
    """
    This dialog allows to create a new free file inside any project.
    A free file is a file that is not vincled with the project model
    an may be freely edited or modified.
    """
    @wxx.SetInfo(__doc__)
    def __init__(self, parent, container):
        """constructor"""
        self.container = container  # the receiver of the new element
        super(NewFile, self).__init__(parent)
        if type(container) is model.Project:
            self._path = container.dir
        elif isinstance(container, model.arch.Dir):
            self._path = container.abs_file
        else:
            self._path, f = os.path.split(self.container.abs_file)

    def Validate(self):
        """validate the dialog"""
        fname = self.m_file.GetValue().strip()
        if not fname:
            wx.MessageBox("File name must be non empty", "Error",
                wx.OK | wx.CENTER | wx.ICON_ERROR, self)
            return False
        self._file = os.path.join(self._path, fname)
        #check about file existence
        if os.path.exists(self._file):
            wx.MessageBox("File already exists", "Error",
                wx.OK | wx.CENTER | wx.ICON_ERROR, self)
            return False
        return True

    def CopyAttributes(self, fobj):
        """Copy dialog selections to object"""
        fobj._file = self._file

    def SetAttributes(self, fobj):
        """Copy object attributes to dialog"""
        self._path, fname = os.path.split(fobj.abs_file)
        self.m_file.SetValue(fname)

    def get_kwargs(self):
        """Returns suitable arguments for creating object"""
        kwargs = {'parent': self.container, 'file': self._file}
        return kwargs

    def OnOK(self, event):
        """implement OnOK button"""
        if self.Validate():
            self.EndModal(wx.ID_OK)

    def OnCancel(self, event):
        """implement OnCancel button"""
        self.EndModal(wx.ID_CANCEL)


