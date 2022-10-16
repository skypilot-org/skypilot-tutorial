#!/usr/bin/env bash
# Usage: connect.sh <IP-address>

if [ $# -lt 1 ]; then
  echo $#
  echo 1>&2 "$0: not enough arguments. Please specify ip address to connect to."
  exit 2
elif [ $# -gt 1 ]; then
  echo 1>&2 "$0: too many arguments"
  exit 2
fi

# SSH connect to provided IP address using the this key
KEY='ADD_SKYPILOT_KEY_HERE'

# Constants
TMP_KEY_PATH='/tmp/key.pem'
USERNAME='ubuntu'

# Parse cmdline args
# The IP address of the EC2 instance
IP=$1

# Write the key to a file
rm -f ${TMP_KEY_PATH}
echo "$KEY" > ${TMP_KEY_PATH}
chmod 400 ${TMP_KEY_PATH}

# Connect and forward three ports
echo "======= SkyCamp 2022 ======="
echo "Connecting to $IP with username $USERNAME and forwarding port 8888, 8889 and 8890"
echo "============================"
ssh -i ${TMP_KEY_PATH} -L 8888:localhost:8888 -L 8889:localhost:8889 -L 8890:localhost:8890 "$USERNAME"@"$IP"
