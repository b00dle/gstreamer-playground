import os

import gi
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
gi.require_version("GstVideo", "1.0")
from gi.repository import Gst, GObject, Gtk
# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11, GstVideo

class PlaybinViewer(object):
    def __init__(self):
        self._init_ui()
        self._init_player()

    def _init_ui(self):
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_title("Video-Player")
        self.window.set_default_size(500, 400)
        self.window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox_layout = Gtk.VBox()
        self.window.add(vbox_layout)
        hbox_layout = Gtk.HBox()
        vbox_layout.pack_start(hbox_layout, False, False, 0)
        self.entry = Gtk.Entry()
        hbox_layout.add(self.entry)
        self.button = Gtk.Button("Start")
        hbox_layout.pack_start(self.button, False, False, 0)
        self.button.connect("clicked", self.start_stop)
        self.movie_window = Gtk.DrawingArea()
        vbox_layout.add(self.movie_window)
        self.window.show_all()

    def _init_player(self):
        self.player = Gst.ElementFactory.make("playbin", "player")
        # init message handling for player bus
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_synch_message)
        # init bin to group time overlay and video_sink
        bin = Gst.Bin.new("video-and-time-bin")
        timeoverlay = Gst.ElementFactory.make("timeoverlay")
        bin.add(timeoverlay)
        time_pad = timeoverlay.get_static_pad("video_sink")
        ghostpad = Gst.GhostPad.new("sink", time_pad)
        bin.add_pad(ghostpad)
        videosink = Gst.ElementFactory.make("autovideosink")
        bin.add(videosink)
        timeoverlay.link(videosink)
        self.player.set_property("video-sink", bin)

    def start_stop(self, w):
        if self.button.get_label() == "Start":
            filepath = self.entry.get_text().strip()
            if os.path.isfile(filepath):
                filepath = os.path.realpath(filepath)
                self.button.set_label("Stop")
                self.player.set_property("uri", "file://" + filepath)
                self.player.set_state(Gst.State.PLAYING)
        else:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print ("Error: %s" % err, debug)
            self.button.set_label("Start")

    def on_synch_message(self, bus, message):
        if message.get_structure().get_name() == "prepare-window-handle":
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_window_handle(self.movie_window.get_property("window").get_xid())