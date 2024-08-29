#!/bin/sh
echo "Validating services and deploy"
systemctl status SimpleFlaskCloudAWS
if [ $? != 0 ]; then echo "SimpleFlaskCloudAWS application WASN'T started"; else echo "SimpleFlaskCloudAWS application started"; fi
curl -f http://localhost:8080/> /dev/null
if [ $? != 0 ]; then  echo "COULD NOT access SimpleFlaskCloudAWS application"; else echo "SimpleFlaskCloudAWS application are accessible"; fi

