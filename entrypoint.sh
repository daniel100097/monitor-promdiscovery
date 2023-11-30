#!/bin/bash

set -e

while true; do
    echo "Starting monitor_promdiscovery"
    python monitor_promdiscovery -f /config.yml -s icinga2
    echo "Sleeping for 60 seconds"
    sleep 60
done
