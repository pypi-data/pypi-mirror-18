"""Subclass of NewVariable, which is generated by wxFormBuilder."""

import re
import copy
import wx
import wxx
from activity.models.ui import ui as ui
import model
import app.resources as rc


# Implementing NewVariable
class VariableDialog(ui.NewVariable):
    """
    This dialog allows to setup a non-member
    variable.
    """
    @wxx.SetInfo(__doc__)
    def __init__(self, parent, container):
        """Dialog initialization"""
        super(VariableDialog, self).__init__(parent)
        self._container = container
        self._types = dict([(x._name, x) for x in container.types])
        # add types but not on-the-fly template type
        self.m_choice1.AppendItems([x for x in self._types.keys() if x != '@'])
        self.choiceStr = ""
        self.m_textCtrl6.SetFocus()
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(rc.GetBitmap("member"))
        self.SetIcon(icon)

    # Handlers for NewVariable events.
    def OnTypeChanged(self, event):
        """Handle type change event"""
        """This event happens when the return type is changed. The main goal
        of this callback is handling template types for argument specification"""
        iSel = self.m_choice1.GetCurrentSelection()
        _type = self._types.get(self.m_choice1.GetString(iSel), None)
        template_args = False
        if _type is not None:
            if _type._template is not None:
                template_args = True
        if template_args is True:
            self.m_staticText67.Enable(True)
            self.m_template_args.Enable(True)
            self.m_staticText68.Enable(True)
        else:
            self.m_staticText67.Enable(False)
            self.m_template_args.Enable(False)
            self.m_staticText68.Enable(False)
            self.m_template_args.SetValue('')
        event.Skip()

    def CopyAttributes(self, variable):
        """Get the atributes"""
        variable._name = self._name
        variable._typei = copy.copy(self._typei)
        variable._static = self._static
        variable._default = self._default
        variable._volatile = self._volatile
        variable.note = self._note

    def SetAttributes(self, member):
        """Set the attributes"""
        self.m_textCtrl6.SetValue(member._name)
        ti = member._typei
        iSel = self.m_choice1.FindString(ti.type_name)
        self.m_choice1.SetSelection(iSel)
        iSel = self.m_choice2.FindString(member._access)
        self.m_choice2.SetSelection(iSel)
        self.m_checkBox105.SetValue(member._static)
        self.m_textCtrl8.SetValue(member._default)
        self.m_checkBox49.SetValue(member._volatile)
        self.m_checkBox11.SetValue(ti._const)
        self.m_checkBox13.SetValue(ti._ptr)
        self.m_checkBox12.SetValue(ti._ref)
        self.m_checkBox15.SetValue(ti._ptr_to_ptr)
        self.m_checkBox14.SetValue(ti._const_ptr)
        self.m_checkBox17.SetValue(ti._array)
        if ti._array is True:
            self.m_textCtrl7.Show(True)
            self.m_textCtrl7.Enable(True)
            self.m_textCtrl7.SetValue(str(ti._array_size))
        else:
            self.m_textCtrl7.SetValue('0')
        if ti._type_args is not None:
            self.m_staticText67.Enable(True)
            self.m_template_args.Enable(True)
            self.m_staticText68.Enable(True)
            self.m_template_args.SetValue(ti._type_args)
        self.m_richText1.SetValue(member.note)
        self.SetTitle("Edit variable")

    def Validate(self):
        """Dialog validation"""
        self._name = self.m_textCtrl6.GetValue()
        if len(self._name) == 0:
            wx.MessageBox("Variable name must not be empty", "Error",
                wx.OK | wx.CENTER | wx.ICON_ERROR, self)
            return False
        if re.match("^[A-Za-z_][0-9A-Za-z_]*$", self._name) is None:
            wx.MessageBox("Variable name contains invalid characters", "Error",
                wx.OK | wx.CENTER | wx.ICON_ERROR, self)
            return False
        iSel = self.m_choice1.GetCurrentSelection()
        if iSel == wx.NOT_FOUND:
            wx.MessageBox("Invalid type", "Error",
                wx.OK | wx.CENTER | wx.ICON_ERROR, self)
            return False
        typename = self.m_choice1.GetString(iSel)
        self._static = self.m_checkBox105.IsChecked()
        self._default = self.m_textCtrl8.GetValue()
        self._volatile = self.m_checkBox49.GetValue()
        if self.m_checkBox17.IsChecked():
            try:
                asize = int(self.m_textCtrl7.GetValue())
            except:
                asize = ''
        else:
            asize = None
        _type = self._types[typename]
        if _type._template is not None:
            #we construct type instance with explicit arguments
            type_args = self.m_template_args.GetValue()
            self._typei = model.cc.typeinst(
                type=_type,
                type_args=type_args,
                const=self.m_checkBox11.IsChecked(),
                ptr=self.m_checkBox13.IsChecked(),
                ref=self.m_checkBox12.IsChecked(),
                ptrptr=self.m_checkBox15.IsChecked(),
                constptr=self.m_checkBox14.IsChecked(),
                array=self.m_checkBox17.IsChecked(),
                arraysize=asize
            )
        else:
            self._typei = model.cc.typeinst(
                type=self._types[typename],
                const=self.m_checkBox11.IsChecked(),
                ptr=self.m_checkBox13.IsChecked(),
                ref=self.m_checkBox12.IsChecked(),
                ptrptr=self.m_checkBox15.IsChecked(),
                constptr=self.m_checkBox14.IsChecked(),
                array=self.m_checkBox17.IsChecked(),
                arraysize=asize
        )
        self._note = self.m_richText1.GetValue()
        return True

    def get_kwargs(self):
        """return arguments for object instance"""
        return  {'parent': self._container, 'name': self._name,
            'type': self._typei, 'static': self._static,
            'volatile': self._volatile, 'default': self._default,
            'note': self._note}

    def OnKeyDown(self, event):
        """Listbox selection"""
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_UP or keycode == wx.WXK_NUMPAD_UP:
            i = self.m_choice1.GetSelection()
            if i is not wx.NOT_FOUND and i > 0:
                self.m_choice1.SetSelection(i - 1)
        elif keycode == wx.WXK_DOWN or keycode == wx.WXK_NUMPAD_DOWN:
            i = self.m_choice1.GetSelection() + 1
            if i > wx.NOT_FOUND and i < len(self._types):
                self.m_choice1.SetSelection(i)
        elif keycode < 256:
            keychar = chr(keycode)
            if keychar.isalnum() or keycode is wx.WXK_SPACE:
                self.choiceStr += keychar.lower()
                for t in self._types:
                    tl = t.lower()
                    if tl.find(self.choiceStr) == 0:
                        sel = self.m_choice1.FindString(t)
                        if sel is not wx.NOT_FOUND:
                            self.m_choice1.SetSelection(sel)
                            if keycode is not wx.WXK_SPACE:
                                event.Skip()
                            return
            self.choiceStr = ""
        event.Skip()

    def OnToggleStatic(self, event):
        """toggle static event"""
        event.Skip()

    def OnPointerToggle(self, event):
        """ptr toggle gui"""
        if self.m_checkBox13.IsChecked():
            self.m_checkBox14.Enable(True)
            self.m_checkBox50.Enable(True)
            self.m_checkBox15.Enable(True)
        else:
            self.m_checkBox14.Enable(False)
            self.m_checkBox50.Enable(False)
            self.m_checkBox15.Enable(False)
            self.m_checkBox14.SetValue(False)
            self.m_checkBox50.SetValue(False)
            self.m_checkBox15.SetValue(False)
        event.Skip()

    def OnToggleArray(self, event):
        """Handle toggle array"""
        if  self.m_checkBox17.IsChecked():
            self.m_textCtrl7.Show(True)
            self.m_textCtrl7.Enable(True)
        else:
            self.m_textCtrl7.Show(False)
            self.m_textCtrl7.Enable(False)
        event.Skip()

    def OnCancel(self, event):
        """cancel event handler"""
        self.EndModal(wx.ID_CANCEL)

    def OnOK(self, event):
        """ok event handler"""
        if self.Validate():
            self.EndModal(wx.ID_OK)

