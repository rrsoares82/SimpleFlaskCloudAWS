#!/bin/sh
echo "pos installation checking ..."
systemctl restart simpleflaskcloudaws
if [ -f /opt/SimpleFlaskCloudAWS ]; then echo "SimpleFlaskCloudAWS installed on /opt/SimpleFlaskCloudAWS"; else echo "SimpleFlaskCloudAWS NOT installed (/opt/SimpleFlaskCloudAWS)"; fi
