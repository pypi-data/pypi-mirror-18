#
# ImageViewAggGtk.py -- a backend for Ginga using Gtk widgets and Cairo
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.

import sys, os

import numpy

from ginga.gtk3w import GtkHelp
from ginga import Mixins, Bindings, colors

from ginga.canvas.mixins import DrawingMixin, CanvasMixin, CompoundMixin
from ginga.util.toolbox import ModeIndicator

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf
import cairo

moduleHome = os.path.split(sys.modules[__name__].__file__)[0]
icon_dir = os.path.abspath(os.path.join(moduleHome, '..', 'icons'))

try:
    # See if we have aggdraw module--best choice
    from ginga.aggw.ImageViewAgg import ImageViewAgg as ImageView, \
         ImageViewAggError as ImageViewError

except ImportError:
    try:
        # No, hmm..ok, see if we have PIL module...
        from ginga.pilw.ImageViewPil import ImageViewPil as ImageView, \
             ImageViewPilError as ImageViewError

    except ImportError:
        try:
            # No dice. How about the OpenCv module?
            from ginga.cvw.ImageViewCv import ImageViewCv as ImageView, \
                 ImageViewCvError as ImageViewError

        except ImportError:
            # Fall back to mock--there will be no graphic overlays
            from ginga.mockw.ImageViewMock import ImageViewMock as ImageView, \
                 ImageViewMockError as ImageViewError


class ImageViewGtkError(ImageViewError):
    pass

class ImageViewGtk(ImageView):

    def __init__(self, logger=None, rgbmap=None, settings=None):
        ImageView.__init__(self, logger=logger,
                           rgbmap=rgbmap,
                           settings=settings)

        imgwin = Gtk.DrawingArea()
        imgwin.connect("draw", self.draw_event)
        imgwin.connect("configure-event", self.configure_event)
        imgwin.set_events(Gdk.EventMask.EXPOSURE_MASK)
        # prevents some flickering
        imgwin.set_double_buffered(True)
        imgwin.set_app_paintable(True)
        # prevents extra redraws, because we manually redraw on a size
        # change
        imgwin.set_redraw_on_allocate(False)
        self.imgwin = imgwin
        self.imgwin.show_all()

        # cursors
        self.cursor = {}

        # see reschedule_redraw() method
        self._defer_task = None
        self.msgtask = None


    def get_widget(self):
        return self.imgwin

    def get_image_as_pixbuf(self):
        arr = self.getwin_array(order='RGB')
        pixbuf = GtkHelp.pixbuf_new_from_array(arr,
                                               GdkPixbuf.Colorspace.RGB,
                                               8)
        return pixbuf

    def get_image_as_widget(self):
        """Used for generating thumbnails.  Does not include overlaid
        graphics.
        """
        pixbuf = self.get_image_as_pixbuf()
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        image.show()
        return image

    def save_image_as_file(self, filepath, format='png', quality=90):
        """Used for generating thumbnails.  Does not include overlaid
        graphics.
        """
        pixbuf = self.get_image_as_pixbuf()
        options, values = [], []
        if format == 'jpeg':
            options.append('quality')
            values.append(str(quality))
        pixbuf.savev(filepath, format, options, values)

    def get_rgb_image_as_pixbuf(self):
        dawd = self.surface.get_width()
        daht = self.surface.get_height()
        rgb_buf = bytes(self.surface.get_data())
        pixbuf = GtkHelp.pixbuf_new_from_data(rgb_buf, GdkPixbuf.Colorspace.RGB,
                                      False, 8, dawd, daht, dawd*3)

        return pixbuf

    def save_rgb_image_as_file(self, filepath, format='png', quality=90):
        pixbuf = self.get_rgb_image_as_pixbuf()
        options = {}
        if format == 'jpeg':
            options['quality'] = str(quality)
        pixbuf.save(filepath, format, options)

    def reschedule_redraw(self, time_sec):
        time_ms = int(time_sec * 1000)
        try:
            if self._defer_task is not None:
                GObject.source_remove(self._defer_task)
                self._defer_task = None
        except:
            pass
        self._defer_task = GObject.timeout_add(time_ms,
                                               self.delayed_redraw_gtk)

    def delayed_redraw_gtk(self):
        self._defer_task = None
        self.delayed_redraw()

    def update_image(self):
        if not self.surface:
            return

        win = self.imgwin.get_window()
        if win is not None and self.surface is not None:
            imgwin_wd, imgwin_ht = self.get_window_size()

            self.imgwin.queue_draw_area(0, 0, imgwin_wd, imgwin_ht)

            # Process expose events right away so window is responsive
            # to scrolling
            win.process_updates(True)


    def draw_event(self, widget, cr):
        self.logger.debug("updating window from surface")

        arr8 = self.get_image_as_array()
        ht, wd = arr8.shape[:2]
        self.logger.debug("got %dx%d RGB image buffer" % (
            wd, ht))

        pixbuf = GtkHelp.pixbuf_new_from_array(arr8,
                                               GdkPixbuf.Colorspace.RGB,
                                               8)

        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        return False

    def configure_window(self, width, height):
        self.configure_surface(width, height)

    def configure_event(self, widget, event):
        rect = widget.get_allocation()
        x, y, width, height = rect.x, rect.y, rect.width, rect.height

        if self.surface is not None:
            # This is a workaround for a strange bug in Gtk 3
            # where we get multiple configure callbacks even though
            # the size hasn't changed.  We avoid creating a new surface
            # if there is an old surface with the exact same size.
            # This prevents some flickering of the display on focus events.
            wwd, wht = self.get_window_size()
            if (wwd == width) and (wht == height):
                return True

        #self.surface = None
        self.logger.debug("allocation is %d,%d %dx%d" % (
            x, y, width, height))
        #width, height = width*2, height*2
        self.configure_window(width, height)
        return True

    def size_request(self, widget, requisition):
        """Callback function to request our desired size.
        """
        requisition.width, requisition.height = self.get_desired_size()
        return True

    def set_cursor(self, cursor):
        win = self.imgwin.get_window()
        if win is not None:
            win.set_cursor(cursor)

    def define_cursor(self, ctype, cursor):
        self.cursor[ctype] = cursor

    def get_cursor(self, ctype):
        return self.cursor[ctype]

    def switch_cursor(self, ctype):
        self.set_cursor(self.cursor[ctype])

    def center_cursor(self):
        if self.imgwin is None:
            return
        win_x, win_y = self.get_center()
        scrn_x, scrn_y = self.imgwin.window.get_origin()
        scrn_x, scrn_y = scrn_x + win_x, scrn_y + win_y

        # set the cursor position
        disp = self.imgwin.window.get_display()
        screen = self.imgwin.window.get_screen()
        disp.warp_pointer(screen, scrn_x, scrn_y)

    def position_cursor(self, data_x, data_y):
        if self.imgwin is None:
            return
        win_x, win_y = self.get_canvas_xy(data_x, data_y)
        scrn_x, scrn_y = self.imgwin.window.get_origin()
        scrn_x, scrn_y = scrn_x + win_x, scrn_y + win_y

        # set the cursor position
        disp = self.imgwin.window.get_display()
        screen = self.imgwin.window.get_screen()
        disp.warp_pointer(screen, scrn_x, scrn_y)

    def _get_rgbbuf(self, data):
        buf = data.tostring(order='C')
        return buf

    def onscreen_message(self, text, delay=None, redraw=True):
        if self.msgtask is not None:
            try:
                GObject.source_remove(self.msgtask)
                self.msgtask = None
            except:
                pass
        self.message = text
        if redraw:
            self.redraw(whence=3)
        if delay:
            ms = int(delay * 1000.0)
            self.msgtask = GObject.timeout_add(ms,
                                               self.clear_onscreen_message_gtk)

    def clear_onscreen_message_gtk(self):
        self.msgtask = None
        self.onscreen_message(None)

class ImageViewEvent(ImageViewGtk):

    def __init__(self, logger=None, rgbmap=None, settings=None):
        ImageViewGtk.__init__(self, logger=logger, rgbmap=rgbmap,
                              settings=settings)

        imgwin = self.imgwin
        imgwin.set_can_focus(True)
        imgwin.connect("map_event", self.map_event)
        imgwin.connect("focus_in_event", self.focus_event, True)
        imgwin.connect("focus_out_event", self.focus_event, False)
        imgwin.connect("enter_notify_event", self.enter_notify_event)
        imgwin.connect("leave_notify_event", self.leave_notify_event)
        imgwin.connect("motion_notify_event", self.motion_notify_event)
        imgwin.connect("button_press_event", self.button_press_event)
        imgwin.connect("button_release_event", self.button_release_event)
        imgwin.connect("key_press_event", self.key_press_event)
        imgwin.connect("key_release_event", self.key_release_event)
        imgwin.connect("scroll_event", self.scroll_event)
        mask = imgwin.get_events()
        imgwin.set_events(mask
                          | Gdk.EventMask.ENTER_NOTIFY_MASK
                          | Gdk.EventMask.LEAVE_NOTIFY_MASK
                          | Gdk.EventMask.FOCUS_CHANGE_MASK
                          | Gdk.EventMask.STRUCTURE_MASK
                          | Gdk.EventMask.BUTTON_PRESS_MASK
                          | Gdk.EventMask.BUTTON_RELEASE_MASK
                          | Gdk.EventMask.KEY_PRESS_MASK
                          | Gdk.EventMask.KEY_RELEASE_MASK
                          | Gdk.EventMask.POINTER_MOTION_MASK
                          | Gdk.EventMask.POINTER_MOTION_HINT_MASK
                          | Gdk.EventMask.SCROLL_MASK)

        # Set up widget as a drag and drop destination
        imgwin.connect("drag-data-received", self.drop_event_cb)
        imgwin.connect("drag-motion", self.drag_motion_cb)
        imgwin.connect("drag-drop", self.drag_drop_cb)
        self.TARGET_TYPE_TEXT = 0
        imgwin.drag_dest_set(Gtk.DestDefaults.ALL, [],
                             Gdk.DragAction.COPY)
        imgwin.drag_dest_add_text_targets()

        # last known window mouse position
        self.last_win_x = 0
        self.last_win_y = 0
        # last known data mouse position
        self.last_data_x = 0
        self.last_data_y = 0
        # Does widget accept focus when mouse enters window
        self.enter_focus = self.t_.get('enter_focus', True)

        # @$%&^(_)*&^ gnome!!
        self._keytbl = {
            'shift_l': 'shift_l',
            'shift_r': 'shift_r',
            'control_l': 'control_l',
            'control_r': 'control_r',
            'alt_l': 'alt_l',
            'alt_r': 'alt_r',
            'super_l': 'super_l',
            'super_r': 'super_r',
            'meta_right': 'meta_right',
            'asciitilde': '~',
            'grave': 'backquote',
            'exclam': '!',
            'at': '@',
            'numbersign': '#',
            'percent': '%',
            'asciicircum': '^',
            'ampersand': '&',
            'asterisk': '*',
            'dollar': '$',
            'parenleft': '(',
            'parenright': ')',
            'underscore': '_',
            'minus': '-',
            'plus': '+',
            'equal': '=',
            'braceleft': '{',
            'braceright': '}',
            'bracketleft': '[',
            'bracketright': ']',
            'bar': '|',
            'colon': ':',
            'semicolon': ';',
            'quotedbl': 'doublequote',
            'apostrophe': 'singlequote',
            'backslash': 'backslash',
            'less': '<',
            'greater': '>',
            'comma': ',',
            'period': '.',
            'question': '?',
            'slash': '/',
            'space': 'space',
            'escape': 'escape',
            'return': 'return',
            'tab': 'tab',
            'f1': 'f1',
            'f2': 'f2',
            'f3': 'f3',
            'f4': 'f4',
            'f5': 'f5',
            'f6': 'f6',
            'f7': 'f7',
            'f8': 'f8',
            'f9': 'f9',
            'f10': 'f10',
            'f11': 'f11',
            'f12': 'f12',
            'right': 'right',
            'left': 'left',
            'up': 'up',
            'down': 'down',
            }

        # Define cursors
        for curname, filename in (('pan', 'openHandCursor.png'),
                               ('pick', 'thinCrossCursor.png')):
            path = os.path.join(icon_dir, filename)
            cur = GtkHelp.make_cursor(self.imgwin, path, 8, 8)
            self.define_cursor(curname, cur)

        for name in ('motion', 'button-press', 'button-release',
                     'key-press', 'key-release', 'drag-drop',
                     'scroll', 'map', 'focus', 'enter', 'leave',
                     ):
            self.enable_callback(name)

    def transkey(self, keyname):
        try:
            return self._keytbl[keyname.lower()]

        except KeyError:
            return keyname

    def get_keyTable(self):
        return self._keytbl

    def set_enter_focus(self, tf):
        self.enter_focus = tf

    def map_event(self, widget, event):
        super(ImageViewZoom, self).configure_event(widget, event)
        return self.make_callback('map')

    def focus_event(self, widget, event, hasFocus):
        return self.make_callback('focus', hasFocus)

    def enter_notify_event(self, widget, event):
        if self.enter_focus:
            widget.grab_focus()
        return self.make_callback('enter')

    def leave_notify_event(self, widget, event):
        self.logger.debug("leaving widget...")
        return self.make_callback('leave')

    def key_press_event(self, widget, event):
        # without this we do not get key release events if the focus
        # changes to another window
        #Gdk.keyboard_grab(widget.get_window(), False, event.time)

        keyname = Gdk.keyval_name(event.keyval)
        keyname = self.transkey(keyname)
        self.logger.debug("key press event, key=%s" % (keyname))
        return self.make_ui_callback('key-press', keyname)

    def key_release_event(self, widget, event):
        #Gdk.keyboard_ungrab(event.time)

        keyname = Gdk.keyval_name(event.keyval)
        keyname = self.transkey(keyname)
        self.logger.debug("key release event, key=%s" % (keyname))
        return self.make_ui_callback('key-release', keyname)

    def button_press_event(self, widget, event):
        # event.button, event.x, event.y
        x = event.x; y = event.y
        button = 0
        if event.button != 0:
            button |= 0x1 << (event.button - 1)
        self.logger.debug("button event at %dx%d, button=%x" % (x, y, button))

        data_x, data_y = self.get_data_xy(x, y)
        return self.make_ui_callback('button-press', button, data_x, data_y)

    def button_release_event(self, widget, event):
        # event.button, event.x, event.y
        x = event.x; y = event.y
        button = 0
        if event.button != 0:
            button |= 0x1 << (event.button - 1)
        self.logger.debug("button release at %dx%d button=%x" % (x, y, button))

        data_x, data_y = self.get_data_xy(x, y)
        return self.make_ui_callback('button-release', button, data_x, data_y)

    def get_last_win_xy(self):
        return (self.last_win_x, self.last_win_y)

    def get_last_data_xy(self):
        return (self.last_data_x, self.last_data_y)

    def motion_notify_event(self, widget, event):
        button = 0
        if event.is_hint:
            tup = event.window.get_pointer()
            xx, x, y, state = tup
        else:
            x, y, state = event.x, event.y, event.state
        self.last_win_x, self.last_win_y = x, y

        if state & Gdk.ModifierType.BUTTON1_MASK:
            button |= 0x1
        elif state & Gdk.ModifierType.BUTTON2_MASK:
            button |= 0x2
        elif state & Gdk.ModifierType.BUTTON3_MASK:
            button |= 0x4
        # self.logger.debug("motion event at %dx%d, button=%x" % (x, y, button))

        data_x, data_y = self.get_data_xy(x, y)
        self.last_data_x, self.last_data_y = data_x, data_y

        return self.make_ui_callback('motion', button, data_x, data_y)

    def scroll_event(self, widget, event):
        # event.button, event.x, event.y
        x = event.x; y = event.y

        degrees, direction = GtkHelp.get_scroll_info(event)
        self.logger.debug("scroll deg=%f direction=%f" % (
            degrees, direction))

        data_x, data_y = self.get_data_xy(x, y)
        self.last_data_x, self.last_data_y = data_x, data_y

        return self.make_ui_callback('scroll', direction, degrees,
                                  data_x, data_y)

    def drag_drop_cb(self, widget, context, x, y, time):
        self.logger.debug('drag_drop_cb')
        # initiates a drop
        success = delete = False
        targets = context.list_targets()
        for mimetype in targets:
            if str(mimetype) in ("text/thumb", "text/plain", "text/uri-list"):
                Gdk.drop_reply(context, True, time)
                success = True
                return True

        self.logger.debug("dropped format type did not match known types")
        Gdk.drop_reply(context, False, time)
        return True

    def drag_motion_cb(self, widget, context, x, y, time):
        self.logger.debug('drag_motion_cb')
        # checks whether a drop is possible
        targets = context.list_targets()
        for mimetype in targets:
            if str(mimetype) in ("text/thumb", "text/plain", "text/uri-list"):
                Gdk.drag_status(context, Gdk.DragAction.COPY, time)
                return True

        Gdk.drag_status(context, 0, time)
        self.logger.debug('drag_motion_cb done')
        return False

    def drop_event_cb(self, widget, context, x, y, selection, info, time):
        self.logger.debug('drop_event')
        if info != self.TARGET_TYPE_TEXT:
            Gtk.drag_finish(context, False, False, time)
            return False

        buf = selection.get_text().strip()
        if '\r\n' in buf:
            paths = buf.split('\r\n')
        else:
            paths = buf.split('\n')
        self.logger.debug("dropped filename(s): %s" % (str(paths)))

        self.make_ui_callback('drag-drop', paths)

        Gtk.drag_finish(context, True, False, time)
        return True


class ImageViewZoom(Mixins.UIMixin, ImageViewEvent):

    # class variables for binding map and bindings can be set
    bindmapClass = Bindings.BindingMapper
    bindingsClass = Bindings.ImageViewBindings

    @classmethod
    def set_bindingsClass(cls, klass):
        cls.bindingsClass = klass

    @classmethod
    def set_bindmapClass(cls, klass):
        cls.bindmapClass = klass

    def __init__(self, logger=None, rgbmap=None, settings=None,
                 bindmap=None, bindings=None):
        ImageViewEvent.__init__(self, logger=logger, rgbmap=rgbmap,
                                settings=settings)
        Mixins.UIMixin.__init__(self)

        self.ui_setActive(True)

        if bindmap is None:
            bindmap = ImageViewZoom.bindmapClass(self.logger)
        self.bindmap = bindmap
        bindmap.register_for_events(self)

        if bindings is None:
            bindings = ImageViewZoom.bindingsClass(self.logger)
        self.set_bindings(bindings)

    def get_bindmap(self):
        return self.bindmap

    def get_bindings(self):
        return self.bindings

    def set_bindings(self, bindings):
        self.bindings = bindings
        bindings.set_bindings(self)


class CanvasView(ImageViewZoom):

    def __init__(self, logger=None, settings=None, rgbmap=None,
                 bindmap=None, bindings=None):
        ImageViewZoom.__init__(self, logger=logger, settings=settings,
                               rgbmap=rgbmap,
                               bindmap=bindmap, bindings=bindings)

        # Needed for UIMixin to propagate events correctly
        self.objects = [self.private_canvas]

    def set_canvas(self, canvas, private_canvas=None):
        super(CanvasView, self).set_canvas(canvas,
                                           private_canvas=private_canvas)

        self.objects[0] = self.private_canvas


class ImageViewCanvasError(ImageViewGtkError):
    pass

class ImageViewCanvas(ImageViewZoom,
                      DrawingMixin, CanvasMixin, CompoundMixin):

    def __init__(self, logger=None, rgbmap=None, settings=None,
                 bindmap=None, bindings=None):
        ImageViewZoom.__init__(self, logger=logger,
                               rgbmap=rgbmap,
                               settings=settings,
                               bindmap=bindmap,
                               bindings=bindings)
        CompoundMixin.__init__(self)
        CanvasMixin.__init__(self)
        DrawingMixin.__init__(self)

        # we are both a viewer and a canvas
        self.set_canvas(self, private_canvas=self)

        self._mi = ModeIndicator(self)

#END
