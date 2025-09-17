#!/bin/bash

# Number of iterations
COUNT=100

# Starting values
BASE_UUID="VIRTUAL-EVENT-GEN"
START_PORT=2001

for i in $(seq 1 $COUNT); do
  UUID=$(printf "%s-%03d" "$BASE_UUID" "$i")
  PORT=$((START_PORT + i - 1))

  sed \
    -e "s/VIRTUAL-EVENT-GEN-001/$UUID/" \
    -e "s/port: 2104/port: $PORT/" \
    asset.yml > asset_tmp.yml

  echo "Generated asset_tmp.yml with UUID=$UUID and port=$PORT"

  ofa device up asset_tmp.yml
  sleep 3
done
