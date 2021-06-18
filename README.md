# AQI Stations Scraper

I made this small Python utility in order to keep an updated record of
the historical data for the Air Quality Index for the > 180 Japanese Air
Monitoring stations, as I needed this data for my PhD research. 

Since I couldn't find an API to acces the historical data (at the time
of writing, you can only fetch current AQI values for any given location
through the [current API](https://aqicn.org/api/)) and I had been wanting
to test the web scraping capabilities of the `selenium` package for a 
while, I developed a (quite hacky) way of automatically fetching all
of the individual `csv` files with the historical data, which can be found
in the `data/japan-aqi` directory.