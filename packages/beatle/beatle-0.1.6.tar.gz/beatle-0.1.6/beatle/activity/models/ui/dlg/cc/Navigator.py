"""Subclass of Navigator, which is generated by wxFormBuilder."""

import wx
from activity.models.ui import ui as ui
import app.resources as rc
from model import cc


# Implementing Navigator
class NavigatorDialog(ui.Navigator):
    """
    This dialog shows insertable elements
    """
    _escKeyId = wx.Window.NewControlId()

    def __init__(self, parent, root, pos):
        """Initialice the navigator dialog"""
        super(NavigatorDialog, self).__init__(parent)
        self.imglist = rc.GetBitmapImageList()
        self.m_tree.SetImageList(self.imglist)
        # The root element is a class :
        # iterate and add elements
        treeid = self.m_tree.AddRoot(wx.EmptyString)
        self.m_tree.SetPyData(treeid, wx.TreeItemData(root))
        self.FillTree(treeid, root)
        first, cookie = self.m_tree.GetFirstChild(treeid)
        if first.IsOk():
            self.m_tree.SelectItem(first)
        self._set_accelerators()
        self.Move(pos)
        self.Show(True)
        self._str = wx.EmptyString

    def FillTree(self, treeid, obj, prefix=wx.EmptyString):
        """Fill the tree"""
        if obj is None:
            return
        if type(obj) is cc.Class:
            f = lambda x: x.inner_class == obj
            members = obj(cc.MemberData, filter=f, cut=True)
            members.sort()
            for member in members:
                treeitemid = self.m_tree.AppendItem(treeid, '{prefix}{name}'.format(
                    prefix=prefix, name=member.prefixed_name), image=member.bitmap_index)
                if type(member.type_instance.base_type) is cc.Class:
                    # Add has child property
                    self.m_tree.SetItemHasChildren(treeitemid, True)
                self.m_tree.SetPyData(treeitemid, wx.TreeItemData(member))
            methods = obj(cc.MemberMethod, filter=f, cut=True)
            methods.sort()
            for method in methods:
                treeitemid = self.m_tree.AppendItem(treeid, '{prefix}{call}'.format(
                    prefix=prefix, call=method.call), image=method.bitmap_index)
                if type(method.type_instance.base_type) is cc.Class:
                    # Add has child property
                    self.m_tree.SetItemHasChildren(treeitemid, True)
                self.m_tree.SetPyData(treeitemid, wx.TreeItemData(method))

    def OnSelectElement(self, event):
        """Handle to ensure scroll"""
        self.m_tree.ScrollTo(event.GetItem())

    def OnExpandItem(self, event):
        """Handle the expansion of the tree and inserting elemens"""
        treeitem = event.GetItem()
        if not treeitem.IsOk():
            return
        obj = self.m_tree.GetPyData(treeitem).GetData()
        if obj is None:
            return
        if self.m_tree.GetChildrenCount(treeitem, False) > 0:
            return
        tti = obj.type_instance
        if type(tti.base_type) is not cc.Class:
            return
        if tti.is_ptr:
            prefix = '->'
        else:
            prefix = '.'
        self.FillTree(treeitem, tti.base_type, prefix)

    def _set_accelerators(self):
        """Set the accelerator table"""
        aTable = wx.AcceleratorTable([
            wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, NavigatorDialog._escKeyId)
        ])
        self.SetAcceleratorTable(aTable)
        self.Bind(wx.EVT_MENU, self.OnCancel, id=NavigatorDialog._escKeyId)

    def OnLoseFocus(self, event):
        """Cancel search"""
        self.EndModal(wx.ID_CANCEL)

    def OnCancel(self, event):
        """Cancel search"""
        self.EndModal(wx.ID_CANCEL)

    def ChainedString(self, treeitem):
        if not treeitem.IsOk():
            return wx.EmptyString
        parentitem = self.m_tree.GetItemParent(treeitem)
        if not parentitem.IsOk():
            return wx.EmptyString
        text = self.m_tree.GetItemText(treeitem)
        return self.ChainedString(parentitem)+text

    @property
    def value(self):
        """return selected text"""
        return self._str

    def OnChoice(self, event):
        """Do final selection"""
        self._str = self.ChainedString(self.m_tree.GetSelection())
        self.EndModal(wx.ID_OK)
