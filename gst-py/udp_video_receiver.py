import os
import gi
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
gi.require_version("GstVideo", "1.0")
from gi.repository import Gst, Gtk, GstVideo, GdkX11
from gst_pipeline import GstPipeline

class UdpVideoReceiver(GstPipeline):
    def __init__(self):
        super().__init__("Udp-Video-Receiver")
        self._init_ui()
        self._init_gst_pipe()

    def _init_ui(self):
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_title("Udp Video Receiver")
        self.window.set_default_size(500, 400)
        self.window.connect("destroy", Gtk.main_quit, "WM destroy")
        self.vbox_layout = Gtk.VBox()
        self.window.add(self.vbox_layout)
        hbox_layout = Gtk.HBox()
        self.vbox_layout.pack_start(hbox_layout, False, False, 0)
        self.entry = Gtk.Entry()
        hbox_layout.add(self.entry)
        self.button = Gtk.Button("Start")
        hbox_layout.pack_start(self.button, False, False, 0)
        #self.button.connect("clicked", self.start_stop)
        #self.movie_window = Gtk.DrawingArea()
        #self.vbox_layout.add(self.movie_window)
        self.window.show_all()

    def _init_gst_pipe(self):
        # create necessary elements
        self.udp_src = self.make_add_element("udpsrc", "udpsrc")
        self.udp_src.set_property("port", 5000)
        self.udp_src.set_property("caps", Gst.caps_from_string("application/x-rtp"))
        self.src_queue = self.make_add_element("queue", "src_queue")
        self.rtp_depay = self.make_add_element("rtpgstdepay", "rtp_depay")
        self.jpeg_decoder = self.make_add_element("jpegdec", "jpeg_decoder")
        self.videosink = self.make_add_element("gtksink", "videosink")
        self.vbox_layout.add(self.videosink.props.widget)
        self.videosink.props.widget.show()

        #self.register_callback(self.decoder, "pad-added", self.decoder_pad_added)

        self.link_elements(self.udp_src, self.src_queue)
        self.link_elements(self.src_queue, self.rtp_depay)
        self.link_elements(self.rtp_depay, self.jpeg_decoder)
        self.link_elements(self.jpeg_decoder, self.videosink)

        self.pipeline.set_state(Gst.State.PLAYING)

    def on_bus_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.STREAM_START:
            print("stream start")
            self.pipeline.set_state(Gst.State.PLAYING)
        elif t == Gst.MessageType.ERROR:
            self.pipeline.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print(message.src.get_name()+" Error: %s" % err, debug)
        elif t == Gst.MessageType.STATE_CHANGED:
            #if isinstance(message.src, Gst.Pipeline):
            old_state, new_state, pending_state = message.parse_state_changed()
            print(message.src.get_name()+" state changed from %s to %s." %
                  (old_state.value_nick, new_state.value_nick))
        elif t == Gst.MessageType.ELEMENT:
            print("element message from", message.src.get_name())
        else:
            print(t)

class UdpVideoReceiverAlt(GstPipeline):
    def __init__(self):
        super().__init__("Udp-Video-Receiver")
        self._init_ui()
        self._init_gst_pipe()

    def _init_ui(self):
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_title("Udp Video Receiver")
        self.window.set_default_size(500, 400)
        self.window.connect("destroy", Gtk.main_quit, "WM destroy")
        self.vbox_layout = Gtk.VBox()
        self.window.add(self.vbox_layout)
        hbox_layout = Gtk.HBox()
        self.vbox_layout.pack_start(hbox_layout, False, False, 0)
        self.entry = Gtk.Entry()
        hbox_layout.add(self.entry)
        self.button = Gtk.Button("Start")
        hbox_layout.pack_start(self.button, False, False, 0)
        #self.button.connect("clicked", self.start_stop)
        self.movie_window = Gtk.DrawingArea()
        self.vbox_layout.add(self.movie_window)
        self.window.show_all()

    def _init_gst_pipe(self):
        # create necessary elements
        self.udp_src = self.make_add_element("udpsrc", "udpsrc")
        self.udp_src.set_property("port", 5000)
        self.udp_src.set_property("caps", Gst.caps_from_string("application/x-rtp, media=video"))
        self.src_queue = self.make_add_element("queue", "src_queue")
        self.rtp_depay = self.make_add_element("rtph263pdepay", "rtp_depay")
        self.av_decoder = self.make_add_element("avdec_h263", "av_decoder")
        self.videosink = self.make_add_element("autovideosink", "videosink")
        #self.vbox_layout.add(self.videosink.props.widget)

        #self.register_callback(self.decoder, "pad-added", self.decoder_pad_added)

        self.link_elements(self.udp_src, self.src_queue)
        self.link_elements(self.src_queue, self.rtp_depay)
        self.link_elements(self.rtp_depay, self.av_decoder)
        self.link_elements(self.av_decoder, self.videosink)

        self.pipeline.set_state(Gst.State.PLAYING)

    def on_bus_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.STREAM_START:
            print("stream start")
            self.pipeline.set_state(Gst.State.PLAYING)
        elif t == Gst.MessageType.ERROR:
            self.pipeline.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print(message.src.get_name()+" Error: %s" % err, debug)
        elif t == Gst.MessageType.STATE_CHANGED:
            #if isinstance(message.src, Gst.Pipeline):
            old_state, new_state, pending_state = message.parse_state_changed()
            print(message.src.get_name()+" state changed from %s to %s." %
                  (old_state.value_nick, new_state.value_nick))
        elif t == Gst.MessageType.ELEMENT:
            print("element message from", message.src.get_name())
        else:
            print(t)

    def on_bus_sync_message(self, bus, message):
        """ Sets x window ID once image sink is ready to prepare output. """
        message_name = message.get_structure().get_name()
        if message_name == "prepare-window-handle":
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_window_handle(self.movie_window.get_property("window").get_xid())