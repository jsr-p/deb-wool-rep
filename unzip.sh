#!/usr/bin/env bash

mkdir -p data-raw
for file in zipfiles/*; do
    echo "Unzipping $file"
    unzip -o -d data-raw "$file"
done

# Some files wrong permissions
chmod -R a+r data-raw/
