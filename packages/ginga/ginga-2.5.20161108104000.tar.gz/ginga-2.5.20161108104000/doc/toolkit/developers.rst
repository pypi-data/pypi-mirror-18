.. _ch-programming-ginga:

+++++++++++++++++++++++++++++++++
Developing with the Ginga Toolkit
+++++++++++++++++++++++++++++++++

* :ref:`modindex`

=========================================================================
Example: Using Ginga Components to Build a Simple Standalone Image Viewer
=========================================================================

First, let's take a look at how to use the "bare" Ginga rending class
by itself.  Ginga basically follows the Model-View-Controller (MVC)
design pattern, that is described in more detail in
the :ref:`chapter on internals <ch-programming-internals>`.
The "view" classes are rooted in the base class ``ImageView``.
Ginga supports backends for different widget sets through various
subclasses of this class.   

Typically, a developer picks a GUI toolkit that has a supported backend
(Gtk, Qt, Tk, Matplotlib) and writes a GUI program using that widget set
with the typical Python toolkit bindings and API.  Where they want a 
image view pane they instantiate the appropriate subclass of 
``ImageView``, and using the  ``get_widget()`` call extract the native
widget and insert it into the GUI layout.  A reference should be kept to
the view object.

Ginga does not create any additional GUI components beyond the image
pane itself, however it does provide a standard set of keyboard and
mouse bindings on the widget that can be enabled, disabled or changed.
The user interface bindings are configurable via a pluggable
``Bindings`` class which constitutes the "controller" part of the MVC
design.  There are a plethora of callbacks that can be registered,
allowing the user to create their own custom user interface for
manipulating the view.   

.. _fig1:
.. figure:: figures/barebonesviewer_qt.png
   :scale: 100%
   :figclass: h

   A simple, "bare bones" FITS viewer written in Qt.  

Listing 1 shows a code listing for a simple graphical FITS
viewer built using the subclass ``ImageViewZoom`` from the module
``ginga.qtw`` (screenshot in Figure :ref:`fig1`) written in around 100
or so lines of Python.  It creates a window containing an image view and
two buttons.  This example, included with the Ginga source (look in the
``examples`` directory), will open FITS files dragged and dropped on the 
image window or via a dialog popped up when clicking the "Open File"
button.   

.. code-block:: python


we create a ``ImageViewZoom`` object.  On this object we enable automatic
cut levels (using the 'zscale' algorithm), configure it to auto zoom the
image to fit the window and set a callback function for files dropped on
the window.  We extract the user-interface bindings with
``get_bindings()``, and on this object enable standard user interactive
controls for panning, zooming, cut levels, simple transformations (flip
x/y and swap axes), rotation and color map warping.
We then extract the platform-specific widget (Qt-based, in this case) using
``get_widget()`` and pack it into a Qt container along with a couple of
buttons to complete the viewer. 

Scanning down the code a bit, we can see that whether by dragging and
dropping or via the click to open, we ultimately call the load_file()
method to get the data into the viewer.  As shown, load_file creates 
an AstroImage object (the "model" part of our MVC design).  It then
passes this object to the viewer via the set_image() method.  
AstroImage objects have methods for ingesting data via a file path, an
``Astropy``/``pyfits`` HDU or a bare ``Numpy`` data array. 

Many of these sorts of examples are contained in the ``examples``
directory in the source distribution.  Look for files with names
matching example*_*.py

.. _sec-plotting:

Graphics plotting with Ginga
----------------------------

.. _fig2:
.. figure:: figures/example2_screenshot.png
   :scale: 100%
   :figclass: h

   An example of a ``ImageViewCanvas`` widget with graphical overlay. 

For each supported widget set there is a subclass of ImageViewZoom called
``ImageViewCanvas`` (an example is shown in Figure :ref:`fig2`).
This class adds scalable object plotting on top of the image view plane.
A variety of simple graphical shapes are available,
including lines, circles, rectangles, points, polygons, text, rulers,
compasses, etc.  Plotted objects scale, transform and rotate seamlessly
with the image. 

See the scripts prefaced with "example2" (under the "examples"
directory) in the package source for details.  

Rendering into Matplotlib Figures
---------------------------------

Ginga can also render directly into a Matplotlib Figure, which opens up
interesting possibilities for overplotting beyond the limited
capabilities of the ``ImageViewCanvas`` class.  In short,
this allows you to have all the interactive UI goodness of a Ginga widget
in a matplotlib figure.  You can interactively flip, rotate, pan, zoom,
set cut levels and color map warp a FITS image.  Furthermore, you can plot
using matplotlib plotting on top of the image and the plots will follow all
the transformations.  The interactive performance is not quite as speedy
as with the other toolkit backends, but quite usable.

Look at the examples in `examples/matplotlib`, especially `example4_mpl.py`.


