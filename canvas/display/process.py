import model
from util import AttrDict

class Process (model.Process):
    def __init__ (self, x, y, name, params, input_chans=[], output_chans=[], sub_network=None):
        model.Process.__init__(self, name, params, input_chans, output_chans, sub_network)
        self._x, self._y = x, y
        
        # Process style, will end up in YAML at some point.
        self.style = AttrDict (
            top             = (202, 214, 234),
            bottom          = (172, 192, 216),
            bottom_hi       = (255,255,255),
            shadow          = (218, 230, 242),
            s_offset        = 5,
            border          = ( 76,  76,  85),
            text            = ( 44,  48,  52),
            v_pad           = 10,               # Vertical padding
            h_pad           = 10,               # Horizontal padding
            lbl_pad         = 2,                # Label padding
            cend_r          = 4.5,              # Radius of channel end.
            main_label      = 13,               # Font size of main label
            end_pad         = 5,
            expander_size   = 6,                # Expander widget size.
            expander_offset = 7,
        )

    def get_x (self): return self._x
    def set_x (self, x): self._x = x
    x = property(get_x, set_x)

    def get_y (self): return self._y
    def set_y (self, y): self._y = y
    y = property(get_y, set_y)
    
    def get_bounds (self):
        (w, h) = get_size()
        return (x, y, x + w, y + h)
    
    def get_size (self):
        (w, h) = get_name_size()
        return (w, h)

    def get_name_size (self):
        # Calculate size of process name & add outer padding.
        gc.SetFont(gc.CreateFont(wx.Font(pointSize=style['main_label'], family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL), style['text']))
        (w, h) = gc.GetTextExtent(self.name)
        w += (self.style.h_pad * 2)
        h += (self.style.v_pad * 2)
        return (w, h)