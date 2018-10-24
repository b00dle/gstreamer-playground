#!/bin/bash
while :; 
do
  gst-launch-1.0 -v filesrc location="green-sample.mp4" ! decodebin ! videoconvert ! avenc_h263p ! rtph263ppay ! udpsink port=5001
  printf '\n\n\nLOOPING CLIENT PLAYBACK\n\n\n';
  sleep 1; 
done
