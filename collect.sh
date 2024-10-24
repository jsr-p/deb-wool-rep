#!/usr/bin/env bash


# website: https://www.cdc.gov/brfss/annual_data/annual_data.htm


urls=(
        https://www.cdc.gov/brfss/annual_data/2005/files/CDBRFS05XPT.zip
        https://www.cdc.gov/brfss/annual_data/2006/files/CDBRFS06XPT.ZIP
        http://www.cdc.gov/brfss/annual_data/2007/files/CDBRFS07XPT.ZIP
        https://www.cdc.gov/brfss/annual_data/2008/files/CDBRFS08XPT.ZIP
        https://www.cdc.gov/brfss/annual_data/2009/files/CDBRFS09XPT.ZIP
        https://www.cdc.gov/brfss/annual_data/2010/files/CDBRFS10XPT.zip
        https://www.cdc.gov/brfss/annual_data/2011/files/LLCP2011XPT.ZIP
        https://www.cdc.gov/brfss/annual_data/2012/files/LLCP2012XPT.ZIP
        https://www.cdc.gov/brfss/annual_data/2013/files/LLCP2013XPT.ZIP
        https://www.cdc.gov/brfss/annual_data/2014/files/LLCP2014XPT.ZIP
        https://www.cdc.gov/brfss/annual_data/2015/files/LLCP2015XPT.zip
        https://www.cdc.gov/brfss/annual_data/2016/files/LLCP2016XPT.zip
        https://www.cdc.gov/brfss/annual_data/2017/files/LLCP2017XPT.zip
        https://www.cdc.gov/brfss/annual_data/2018/files/LLCP2018XPT.zip
)

mkdir -p zipfiles
for url in "${urls[@]}"; do
        wget "$url" --directory-prefix=zipfiles
done
