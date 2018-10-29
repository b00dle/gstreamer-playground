#!/bin/bash
gst-launch-1.0 videomixer name=mixer \
  sink_0::zorder=0 sink_1::zorder=1 sink_1::xpos=320 sink_2::zorder=2 sink_2::ypos=240 ! videoconvert ! fpsdisplaysink \
  udpsrc port=5000 caps="application/x-rtp, media=application" ! rtpgstdepay ! jpegdec ! videoscale ! video/x-raw, width=320, height=240 ! mixer.sink_0 \
  udpsrc port=5001 caps="application/x-rtp, media=application" ! rtpgstdepay ! jpegdec ! videoscale ! video/x-raw, width=320, height=240 ! mixer.sink_1 \
  udpsrc port=5002 caps="application/x-rtp, media=application" ! rtpgstdepay ! jpegdec ! videoscale ! video/x-raw, width=320, height=240 ! mixer.sink_2
