#!/bin/sh
echo "Starting SimpleFlaskCloudAWS application"
systemctl start simpleflaskcloudaws
if [ $? == 0 ]; then echo " ...application started"; fi