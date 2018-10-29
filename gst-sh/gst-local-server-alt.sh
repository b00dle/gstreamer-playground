#!/bin/bash
gst-launch-1.0 -v udpsrc port=5000 caps="application/x-rtp, media=application" ! rtpjitterbuffer ! rtpgstdepay ! jpegdec ! fpsdisplaysink
