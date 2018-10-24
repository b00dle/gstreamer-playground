import gi
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
gi.require_version("GstVideo", "1.0")
from gi.repository import Gst, GObject, Gtk

viewer = None

def run_filesrc_viewer():
    global viewer
    from filesrc_viewer import FilesrcViewer
    GObject.threads_init()
    Gst.init(None)
    viewer = FilesrcViewer()
    Gtk.main()


def run_simple_video_viewer():
    global viewer
    from playbin_viewer import PlaybinViewer
    GObject.threads_init()
    Gst.init(None)
    viewer = PlaybinViewer()
    Gtk.main()


def run_audio_test():
    global viewer
    from audio_test_pipeline import AudioTest
    GObject.threads_init()
    Gst.init(None)
    viewer = AudioTest()
    Gtk.main()


def run_udp_video_sender():
    global viewer
    from udp_video_sender import UdpVideoSender
    GObject.threads_init()
    Gst.init(None)
    viewer = UdpVideoSender()
    Gtk.main()

if __name__ == "__main__":
    run_udp_video_sender()