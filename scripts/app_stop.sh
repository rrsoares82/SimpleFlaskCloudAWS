#!/bin/sh
echo "Stopping ASWeb application"
systemctl stop simpleflaskcloudaws
if [ $? == 0 ]; then echo " ...application stopped"; fi