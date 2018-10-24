import os
import gi
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
gi.require_version("GstVideo", "1.0")
from gi.repository import Gst, Gtk, GstVideo
from gst_pipeline import GstPipeline

class UdpVideoSender(GstPipeline):
    def __init__(self):
        super().__init__("Filesrc-Viewer")
        self._init_ui()
        self._init_gst_pipe()

    def _init_ui(self):
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_title("Udp Video Sender")
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
        # create necessary elements
        self.filesrc = self.make_add_element("filesrc", "filesrc")
        self.decoder = self.make_add_element("decodebin", "decoder")
        self.queue = self.make_add_element("queue", "vid_queue")
        self.converter = self.make_add_element("videoconvert", "converter")
        self.h263_encoder = self.make_add_element("avenc_h263p", "h263_encoder")
        self.rtp_packer = self.make_add_element("rtph263ppay", "rtp_packer")
        self.udp_sink = self.make_add_element("udpsink", "udp_sink")
        self.udp_sink.set_property("port", 5000)

        # connect element signals
        self.register_callback(self.decoder, "pad-added", self.decoder_pad_added)

        # setup pipeline links
        self.link_elements(self.filesrc, self.decoder)

        # link queue to converter through to udp sink
        # note: queue will be dynamically linked once pad is added on decoder
        # (see self.decoder_pad_added)
        self.link_elements(self.queue, self.converter)
        self.link_elements(self.converter, self.h263_encoder)
        self.link_elements(self.h263_encoder, self.rtp_packer)
        self.link_elements(self.rtp_packer, self.udp_sink)

    def on_bus_message(self, bus, message):
        """ Resets Start button based on playback/error state. """
        t = message.type
        if t == Gst.MessageType.EOS:
            self.pipeline.set_state(Gst.State.NULL)
            self.button.set_label("Start")
        elif t == Gst.MessageType.ERROR:
            self.pipeline.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            self.button.set_label("Start")

    def on_bus_sync_message(self, bus, message):
        pass

    def start_stop(self, w):
        """ Toggles playback depending on current play state. """
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

    def decoder_pad_added(self, decoder, pad):
        """
        Link decoder src pad to queue sink pad
        once the decoder receives input from the filesrc.
        """
        template_property = pad.get_property("template")
        template_name = template_property.name_template
        # template name may differ for other decoders/demuxers
        if template_name == "src_%u":
            # link to video queue sink
            queue_sink = self.queue.sinkpads[0]
            self.link_elements(pad, queue_sink)