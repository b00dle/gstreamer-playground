#!/bin/bash
gst-launch-1.0 videomixer name=mixer sink_0::zorder=0 sink_1::zorder=1 sink_2::zorder=2 ! videoconvert ! autovideosink \
 udpsrc port=5000 caps="application/x-rtp, media=video" ! rtph263pdepay ! avdec_h263 ! videoscale ! video/x-raw, width=640, height=480 ! alpha method=green ! mixer.sink_0 \
 udpsrc port=5001 caps="application/x-rtp, media=video" ! rtph263pdepay ! avdec_h263 ! videoscale ! video/x-raw, width=640, height=480 ! alpha method=green ! mixer.sink_1 \
 udpsrc port=5002 caps="application/x-rtp, media=video" ! rtph263pdepay ! avdec_h263 ! videoscale ! video/x-raw, width=640, height=480 ! alpha method=green ! mixer.sink_2
