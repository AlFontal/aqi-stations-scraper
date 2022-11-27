# AQI Stations Scraper

[![Update datasets](https://github.com/AlFontal/aqi-stations-scraper/actions/workflows/actions.yml/badge.svg)](https://github.com/AlFontal/aqi-stations-scraper/actions/workflows/actions.yml)
![python](https://img.shields.io/badge/python-v3.10-orange?logo=Python&logoColor=white)

I made this small Python utility in order to keep an updated record of  the historical data for the
Air Quality Index for the >180 Japanese Air Monitoring stations, as I needed this data for my PhD
research. I am currently  scraping from the site [aqicn.org](http://aqicn.org/sources/), which
collects data from  over 12,000 air monitoring stations.

Since I couldn't find an API to access the historical data (at the time of writing, you can only
fetch current AQI values for any given location through the [current API](https://aqicn.org/api/))
and I had been wanting to test the web scraping capabilities of the `selenium` package for a while,
I developed a (quite hacky) way of automatically fetching all of the individual `csv` files with the
complete historical data, which can be found  in the `data/japan-aqi` directory.

I wanted to test the CI/CD capabilities of Github Actions too (see the 
`.github/workflows/actions.yml` directory for the instructions),  so I set up a scheduled trigger
to run the workflow every Sunday at 2:00 AM UTC and update the datasets with new data.

## Running locally

In case you want to run a local instance, you will need to first clone the repo and generate a
`.env` file in the root directory including the following variables which will then be used when
doing the requests to the site:

```bash
USER_FULL_NAME = 'Your name'
USER_EMAIL = 'Your email'
USER_ORGANIZATION = 'Your org'
```

To reproduce the environment you will need to use `poetry` to install the dependencies, which you
can install either by running (recommended):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or if you want to use `pipx`:

```bash
pipx install poetry
```

You can check the [official poetry docs](https://python-poetry.org/docs/#installing-with-the-official-installer) to see the up-to-date installation instructions.

With a working version of `poetry` running in your system, just run:

```bash
poetry install
```

Which will install the dependencies defined in `pyproject.toml`. You should now be able to use:

```bash
poetry run python japan_aqi.py
```

To run the scraping script which should download the available files at the time.