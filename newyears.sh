#!/usr/bin/env bash
years=(
        2015
        2016
        2017
)
for year in $years; do
        cat scripts/clean_2014.py | 
                sd "year = '2014'" "year = '$year'" > scripts/clean_$year.py
        echo scripts/clean_$year.py
done

# sex column named sex1 in 2018...
cat scripts/clean_2014.py | 
        sd "year = '2014'" "year = '2018'" |
        sd "sex = df.*" 'sex = df["sex1"]' > scripts/clean_2018.py
echo scripts/clean_$year.py
