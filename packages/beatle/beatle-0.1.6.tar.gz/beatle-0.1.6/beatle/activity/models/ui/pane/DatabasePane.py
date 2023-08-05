"""Subclass of DatabasePane, which is generated by wxFormBuilder."""
import wx
import wx.stc
from model import database
from app.handlers import IdentifiersHandler as ID
from activity.models.ui import ui as ui
from activity.models.handlers.sql import EditorHandler
from  ctx import theContext as context



# Implementing DatabasePane
class DatabasePane(ui.DatabasePane):
    """Implements database sql editor"""
    _closePane  = ID.register('close-pane')

    def __init__(self, parent, mainframe, object):
        """Initialize pane"""
        if object and type(object) in [database.Table, database.Field, database.Schema]:
            text = object.query
        else:
            text = ''
        self._editorArgs = {
            'language': 'sql',
            'handler': EditorHandler(text=text)
        }
        super(DatabasePane, self).__init__(parent)
        self._mainframe = mainframe
        self._object = object
        self._notebook = parent
        self._handler = None
        if object and type(object) in [database.Table, database.Field, database.Schema]:
            self._handler = object.project.handler
            try:
                self.ExecuteSQL()
            except:
                pass
        self.m_editor.Bind(wx.EVT_KILL_FOCUS, self.OnLeaveFocus)
        self.m_editor.Bind(wx.EVT_SET_FOCUS, self.OnGetFocus)

    def ExecuteSQL(self):
        """Try to execute sql"""
        try:
            dc = wx.ClientDC(self.m_grid)
            font = self.m_grid.GetFont()
            with database.dbopen(self._handler) as conn:
                with database.cursorquery(conn, self.m_editor.GetText()) as result:
                    # Ok, get the columns
                    self.m_grid.ClearColumns()
                    self.m_grid.DeleteAllItems()
                    for x in result.description:
                    #w, h = dc.GetTextExtent(x[0])
                        w = dc.GetFullTextExtent(x[0], font)[0]
                        w = max(w + 40, 40)
                        self.m_grid.AppendTextColumn(x[0], 0, w, wx.ALIGN_LEFT, 7)
                        # Iterate results
                    row = result.fetchone()
                    while row is not None:
                        #row = [str(x) for x in row[0]]
                        self.m_grid.AppendItem(row)
                        row = result.fetchone()
                """
                with database.rawquery(conn, self.m_editor.GetText()) as data:
                    # Ok, get the columns
                    self.m_grid.ClearColumns()
                    self.m_grid.DeleteAllItems()
                    for x in data.describe():
                        #w, h = dc.GetTextExtent(x[0])
                        w = dc.GetFullTextExtent(x[0], font)[0]
                        w = max(w + 40, 40)
                        self.m_grid.AppendTextColumn(x[0], 0, w, wx.ALIGN_LEFT, 7)
                    # Iterate results
                    for i in range(0, data.num_rows()):
                        row = [str(x) for x in data.fetch_row()[0]]
                        self.m_grid.AppendItem(row)"""
            self.m_grid.Layout()
        except:
            pass

    def OnLeaveFocus(self, event):
        """"""
        self.m_editor.SetSTCFocus(False)
        pass

    def OnGetFocus(self, event):
        """"""
        self.m_editor.SetSTCFocus(True)
        #self.m_editor.SetFocus()
        pass

    def Commit(self):
        pass
