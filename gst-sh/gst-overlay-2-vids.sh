#!/bin/bash
gst-launch-1.0 videomixer name=mixer sink_0::zorder=0 sink_1::zorder=1 sink_2::zorder=2 ! videoconvert ! autovideosink \
 filesrc location="green-sample-2.mp4" ! decodebin ! videoscale ! video/x-raw, width=1280, height=720 ! alpha method=green ! mixer.sink_0 \
 filesrc location="green-sample.mp4" ! decodebin ! videoscale ! video/x-raw, width=1280, height=720 ! alpha method=green ! mixer.sink_1 \
 filesrc location="green-sample-3.mp4" ! decodebin ! videoscale ! video/x-raw, width=1280, height=720 ! alpha method=green ! mixer.sink_2
