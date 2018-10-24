import gi
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
gi.require_version("GstVideo", "1.0")
from gi.repository import Gst, GObject, Gtk

class AudioTest(object):
    def __init__(self):
        self._init_ui()
        self._init_gst_pipe()

    def _init_ui(self):
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_title("Audio Test")
        self.window.set_default_size(100, 100)
        self.window.connect("destroy", Gtk.main_quit, "WM destroy")
        self.window.show_all()

    def _init_gst_pipe(self):
        self.pipeline = Gst.Pipeline()

        self.audiosrc = Gst.ElementFactory.make("audiotestsrc", "audio")
        self.pipeline.add(self.audiosrc)

        self.audiosink = Gst.ElementFactory.make("alsasink", "sink")
        self.pipeline.add(self.audiosink)

        self.audiosrc.link(self.audiosink)

        self.pipeline.set_state(Gst.State.PLAYING)