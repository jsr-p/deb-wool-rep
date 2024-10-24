#!/usr/bin/env bash

# Run python scripts
for i in {2005..2018}; do 
        file=scripts/clean_$i.py
        echo "Running $file"
        python $file
done
