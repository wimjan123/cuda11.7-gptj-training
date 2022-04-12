#!/bin/bash

set -e

# DOCKER HUB
CMD="curl -vs -H 'Content-Type: application/json' -d \"{'username':'${DOCKER_HUB_SVC_USER}','password':'${DOCKER_HUB_SVC_PASS}'}\" https://hub.docker.com/v2/users/login"
TOKEN=$(${CMD} | jq -r .token)
echo "TOKEN: ${TOKEN}"

# JSON_DATA="{'full_description': '$(cat doc/README.md)'}"
# cmd="curl -vs -x PATCH -H 'Authorization: Bearer ${TOKEN}' -H 'Content-Type: application/json' -d '${JSON_DATA}' https://hub.docker.com/v2/repositories/nvidia/cuda/"
# echo "COMMAND: ${CMD}"
# ${CMD}


#
# NGC
#
# ngc registry image update nvidia/cuda  --overview doc/README.md
