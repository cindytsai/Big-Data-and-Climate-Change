# Big Data and Climate Change
Try to find the relationship between weather report data and evidence of climate change, and the relationship between weather report data.
Eventually, try to forecast the weather report, from previous data.</br>
All daily weather report are from [Global Summary of the Day (GSOD)](https://www7.ncdc.noaa.gov/CDO/cdoselect.cmd?datasetabbv=GSOD&countryabbv=&georegionabbv=).

> This repository is still in progress. I haven't organized it yet, so the scripts break into several parts according to the steps and methods I made. Will be updated sooner or later if I have time or new discovery.

### Things Not Done Yet
- [ ] Raw data from Global Summary of the Day (GSOD), convert and insert _directly_ into SQLite.</br>
Since I import data into database manually by using [DB Browser](https://sqlitebrowser.org/) first, it still needs script to convert and insert into SQLite automaticlly.

***

## Contents
- Overview
- Raw Data Source



## Overview
### Directory
### Workflow

## Raw Data Source 
- [Global Summary of the Day (GSOD)](https://www7.ncdc.noaa.gov/CDO/cdoselect.cmd?datasetabbv=GSOD&countryabbv=&georegionabbv=)</br>
The data format and column name is nice and clean, though there might be some missing date and year in the file. In "_Select Output Format_" section, please choose "_comma delimited_", which will make my life easier! And also the script is specific to "comma delimited" format.
  - See more in [documentation file](https://www7.ncdc.noaa.gov/CDO/GSOD_DESC.txt).
  - Column Name and Unit<br>

| STN--- | WBAN | YEARMODA | TEMP | TEMP COUNT | DEWP | DEWP COUNT | SLP | SLP COUNT | STP | STP COUNT | VISIB | VISIB COUNT | WDSP | WDSP COUNT | MXSPD | GUST | MAX | MIN | PRCP | SNDP | FRSHTT |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| station number | Weather Bureau Air Force Navy number | year month day | average temperature | observation num to calculate mean temperature | average dew point | obervation num to calculate mean dew point | average sea level pressure | observation num to calculate mean sea level pressure | average station pressure | observation num to calculate mean station pressure | average visibility | observation num to calculate mean visibility | average wind speed | observation num to calculate mean wind speed | maximum sustained wind speed | maximum wind gust | maximum temperature (with flag) | minimum temperature (with flag) | total precipitation (with flag) | snow depth | Fog/Rain/Snow or Ice Pellets/Hail/Thunder/Tornado or Funnel Cloud |
| Int. | Int. | Int. | Real (&deg;F) | Int. | Real (&deg;F) | Int. | Real (millibar) | Int. | Real (millibar) | Int. | Real (mile) | Int. | Real (knot) | Int. | Real (knot) | Real (knot) | Real (&deg;F) and Char (\*) | Real (&deg;F) and Char (\*) | Real (inch) and Char | Real (inch) | Int.|

- [Storm Event Database](https://www.ncdc.noaa.gov/stormevents/)</br>
Data include the occurrence of storms, other significant weather phenomena; rare, unusual, weather phenomena that generate media attention; and other significant meteorological events.

## Data
- Convert and insert data into database.</br>
  - [convertData.py](https://github.com/cindytsai/weather_report_and_climate_change/blob/master/source/convertData.py)</br>
  The script converts data format and unit, then insert into database with table name "_year_".
  - Column Name and Unit</br>