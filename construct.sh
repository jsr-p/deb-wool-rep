#!/usr/bin/env bash

# Script to construct cleaning scripts from existing cleaning scripts
# by https://github.com/winstonlarson/brfss/tree/master
# I change the code to read parquet files; remove last lines and add some new
# columns

mkdir -p clean

for file in cleaning_code/clean_[1,2]*.py; do
        bname="$(basename $file)"
cat $file | sd '.*pd\.read_csv.*' \
        'df = pd.read_parquet(f"data/brfss{year}.parquet")
df = df.rename(columns=dict(zip(df.columns, df.columns.str.lower())))
df.columns = ["x." + col[1:] if col.startswith("_") else col for col in df.columns]' | head -n -4 > /tmp/txt.py

echo "mental_health = df['menthlth']
pm_health = df['poorhlth']
child1 = df['children']
child2 = df['x.chldcnt'] 
edu = df['educa'] 
brfss_out = pd.concat([ income, race, state, age, sex, height, 
weight, bmi, mental_health, child1, child2, edu, pm_health], axis=1)
brfss_out.columns = ['income', 'race', 'state', 'age', 'sex', 
'height', 'weight', 'bmi', 'mental_health', 'child1', 'child2', 
'edu', 'pm_health']
brfss_out.to_csv('clean/brfss'+year+'clean.csv')
print('Saved file to: clean/brfss'+year+'clean.csv')
" > /tmp/txt2.py
cat /tmp/txt.py /tmp/txt2.py > scripts/$bname
echo Processed $bname
done
