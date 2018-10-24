import os
import gi
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
gi.require_version("GstVideo", "1.0")
from gi.repository import Gst, GObject, Gtk, GstVideo

from pprint import pprint

class FilesrcViewer(object):
    def __init__(self):
        self._init_ui()
        self._init_gst_pipe()

    def _init_ui(self):
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_title("Filesrc-Viewer")
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

    def _init_gst_pipe(self):
        self.pipeline = Gst.Pipeline.new("filesrc-viewer-pipeline")

        self.filesrc = Gst.ElementFactory.make("filesrc", "filesrc")
        self.pipeline.add(self.filesrc)

        self.decoder = Gst.ElementFactory.make("decodebin", "decoder")
        self.decoder.connect("pad-added", self.decoder_pad_added)
        self.pipeline.add(self.decoder)

        self.queue = Gst.ElementFactory.make("queue", "vid_queue")
        self.pipeline.add(self.queue)

        self.converter = Gst.ElementFactory.make("videoconvert", "converter")
        self.pipeline.add(self.converter)

        self.videosink = Gst.ElementFactory.make("autovideosink", "videosink")
        self.pipeline.add(self.videosink)

        # link filesrc to decoder
        self.filesrc.link(self.decoder)

        # link queue to converter through to video sink
        # note: queue will be linked once pads added on decoder
        # (see self.decoder_pad_added)
        self.queue.link(self.converter)
        self.converter.link(self.videosink)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

        #self.pipeline.set_state(Gst.State.PLAYING)

    def start_stop(self, w):
        if self.button.get_label() == "Start":
            filepath = self.entry.get_text().strip()
            if os.path.isfile(filepath):
                filepath = os.path.realpath(filepath)
                self.button.set_label("Stop")
                self.filesrc.set_property("location", filepath)
                self.pipeline.set_state(Gst.State.PLAYING)
            else:
                print("given path is no file")
        else:
            self.pipeline.set_state(Gst.State.NULL)
            self.button.set_label("Start")

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.pipeline.set_state(Gst.State.NULL)
            self.button.set_label("Start")
        elif t == Gst.MessageType.ERROR:
            self.pipeline.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            self.button.set_label("Start")

    def decoder_pad_added(self, decoder, pad):
        """ should be triggered once the decoder receives input from the filesrc. """
        template_property = pad.get_property("template")
        template_name = template_property.name_template
        if template_name == "src_%u":
            # link to video queue sink
            queue_sink = self.queue.sinkpads[0]
            pad.link(queue_sink)
        ''' # demuxers will probably have other template names
        if template_name == "video_%02d":
            # link to video queue sink
            queue_sink = self.queue.get_pad("sink")
            pad.link(queue_sink)
        elif template_name == "audio_%02d":
            # link to audio queue sink
            pass
        '''

    def on_sync_message(self, bus, message):
        message_name = message.get_structure().get_name()
        if message_name == "prepare-window-handle":
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_window_handle(self.movie_window.get_property("window").get_xid())