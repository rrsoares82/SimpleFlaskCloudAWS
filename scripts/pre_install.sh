#!/bin/sh

root_path=$(dirname $(dirname $0))

echo "Installing/updating pip"
apt install pip -y

echo "Installing requirements"
python3 -m pip install -r "$root_path/requirements.txt" --break-system-packages

echo "Backup up old environment"
tar -zvcf /opt/SimpleFlaskCloudAWS.tar.gz /opt/SimpleFlaskCloudAWS

echo "Removing old files"
rm -fr /opt/SimpleFlaskCloudAWS