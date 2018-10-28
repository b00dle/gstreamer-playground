#!/bin/bash
while :; 
do
  gst-launch-1.0 -v filesrc \
    location="/home/basti/Documents/studium/master/green-sample-2.mp4" ! \
    decodebin ! videoconvert ! jpegenc quality=75 ! \
    rtpgstpay ! udpsink port=5001
  printf '\n\n\nLOOPING CLIENT PLAYBACK\n\n\n';
  sleep 1; 
done
