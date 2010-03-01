# poped.py
# Part of POPed

import sys
import wx, wx.aui, wx.html

try:
    import cPickle as pickle
except ImportError:
    import pickle

import logging
log = logging.getLogger("popedLogger");


# Pieces of POPed
from Config import Config
from BlockSource import BlockSource
#from OGLProcessDiagram import ProcessDiagram, BlockDropData

from canvas.common import CanvasPanel, BlockDropData

from Templates import renderTemplate

class Frame(wx.Frame):
    def __init__(self, parent, id=-1, title="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER | wx.CLIP_CHILDREN):
        pi = wx.PlatformInformation()
        log.debug("%s with Python %s, wxPython %s"%(pi.GetOperatingSystemIdName(), sys.version ,wx.version()))
        log.debug("Initialising frame")
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        # Menu bars
        mb = wx.MenuBar()

        # File Menu
        file_menu = wx.Menu()
        open_item = file_menu.Append(-1, "&Open\tCtrl-O", "Load a saved network file")
        save_item = file_menu.Append(-1, "&Save\tCtrl-S", "Save this network")
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, "Exit")

        # Compose menu bar.
        mb.Append(file_menu, "File")

        # Accelerators
        accelerator_table = wx.AcceleratorTable( [
            (wx.ACCEL_CTRL, ord('O'), open_item.GetId()),
            (wx.ACCEL_CTRL, ord('S'), save_item.GetId())
        ])
        self.SetAcceleratorTable(accelerator_table)

        self.SetMenuBar(mb)

        # Panes
        self.info = info = self.CreateInfoPanel()
        self._mgr.AddPane(info, wx.BOTTOM, 'Information')

        # Diagram
        diagram = CanvasPanel(self)
        self._mgr.AddPane(diagram, wx.CENTER)

        # Toolbox
        toolbox = self.toolbox = self.CreateToolbox()
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.StartToolboxDrag)
        self._mgr.AddPane(toolbox, wx.LEFT, 'Toolbox')

        # Commit updates
        self._mgr.Update()

        # Events
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_open_item, open_item)
        self.Bind(wx.EVT_MENU, self.on_save_item, save_item)

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.BlockChanged)
        log.debug("Finished initialising main wxFrame and AUIManager panes.")

    def on_open_item (self, event):
        print "Open"

    def on_save_item (self, event):
        print "Save"

    def BlockChanged(self, event):
        self.DisplayInfoPage(
                self.toolbox.GetItemData(
                    self.toolbox.GetSelection()).GetData())

    def StartToolboxDrag (self, event):
        #print "Tree is dragging"
        selectedData =\
            self.toolbox.GetItemData(self.toolbox.GetSelection()).GetData()
        if selectedData:
            blockObject = BlockDropData()
            blockObject.SetData(pickle.dumps(selectedData))
            dropSource = wx.DropSource(self.toolbox)
            dropSource.SetData(blockObject)
            dropSource.DoDragDrop(True)

    def OnExit(self, event):
        self.Close()

    def CreateToolbox(self):
        tree = wx.TreeCtrl(self, -1, wx.Point(0,0), wx.Size(150,250), wx.TR_DEFAULT_STYLE | wx.NO_BORDER)

        blockSource = BlockSource(Config.systemBlockPath)
        for rootName in blockSource.getRoots():
            root = tree.AddRoot(rootName)
            for block in blockSource.getBlocks(rootName):
                itemId = tree.AppendItem(root, block['name'], data=wx.TreeItemData(block))
                tree.SetItemPyData(itemId, block)
            tree.Expand(root)
        return tree

    def CreateInfoPanel(self):
        ctrl = wx.html.HtmlWindow(self, -1, wx.DefaultPosition, wx.Size(400,300))
        if "gtk2" in wx.PlatformInfo:
            ctrl.SetStandardFonts()
        ctrl.SetPage(renderTemplate('welcome.mako'))
        return ctrl

    def DisplayInfoPage(self, block):
        #import pprint
        #self.info.SetPage(
                #'<html><body><pre>%s</pre></body></html>' %
                #pprint.pformat(block))
        if block != None:
            self.info.SetPage(renderTemplate('process_info.mako', **block))

