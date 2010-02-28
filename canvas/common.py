import wx
from display import Process, Network, ChanEnd, Channel
from util import AttrDict

# Pickle
try:
    import cPickle as pickle
except ImportError:
    import pickle

# Logging
import logging
log = logging.getLogger("popedLogger");

class CanvasFrame (wx.Frame):
    def __init__ (self, parent):
        wx.Frame.__init__(self, parent, -1, "Process Canvas", size=(800,600))
        self._panel = CanvasPanel(self)

    def get_panel(self): return self._panel
    panel = property(get_panel)

class CanvasPanel (wx.Panel):
    def __init__ (self, frame):
        wx.Panel.__init__(self, frame, -1)
        # Properties
        self._network = Network(x=0, y=0) # Root network.

        self._selected = None
        self._chan_start_point = None

        # Events
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)

        # Allow drop.
        self.SetDropTarget(CanvasDropTarget(self))

        self.style = AttrDict(
            background = (175, 175, 175)
        )

    def get_network(self): return self._network
    def set_network(self, n): self._network = n
    network = property(get_network, set_network)

    def on_paint (self, event):
        dc = wx.PaintDC(self)
        try:
            gc = wx.GraphicsContext.Create(dc)
        except NotImplementedError:
            print "GraphicsContext not supported here"
            return
        # Drawing
        self.draw_background(gc)
        if self._network:
            self._network.on_paint(gc)
        else:
            print "No network"
    
    def on_motion (self, event):
        if self._selected is not None:
            # Get all of the click data.
            hit = self._selected
            p = hit['hit']
            p.on_motion(event, hit['transform'], hit['offset'])
            self.Refresh()

    def on_left_down (self, event):
        selection = self._network.hit_test(event.X, event.Y)
        print "Result of hit test was %s" % selection
        if selection is not None:
            self._selected = selection
    
    def on_left_up (self, event):
        if self._selected:
            if isinstance(self._selected['hit'], ChanEnd):
                print "Selected a channel end"
                if self._chan_start_point is not None:
                    if self._chan_start_point.datatype == self._selected['hit'].datatype:
                        # Types match, work out which way round the channel is.
                        print "Creating a channel."
                        if self._chan_start_point.direction == 'output':
                            src = self._chan_start_point
                            dest = self._selected['hit']
                        else:
                            src = self._selected['hit']
                            dest = self._chan_start_point
                        self._network.add_channel(Channel('bar', src.datatype, src, dest))
                        self._chan_start_point = None
                        self.Refresh()
                    else:
                        # Types don't match, abort.
                        print "Channel types don't match. Cancelling selection"
                        self._chan_start_point = None
                else:
                    # No ends currently selected, start a chan creation op.
                    print "In channel creation mode"
                    self._chan_start_point = self._selected['hit']
            # Cancel out the current selection.
            self._selected = None

    def draw_background(self, gc):
        (w, h) = self.GetSize()
        path = gc.CreatePath()
        path.AddRectangle(0, 0, w, h)
        brush = gc.CreateBrush(wx.Brush(self.style.background))
        gc.SetBrush(brush)
        gc.DrawPath(path)

class CanvasDropTarget(wx.PyDropTarget):
    def __init__(self, canvas):
        wx.PyDropTarget.__init__(self)
        self.drop_data = BlockDropData()
        self.SetDataObject(self.drop_data)
        self.canvas = canvas

    def OnDrop (self, x, y): pass
    def OnEnter(self, x, y, d): return d
    def OnLeave(self): pass
    def OnDrop(self, x, y): pass
    def OnDragOver(self, x, y, d): return d

    def OnData (self, x, y, d):
        if self.GetData():
            data = self.drop_data.GetDataHere()
            data = pickle.loads(data)
            print "The pickled data is %s" % data
            print "Name should be %s" % data['name']

            for c in data['input']:
                c['direction'] = 'input'
            for c in data['output']:
                c['direction'] = 'output'
            chan_ends = data['input'] + data['output']

            canvas = self.canvas
            p = Process (x, y, data['name'])
            p.add_chan_ends(chan_ends)
            log.debug("Adding process: %s, %s, %s", data['name'], data['input'], data['output'])
            canvas.network.add_process(p)
            canvas.Refresh()
            #self.diagram.GetCanvas().Refresh()
        log.debug("Completed OnData for Canvas droptarget.")
        return d

class BlockDropData(wx.PyDataObjectSimple):
    def __init__(self):
        wx.PyDataObjectSimple.__init__(self, wx.CustomDataFormat('BlockData'))

    def GetDataSize(self):
        return len(self.data)

    def GetDataHere(self):
        return self.data

    def SetData(self, data):
        self.data = data
        return True
