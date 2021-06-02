#!/bin/sh


for file in theorical_drone_tests.py theorical_snowplow_tests.py; do
    echo "runing test for" "$file"
    python3 "$file"
done
