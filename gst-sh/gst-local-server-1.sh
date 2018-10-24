#!/bin/bash
gst-launch-1.0 -v udpsrc port=5000 caps="application/x-rtp, media=video" ! rtph263pdepay ! avdec_h263 ! autovideosink
