# Big Data and Climate Change
Try to find the relationship between weather report data and evidence of climate change, and the relationship between weather report data.
Eventually, try to forecast the weather report, from previous data.</br>
All daily weather report are from [Global Summary of the Day (GSOD)](https://www7.ncdc.noaa.gov/CDO/cdoselect.cmd?datasetabbv=GSOD&countryabbv=&georegionabbv=).

> This repository is still in progress. I haven't organized it yet, so the scripts break into several parts according to the steps and methods I made. Will be updated sooner or later if I have time or new discovery.

## Things Not Done Yet
- [ ] Raw data from Global Summary of the Day (GSOD), convert and insert _directly_ into SQLite.</br>
Since I import data into database manually by using [DB Browser](https://sqlitebrowser.org/) first, it still needs script to convert and insert into SQLite automaticlly.

## Contents

## Raw Data Source 
- [Global Summary of the Day (GSOD)](https://www7.ncdc.noaa.gov/CDO/cdoselect.cmd?datasetabbv=GSOD&countryabbv=&georegionabbv=)</br>
The data format and column name is nice and clean, though there might be some missing date and year in the file. In "_Select Output Format_" section, please choose "_comma delimited_", which will make my life easier! And also the script is specific to "comma delimited" format.
  - Column Name and Unit
  | STN--- | WBAN | YEARMODA | TEMP | TEMP COUNT | DEWP | DEWP COUNT | SLP | SLP COUNT | STP | STP COUNT | VISIB | VISIB COUNT | WDSP | WDSP COUNT | MXSPD | GUST | MAX | MIN | PRCP | SNDP | FRSHTT |
  | ------ | ---- | -------- | ---- | ---------- | ---- | ---------- | --- | --------- | --- | --------- | ----- | ----------- | ---- | ---------- | ----- | ---- | --- | --- | ---- | ---- | ------ |
  
