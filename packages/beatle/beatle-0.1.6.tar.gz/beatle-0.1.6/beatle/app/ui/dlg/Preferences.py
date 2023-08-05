"""Subclass of Preferences, which is generated by wxFormBuilder."""

import wx, wxx
import app
from  app.ui import pane
from  ctx import theContext as context


# Implementing Preferences
class PreferencesDialog(app.Preferences):
    """
    This dialog is used for setup of common preferences.
    """
    @wxx.SetInfo(__doc__)
    def __init__(self, parent):
        """Initialization"""
        super(PreferencesDialog, self).__init__(parent)
        self._config = context.config
        self._fontPane = app.FontPreferences(self.m_auinotebook3)
        import platform
        s_plat = platform.platform() 
        if 'Linux' in s_plat or 'linux' in s_plat:
            self._linux = True
        else:
            self._linux = False
        if self._linux:
            self._webPane  = pane.WebPreferences(self.m_auinotebook3,
                use_proxy=self._config.ReadBool("config/web/useProxy", False),
                same=self._config.ReadBool("config/web/same_proxy",False),
                http_proxy=self._config.Read("config/web/http_proxy",''),
                https_proxy=self._config.Read("config/web/https_proxy",''),
                ftp_proxy=self._config.Read("config/web/ftp_proxy",''))
        if wx.__version__ >= '3.0.0.0':
            self.m_auinotebook3.AddPage(self._fontPane, u"Fonts", False, wx.wx.NOT_FOUND)
            if self._linux:
                self.m_auinotebook3.AddPage(self._webPane, u"Web", False, wx.wx.NOT_FOUND)
        else:
            self.m_auinotebook3.AddPage(self._fontPane, u"Fonts", False, wx.NullBitmap)
            if self._linux:
                self.m_auinotebook3.AddPage(self._webPane, u"Web", False, wx.NullBitmap)
        df = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        dfs = self.GetFontString(df)
        dfs = self._config.Read("config/defaultFont", dfs)
        self._font = self.GetStringFont(dfs)
        

    def GetFontString(self, font):
        """Get info about current font"""
        return font.GetNativeFontInfo().ToString()

    def GetStringFont(self, string):
        """Get info current font"""
        f = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        f.SetNativeFontInfoFromString(string)
        return f

    # Handlers for Preferences events.
    def OnInitDialog(self, event):
        """Dialog initialization"""
        self._fontPane.m_fontPicker.SetSelectedFont(self._font)
        # TODO: Implement OnInitDialog
        pass

    def OnOK(self, event):
        """OnOK handler"""
        dfs = self.GetFontString(self._fontPane.m_fontPicker.GetSelectedFont())
        self._webPane.GetData()
        self._config.Write("config/defaultFont", dfs)
        if self._linux:
            self._config.WriteBool("config/web/useProxy",self._webPane._use_proxy)
            self._config.WriteBool("config/web/same_proxy",self._webPane._use_same)
            self._config.Write("config/web/http_proxy",self._webPane._http_proxy.encode('UTF-8'))
            self._config.Write("config/web/https_proxy",self._webPane._https_proxy.encode('UTF-8'))
            self._config.Write("config/web/ftp_proxy",self._webPane._ftp_proxy.encode('UTF-8'))
        self._config.Flush()
        self.EndModal(wx.ID_OK)


