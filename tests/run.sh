#!/bin/sh

for file in theorical_drone_tests.py theorical_snowplow_tests.py; do
    echo "\nRUNNING TESTS FOR " "$file" "\n"
    python3 "$file"
done
