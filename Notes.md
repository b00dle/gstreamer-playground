## ffmpeg short docs
- copy section of video
ffmpeg -i original.mp4 -ss 00:01:52 -c copy -t 00:00:10 output.mp4

## gstreamer short docs

### gstreamer python setup
- when creating virtualenv make sure to inherit site-packages
  - pygobject (import gi) has to be available

### play video
gst-launch-1.0 playbin uri=file:///home/basti/Documents/studium/master/green-sample.mp4

==> play only video
gst-launch-1.0 filesrc location="green-sample.mp4" ! decodebin ! videoconvert ! autovideosink

==> play video at scaled size
gst-launch-1.0 filesrc location="green-sample.mp4" ! decodebin ! videoscale ! video/x-raw, width=1920, height=1080 ! autovideosink

### mix video streams using alpha keying
gst-launch-1.0 videomixer name=mixer sink_0::zorder=0 sink_1::zorder=1 ! videoconvert ! autovideosink \
 videotestsrc pattern=snow ! mixer.sink_0 \
 videotestsrc pattern=smpte75 ! alpha method=green ! mixer.sink_1

- test using videos from files
gst-launch-1.0 videomixer name=mixer sink_0::zorder=0 sink_1::zorder=1 ! videoconvert ! autovideosink \
 filesrc location="sample-vid.mp4" ! decodebin ! mixer.sink_0 \
 filesrc location="green-sample.mp4" ! decodebin ! alpha method=green ! mixer.sink_1

==> and scaled to same size with 3 vids

gst-launch-1.0 videomixer name=mixer sink_0::zorder=0 sink_1::zorder=1 sink_2::zorder=2 ! videoconvert ! autovideosink \
 filesrc location="green-sample-2.mp4" ! decodebin ! videoscale ! video/x-raw, width=1280, height=720 ! alpha method=green ! mixer.sink_0 \
 filesrc location="green-sample.mp4" ! decodebin ! videoscale ! video/x-raw, width=1280, height=720 ! alpha method=green ! mixer.sink_1 \
 filesrc location="green-sample-3.mp4" ! decodebin ! videoscale ! video/x-raw, width=1280, height=720 ! alpha method=green ! mixer.sink_2

### stream video

==> SENDER
gst-launch-1.0 -v videotestsrc ! videoconvert ! avenc_h263p ! rtph263ppay ! udpsink port=5002
(copy <sender-caps> from output for receiver call)

==> RECEIVER
gst-launch-1.0 -v udpsrc port=5002 caps=<sender-caps> ! rtph263pdepay ! avdec_h263 ! autovideosink

example <sender-caps>: 

caps="application/x-rtp\,\ media\=\(string\)video\,\ clock-rate\=\(int\)90000\,\ encoding-name\=\(string\)H263-1998\,\ payload\=\(int\)96\,\ ssrc\=\(uint\)2158958671\,\ timestamp-offset\=\(uint\)3987338031\,\ seqnum-offset\=\(uint\)29927\,\ a-framerate\=\(string\)30"

caps="application/x-rtp, media=video"

