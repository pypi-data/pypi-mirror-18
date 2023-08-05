"""Subclass of FilesView, which is generated by wxFormBuilder."""

import re
import os
import wx
import wxx
import app
import tran
import model
import ostools
import deco
import app.resources as rc
from app.ui.view import BaseView
from activity.arch.ui import ui, pane, dlg
from activity.arch.actions import debugPythonSession
from activity.arch.actions import build
from ctx import localcontext as context


class FilesView(BaseView, ui.FilesView):
    """Implements pane for file view"""
    clipboard_handler = False
    run_handler = True
    debug_handler = True
    build_handler = True

    perspective = ''
    _refreshFilesId = wx.Window.NewControlId()
    _addProjectFileId = wx.Window.NewControlId()
    _addProjectDirId = wx.Window.NewControlId()

    def __init__(self, parent, root=None):
        """Initialize pane"""
        super(FilesView, self).__init__(parent)
        self.frame = parent
        self.imglist = ostools.MimeHandler.imageList
        self.m_tree.SetImageList(self.imglist)
        self._create_menus()
        self._create_toolbars()
        self._bind_events()
        self._set_accelerators()
        self.m_tree.AddRoot('Projects')
        self.selected = None
        # when we create a models view, we need to update elements
        if root is None:
            # reload full stack
            theApp = context.app
            for wrk in theApp.workspaces:
                self.insert(wrk)
        # enhancement for popup subviews
        else:
            self.insert(root)

    def insert(self, element):
        """Nested insert elements in tree"""
        self.DoRenderAddElement(element)
        for cls in element._child:
            for k in element[cls]:
                self.insert(k)

    def _create_menus(self):
        """Create the view menus"""
        super(FilesView, self)._create_menus()
        self._menu = wx.Menu()
        # add directory
        self._addDir = wx.MenuItem(self._menu, self._addProjectDirId, u"Add new directory ...\tCtrl+N",
            u"add new file", wx.ITEM_NORMAL)
        self._addDir.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_MENU))
        self._menu.AppendItem(self._addDir)
        self._menu.AppendSeparator()
        # add file
        self._addFile = wx.MenuItem(self._menu, self._addProjectFileId, u"Add new file ...\tCtrl+N",
            u"add new file", wx.ITEM_NORMAL)
        self._addFile.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_MENU))
        self._menu.AppendItem(self._addFile)
        self._menu.AppendSeparator()
        # refresh files
        self._refreshFiles = wx.MenuItem(self._menu, self._refreshFilesId, u"Refresh files",
            u"refresh files", wx.ITEM_NORMAL)
        self._refreshFiles.SetBitmap(wx.Bitmap(u"app/res/refresh.xpm", wx.BITMAP_TYPE_ANY))
        self._menu.AppendItem(self._refreshFiles)
        self.RegisterMenu('Files', self._menu)

    def _create_toolbars(self):
        """Create the toolbar menus"""
        super(FilesView, self)._create_toolbars()

    def _bind_events(self):
        """Bind events to this view"""
        self.m_tree.Bind(wx.EVT_RIGHT_DOWN, self.OnTreeMenu)
        self.m_tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnTreeOpenFile)
        self.m_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelChanged)
        # add files
        self.BindSpecial(wx.EVT_UPDATE_UI, self.OnUpdateAddFiles, id=self._addProjectFileId)
        self.BindSpecial(wx.EVT_MENU, self.OnAddFiles, id=self._addProjectFileId)
        self.BindSpecial(wx.EVT_UPDATE_UI, self.OnUpdateAddDir, id=self._addProjectDirId)
        self.BindSpecial(wx.EVT_MENU, self.OnAddDir, id=self._addProjectDirId)
        # refresh files
        self.BindSpecial(wx.EVT_MENU, self.OnRefreshAllFiles, id=self._refreshFilesId)

        # debug
        self.BindSpecial(wxx.EVT_DEBUGGER, self.OnDebugEvent)

        super(FilesView, self)._bind_events()

    def _set_accelerators(self):
        """Set the accelerator table"""
        # ctrl_alt = wx.ACCEL_CTRL + wx.ACCEL_ALT
        # ctrl_shf = wx.ACCEL_CTRL + wx.ACCEL_SHIFT
        aTable = wx.AcceleratorTable([
            wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('N'), self._addProjectFileId),
            wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_LEFT, BaseView._leftKeyId)
        ])
        self.SetAcceleratorTable(aTable)

    @deco.classproperty
    def name(cls):
        """returns the name of this view"""
        return 'Files'

    @classmethod
    def bitmap_index(cls):
        """return the bitmap index"""
        return rc.GetBitmapIndex('files')

    @classmethod
    def bitmap(cls):
        """return the bitmap"""
        return rc.GetBitmap('files')

    def DoRenderAddElement(self, obj):
        """Inserts element in tree"""
        # model tree
        treeOrder = [
            model.Workspace, model.Project,
            model.arch.Dir, model.arch.File
            ]
        if not obj._visibleInTree or type(obj) not in treeOrder:
            return
        ti = treeOrder.index(type(obj))
        #check parent
        if self.m_tree.HoldsObject(obj.parent):
            p = obj.parent
        else:
            p = self.m_tree.GetRootItem()
        if obj.parent is not None:
            # find some major friend item with the same class
            tribal = obj.parent[type(obj)]
            index = tribal.index(obj)
            pre = None
            while index > 0 and pre is None:
                index = index - 1
                candidate = tribal[index]
                if not self.m_tree.HoldsObject(candidate):
                    continue
                pre = candidate
            if pre is not None:
                self.m_tree.InsertItem(p, pre, obj.label,
                    obj.bitmap_index, obj.bitmap_index, obj)
                if hasattr(obj, 'bitmap_open_index'):
                    self.m_tree.SetItemImage(obj,
                        obj.bitmap_open_index, wx.TreeItemIcon_Expanded)
                    self.m_tree.SetItemImage(obj,
                        obj.bitmap_open_index, wx.TreeItemIcon_SelectedExpanded)
                if type(obj) is model.cc.Constructor:
                    self.m_tree.SetItemBold(obj, bold=obj.IsPreferred())
                elif type(obj) in [model.py.Module, model.py.Package]:
                    self.m_tree.SetItemBold(obj, bold=obj._entry)
                return
        itemCount = 0
        citem, cookie = self.m_tree.GetFirstChild(p)
        if type(citem) is wx.TreeItemId:
            citem = self.m_tree.__fer__(citem)
        if type(citem) in treeOrder:
            if ti <= treeOrder.index(type(citem)):
                self.m_tree.PrependItem(p, obj.label,
                     obj.bitmap_index, obj.bitmap_index, obj)
                if hasattr(obj, 'bitmap_open_index'):
                    self.m_tree.SetItemImage(obj,
                        obj.bitmap_open_index, wx.TreeItemIcon_Expanded)
                    self.m_tree.SetItemImage(obj,
                        obj.bitmap_open_index, wx.TreeItemIcon_SelectedExpanded)
                if type(obj) is model.cc.Constructor:
                    self.m_tree.SetItemBold(obj, bold=obj.IsPreferred())
                elif type(obj) in [model.py.Module, model.py.Package]:
                    self.m_tree.SetItemBold(obj, bold=obj._entry)
                return
        while type(citem) is not wx.TreeItemId or citem.IsOk():
            itemCount = itemCount + 1
            citem, cookie = self.m_tree.GetNextChild(p, cookie)
            if type(citem) not in treeOrder:
                continue
            if ti <= treeOrder.index(type(citem)):
                self.m_tree.InsertItemBefore(p, itemCount,
                     obj.label,
                     obj.bitmap_index, obj.bitmap_index, data=obj)
                if hasattr(obj, 'bitmap_open_index'):
                    self.m_tree.SetItemImage(obj,
                        obj.bitmap_open_index, wx.TreeItemIcon_Expanded)
                    self.m_tree.SetItemImage(obj,
                        obj.bitmap_open_index,
                        wx.TreeItemIcon_SelectedExpanded)
                if type(obj) is model.cc.Constructor:
                    self.m_tree.SetItemBold(obj, bold=obj.IsPreferred())
                elif type(obj) in [model.py.Module, model.py.Package]:
                    self.m_tree.SetItemBold(obj, bold=obj._entry)
                return
        #Ok, do apppend
        self.m_tree.AppendItem(p, obj.label, obj.bitmap_index,
            obj.bitmap_index, obj)
        if hasattr(obj, 'bitmap_open_index'):
            self.m_tree.SetItemImage(obj,
                obj.bitmap_open_index, wx.TreeItemIcon_Expanded)
            self.m_tree.SetItemImage(obj, obj.bitmap_open_index,
                wx.TreeItemIcon_SelectedExpanded)
        if type(obj) is model.cc.Constructor:
            self.m_tree.SetItemBold(obj, bold=obj.IsPreferred())
        elif type(obj) in [model.py.Module, model.py.Package]:
            self.m_tree.SetItemBold(obj, bold=obj._entry)

    def UpdateElement(self, obj):
        """Update the tree label for a object"""
        if not self.m_tree.HoldsObject(obj):
            return
        self.m_tree.SetItemText(obj, obj.label)
        self.m_tree.SetItemImage(obj,
            obj.bitmap_index, wx.TreeItemIcon_Normal)
        if hasattr(obj, 'bitmap_open_index'):
            self.m_tree.SetItemImage(obj,
                obj.bitmap_open_index, wx.TreeItemIcon_Expanded)
            self.m_tree.SetItemImage(obj,
                obj.bitmap_open_index, wx.TreeItemIcon_SelectedExpanded)
        self.m_tree.SetItemImage(obj,
            obj.bitmap_index, wx.TreeItemIcon_Selected)
        if type(obj) is model.cc.Constructor:
            self.m_tree.SetItemBold(obj, bold=obj.IsPreferred())
        elif type(obj) in [model.py.Module, model.py.Package]:
            self.m_tree.SetItemBold(obj, bold=obj._entry)

    def OnUpdateAddFiles(self, event):
        """Update event handler"""
        event.Enable(bool(self.selected and self.selected.project))

    @tran.TransactionalMethod('add new file {0}')
    @wxx.CreationDialog(dlg.NewFile, model.arch.File)
    def OnAddFiles(self, event):
        """Event handler"""
        args = [model.arch.Dir, model.Project]
        return (context.frame, self.selected.inner(args))

    def OnUpdateAddDir(self, event):
        """Update event handler"""
        event.Enable(bool(self.selected and self.selected.project))

    @tran.TransactionalMethod('add new dir {0}')
    @wxx.CreationDialog(dlg.NewDir, model.arch.Dir)
    def OnAddDir(self, event):
        """Event handler"""
        container = self.selected.inner(model.arch.Dir)
        if not container:
            container = self.selected.project
        return (context.frame, container)

    def OnRefreshAllFiles(self, event):
        """Event handler for refreshing all files"""
        if self.selected:
            t = type(self.selected)
            if t is model.Workspace:
                self.RefreshAllFiles()
            else:
                self.selected.project.RefreshProjectFiles()
        else:
            self.RefreshAllFiles()

    @tran.TransactionalMethod('refresh all files')
    def RefreshAllFiles(self):
        """Refresh all the files"""
        theApp = context.app
        for wrk in theApp.workspaces:
            self.RefreshWorkspaceFiles(wrk)
        return True

    def RefreshWorkspaceFiles(self, _workspace):
        """Refresh the files contained in a single workspace"""
        for prj in _workspace(model.Project):
            prj.RefreshProjectFiles()

    def OnTreeSelChanged(self, event):
        """Called when tree selection changes"""
        sel = self.m_tree.GetSelection()
        self.selected = (type(sel) is not wx.TreeItemId and sel) or None

    def DoRenderRemoveElement(self, obj):
        """Do remove element in tree"""
        if self.m_tree.HoldsObject(obj):
            self.m_tree.Delete(obj)

    @tran.TransactionalMethod('delete')
    def OnDelete(self, event):
        """delete element"""
        import tran.TransactionStack as stack
        obj = self.selected
        if type(obj) is model.arch.Dir:
            stack.instance.SetName('delete dir {0}'.format(obj.name))
        elif type(obj) is model.arch.File:
            stack.instance.SetName('delete file {0}'.format(obj.name))
        obj.Delete()
        return True

    def TreeLeftKey(self, event):
        """If the selected node is expanded, simply collapse it.
        If not, navigate through parent"""
        if not self.selected:
            return
        if self.m_tree.IsExpanded(self.selected):
            self.m_tree.Collapse(self.selected)
        else:
            parent = self.selected.parent
            if self.m_tree.HoldsObject(parent):
                self.m_tree.SelectItem(parent)

    def OnTreeMenu(self, event):
        """Handles context tree popup menu"""
        (item, where) = self.m_tree.HitTest(event.GetPosition())
        if item is None:
            return
        self.m_tree.SelectItem(item)
        obj = self.selected
        if obj is None:
            return
        menu = wx.Menu()
        menu.Append(app.ID_EDIT_OPEN, "open editor", "Edit file.")
        # add elements filtering disabled
        app.ui.clone_mnu(self._menu, parent=menu, enabled=True)
        menu.AppendSeparator()
        app.ui.append_menuitem_copy(menu, self.frame.editProperties)
        self.PopupMenu(menu, event.GetPosition())
        menu.Destroy()

    def OnTreeOpenFile(self, event):
        """Handle open file"""
        obj = self.selected
        if obj is None or type(obj) is not model.arch.File:
            return
        if hasattr(obj, '_pane') and obj._pane is not None:
            try:
                self.frame.docBook.SetSelection(
                    self.frame.docBook.GetPageIndex(obj._pane))
                return
            except:
                print "spureus _pane reference detected"
                del obj._pane
        frame = context.frame
        # get the appropiated editor
        stat = os.stat(obj.abs_file)
        if stat.st_size > 0:
            access = os.access(obj.abs_file, os.R_OK)
        else:
            access = os.access(obj.abs_file, os.W_OK)
        if not access:
            wx.MessageBox("The file is not readable", "Error",
                wx.OK | wx.CENTER | wx.ICON_ERROR, context.frame)
            return
        if re.match(r"(.)*\.cpp$", obj._file) or re.match(r"(.)*\.h$", obj._file):
            frame.OpenDoc(pane.FilePane, obj)
            return
        if re.match(r"(.)*\.py$", obj._file):
            frame.OpenDoc(pane.FilePythonPane, obj)
            return
        if re.match(r"(.)*\.txt$", obj._file):
            frame.OpenDoc(pane.TextPane, obj)
            return
        try:
            if not obj.is_binary:
                frame.OpenDoc(pane.TextPane, obj)
        except:
            pass

    def OnUpdateEditProperties(self, event):
        """"""
        event.Enable(False)

    def OnEditProperties(self, event):
        """"""
        pass

    def OnUpdateDelete(self, event):
        """"""
        if hasattr(self, '_dbg_session'):
            event.Enable(False)
        elif self.selected:
            if self.selected._readOnly:
                event.Enable(False)
                return
            t = type(self.selected)
            if t is model.arch.File:
                event.Enable(True)
                return
            if t is not model.arch.Dir:
                event.Enable(False)
                return
            if any(x for x in self.selected(model.arch.File,
                model.arch.Dir) if x._readOnly):
                event.Enable(False)
                return
            event.Enable(True)
        else:
            event.Enable(False)

    def OnUpdateRunFile(self, event):
        """default event handler"""
        if not hasattr(self.frame, '_runProcess'):
            obj = self.selected
            event.Enable(bool(obj and type(obj) is model.arch.File
                and re.match(r"(.)*\.py", obj.abs_file)))
        else:
            event.Enable(False)

    def OnUpdateToggleBreakpoint(self, event):
        """Update toggle"""
        book = self.frame.docBook
        if book.GetPageCount():
            page = book.GetCurrentPage()
            if type(page) in [pane.FilePane, pane.FilePythonPane]:
                event.Enable(True)
                event.Check(page.breakpoint)
                return
        event.Enable(False)

    def OnToggleBreakpoint(self, event):
        """Toggle breakpoint"""
        book = self.frame.docBook
        if not book.GetPageCount():
            return
        page = book.GetCurrentPage()
        if type(page) not in [pane.FilePane, pane.FilePythonPane]:
            return
        line = page.line
        page.ToggleBreakpoint(event)
        if hasattr(self, '_dbg_session'):
            pfile = page._object
            if page.breakpoint:
                cmd = 'break {source_file}:{bp}'.format(source_file=pfile._file, bp=line + 1)
                self._dbg_session.send_command(cmd)
            else:
                # This is ugly but my time is small.
                # we must do it better ... pending
                self._dbg_session.send_command('delete')
                self.UpdateBreakpoins()
            self._dbg_session.send_command('info break')

    def OnUpdateDebugFile(self, event):
        """default event handler"""
        if hasattr(self, '_dbg_session'):
            event.Enable(False)
        else:
            obj = self.selected
            event.Enable(bool(obj and type(obj) is model.arch.File
                and re.match(r"(.)*\.py", obj._file)))

    def OnDebugEvent(self, event):
        """handle debugger events dispatched from client"""
        if event.wich == wxx.USER_COMMAND_RESPONSE:
            if hasattr(self, '_dbg_session'):
                response = event.message
                self._dbg_session.UpdateDebugCommandUI(response)
        elif event.wich == wxx.FILE_LINE_INFO:
            path, line = event.message
            self.OpenPythonFileLine(path, line)
        elif event.wich == wxx.UNKNOWN_DEBUG_INFO:
            pass
        elif event.wich == wxx.DEBUG_ENDED:
            if hasattr(self, '_dbg_session'):
                self._dbg_session.deactivateUI()
                del self._dbg_session
            # restore editors
            for i in range(0, self.frame.docBook.GetPageCount()):
                pane = self.frame.docBook.GetPage(i)
                if hasattr(pane, 'RestoreReadOnly'):
                    pane.RestoreReadOnly()
        elif event.wich == wxx.UPDATE_THREADS_INFO:
            if hasattr(self, '_dbg_session'):
                self._dbg_session.UpdateThreadsUI()
        elif event.wich == wxx.UPDATE_LOCALS_INFO:
            if hasattr(self, '_dbg_session'):
                self._dbg_session.UpdateLocalsUI()
        elif event.wich == wxx.UPDATE_BREAKPOINTS_INFO:
            if hasattr(self, '_dbg_session'):
                self._dbg_session.UpdateBreakpointsUI()

    def OpenPythonFileLine(self, path, line):
        """Open a file by path"""
        # search the file inside workspaces
        p = os.path.abspath(path)
        for wrk in context.app.workspaces:
            items = wrk(model.arch.File, filter=lambda x: x.abs_file == p)
            if not len(items):
                continue
            # Ordenamos la apertura del fichero
            obj = items[0]
            if hasattr(obj, '_pane') and obj._pane is not None:
                self.frame.docBook.SetSelection(
                    self.frame.docBook.GetPageIndex(obj._pane))
            else:
                self.frame.OpenDoc(pane.FilePythonPane, obj)
            obj._pane.SetReadOnly(True)
            obj._pane.GotoLine(line - 1, True)
            return True
        return False

    def OnBuildProject(self, event):
        """Update build project"""
        # before build, save first!
        book = self.frame.docBook
        n = book.GetPageCount()
        for pane in [book.GetPage(i) for i in range(0, n)]:
            try:
                if pane.object.project is self.selected:
                    pane.Commit()
            except:
                pass
        build(self.selected.project)

    def OnUpdateDebugProject(self, event):
        """Update the run project button"""
        if hasattr(self, '_dbg_session'):
            event.Enable(False)
        else:
            v = self.selected
            if v and hasattr(v, 'project'):
                v = v.project
                if v and v._language == 'python' and v.main_file:
                    v = v.main_file
                    event.Enable(os.path.exists(v.key_file))
                    return
        event.Enable(False)

    def OnDebugProject(self, event):
        """default event handler"""
        # before running, save first!
        book = self.frame.docBook
        n = book.GetPageCount()
        for pane in [book.GetPage(i) for i in range(0, n)]:
            try:
                if pane.object.project is self.selected:
                    pane.Commit()
            except:
                pass
        self._dbg_session = debugPythonSession(self.selected.project.main_file.key_file)
        self.UpdateBreakpoins()
        self._dbg_session.send_command('info line')
        self._dbg_session.send_command('info threads verbose')
        self._dbg_session.send_command('pp locals()')
        self._dbg_session.send_command('info break')

    def OnDebugFile(self, event):
        """default event handler"""
        # before running, save first!
        if hasattr(self.selected, '_pane') and self.selected._pane:
            self.selected._pane.Commit()
        self._dbg_session = debugPythonSession(self.selected.abs_file)
        self.UpdateBreakpoins()
        self._dbg_session.send_command('info line')
        self._dbg_session.send_command('info threads verbose')
        self._dbg_session.send_command('pp locals()')
        self._dbg_session.send_command('info break')

    def OnUpdateDebugContinue(self, event):
        """default event handler"""
        if hasattr(self, '_dbg_session'):
            event.Enable(self._dbg_session._stepping)
        else:
            event.Enable(False)

    def OnDebugContinue(self, event):
        """default event handler"""
        self._dbg_session.send_command('continue')
        # post standard commands for finish or bp
        self._dbg_session.send_command('info line')
        self._dbg_session.send_command('info threads verbose')
        self._dbg_session.send_command('pp locals()')

    def OnUpdateDebugStepOver(self, event):
        """default event handler"""
        if hasattr(self, '_dbg_session'):
            event.Enable(self._dbg_session._stepping)
        else:
            event.Enable(False)

    def OnDebugStepOver(self, event):
        """default event handler"""
        self._dbg_session.send_command('next')
        self._dbg_session.send_command('info line')
        self._dbg_session.send_command('info threads verbose')
        self._dbg_session.send_command('pp locals()')

    def OnUpdateDebugStepInto(self, event):
        """Update debug stop"""
        if hasattr(self, '_dbg_session'):
            event.Enable(self._dbg_session._stepping)
        else:
            event.Enable(False)

    def OnDebugStepInto(self, event):
        """default event handler"""
        self._dbg_session.send_command('step')
        self._dbg_session.send_command('info line')
        self._dbg_session.send_command('info threads verbose')
        self._dbg_session.send_command('pp locals()')

    def OnUpdateDebugStepOut(self, event):
        """Update debug stop"""
        if hasattr(self, '_dbg_session'):
            event.Enable(self._dbg_session._stepping)
        else:
            event.Enable(False)

    def OnDebugStepOut(self, event):
        """default event handler"""
        self._dbg_session.send_command('frame 0')
        self._dbg_session.send_command('finish')
        self._dbg_session.send_command('info line')
        self._dbg_session.send_command('info threads verbose')
        self._dbg_session.send_command('pp locals()')

    def OnDebugStop(self, event):
        """default event handler"""
        if self._dbg_session._stepping:
            self._dbg_session.send_command('quit')
        else:
            self._dbg_session.force_stop()

    def UpdateBreakpoins(self):
        """Update the brekpoints in the debugger"""
        if not hasattr(self, '_dbg_session'):
            return
        if not self.selected:
            return
        project = self.selected.project
        pfiles = project(model.arch.File)
        for pfile in pfiles:
            for bp in project.breakpoints(pfile):
                cmd = 'break {source_file}:{bp}'.format(source_file=pfile._file, bp=bp + 1)
                self._dbg_session.send_command(cmd)

    def OnUpdateDebugStop(self, event):
        """Update debug stop"""
        event.Enable(hasattr(self, '_dbg_session'))

    def OnRunFile(self, event):
        """default event handler"""
        # before running, save first!
        if hasattr(self.selected, '_pane') and self.selected._pane:
            self.selected._pane.Commit()
        self.frame.RunPythonScript(self.selected.abs_file)

    def OnUpdateStopRun(self, event):
        """default event handler"""
        event.Enable(hasattr(self.frame, '_runProcess'))

    def OnStopRun(self, event):
        """Stop running"""
        self.frame.StopRunning()

    def OnUpdateRunProject(self, event):
        """Update the run project button"""
        if not hasattr(self.frame, '_runProcess'):
            v = self.selected
            if v and hasattr(v, 'project'):
                v = v.project
                if v and v._language == 'python' and v.main_file:
                    v = v.main_file
                    event.Enable(os.path.exists(v.key_file))
                    return
        event.Enable(False)

    def OnRunProject(self, event):
        """default event handler"""
        # before running, save first!
        path = self.selected.project.main_file.key_file
        book = self.frame.docBook
        n = book.GetPageCount()
        for pane in [book.GetPage(i) for i in range(0, n)]:
            try:
                if pane.object.project is self.selected:
                    pane.Commit()
            except:
                pass
        self.frame.RunPythonScript(path)

