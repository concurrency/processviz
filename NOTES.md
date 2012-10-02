# Notes

I'm going to record a few notes as I go.

## Setup

First, I setup Python, wxmac, and a few other things using 'brew'. This took no small amount of doing... but, eventually, I eliminated the problems I was having and was able to run the app.

## Errors

Running the app produces errors:

serafina:processviz jadudm$ python builder.py 
2012-10-01 21:45:37,307 - Processes - DEBUG - Apple Mac OS X with Python 2.7.3 (default, Oct  1 2012, 21:06:14) 
[GCC 4.2.1 Compatible Apple Clang 4.0 ((tags/Apple/clang-421.0.60))], wxPython 2.9.4.0 osx-cocoa (classic)
2012-10-01 21:45:37,307 - Processes - DEBUG - Initialising frame
2012-10-01 21:45:37,380 - Processes - DEBUG - Finished initialising main wxFrame and AUIManager panes.
swig/python detected a memory leak of type 'wxPlatformInfo *', no destructor found.
Traceback (most recent call last):
  File "/Users/jadudm/git/concurrency/processviz/constructor/processes.py", line 139, in BlockChanged
    self.toolbox.GetSelection()).GetData())
AttributeError: 'NoneType' object has no attribute 'GetData'
2012-10-01 21:45:56.880 Python[14764:f07] -_continuousScroll is deprecated for NSScrollWheel. Please use -hasPreciseScrollingDeltas.
2012-10-01 21:45:56.880 Python[14764:f07] -deviceDeltaX is deprecated for NSScrollWheel. Please use -scrollingDeltaX.
2012-10-01 21:45:56.881 Python[14764:f07] -deviceDeltaY is deprecated for NSScrollWheel. Please use -scrollingDeltaY.

It looks like the GUI is not rendering fully... dragging blocks out does not do anything. There's only a small square (which looks wrong), and the canvas itself seems too small (a small, 64x64ish square in the upper-left corner of the window). 

I'll have to dig into this later... it seems like this might be a nice replacement for the browser-based "Flow" that I have been using.


