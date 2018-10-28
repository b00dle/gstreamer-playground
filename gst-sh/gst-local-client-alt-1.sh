#!/bin/bash
while :; 
do
  gst-launch-1.0 -v filesrc \
    location="/home/basti/Documents/studium/master/green-sample.mp4" ! \
    decodebin ! videoconvert ! jpegenc quality=75 ! \
    rtpgstpay ! udpsink port=5000
  printf '\n\n\nLOOPING CLIENT PLAYBACK\n\n\n';
  sleep 1; 
done
