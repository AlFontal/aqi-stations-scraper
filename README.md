# AQI Stations Scraper

[![Update datasets](https://github.com/AlFontal/aqi-stations-scraper/actions/workflows/actions.yml/badge.svg)](https://github.com/AlFontal/aqi-stations-scraper/actions/workflows/actions.yml)

I made this small Python utility in order to keep an updated record of
the historical data for the Air Quality Index for the > 180 Japanese Air
Monitoring stations, as I needed this data for my PhD research. I am currently
scraping from the site [aqicn.org](http://aqicn.org/sources/), which collects data from 
over 12,000 air monitoring stations.

Since I couldn't find an API to acces the historical data (at the time
of writing, you can only fetch current AQI values for any given location
through the [current API](https://aqicn.org/api/)) and I had been wanting
to test the web scraping capabilities of the `selenium` package for a 
while, I developed a (quite hacky) way of automatically fetching all
of the individual `csv` files with the historical data, which can be found
in the `data/japan-aqi` directory.

I wanted to test the CI/CD capabilities of Github Actions too (see the 
`.github/workflows/actions.yml` for the instructions),  so I set up a scheduled trigger
to run the workflow every Sunday at 2:00 AM UTC and update the datasets with new data.
