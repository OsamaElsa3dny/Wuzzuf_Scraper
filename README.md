# Wuzzuf Job Scraper

A [Scrapy](https://scrapy.org/) project that collects job-listing data from Wuzzuf search results and exports it as a CSV file. It is aimed at exploring demand for software, data, AI, cloud, DevOps, and related roles.

## What it collects

For each job listing, the scraper captures:

- Search keyword and result-page number
- Job title and company name
- Location and posted time, when available
- Experience requirement
- Listed skills and technologies

Before export, the cleaning pipeline removes incomplete listings and normalizes company names, locations, and technology lists.

## Included searches

The spider currently searches for these keywords:

`software`, `python`, `backend`, `frontend`, `Data scientist`, `Data engineer`, `Machine learning`, `Ai`, `Cloud`, `Devops`, `full stack`, `Data Analyst`, `Web Application Developer`, and `Mobile Application Developer`.

Change the `keywords` list in [wuzzuf.py](wuzzufscraper/wuzzufscraper/spiders/wuzzuf.py) to customize the search scope.

## Setup

This project requires Python 3 and the following packages:

```bash
python -m pip install scrapy regex pymssql
```

`pymssql` is only needed if you enable the optional SQL Server pipeline; CSV export works with Scrapy and `regex`.

## Run the scraper

Run the spider from the Scrapy project directory:

```bash
cd wuzzufscraper
scrapy crawl wuzzuf_jobs
```

By default, data is written to `wuzzufscraper/wuzzuf_jobs.csv` in UTF-8 CSV format. Existing output may be replaced, so rename or move it first if you need to keep a previous run.

To choose a different output file for one run:

```bash
scrapy crawl wuzzuf_jobs -O jobs.csv
```

## Configuration

Project-level settings are in [settings.py](wuzzufscraper/wuzzufscraper/settings.py). The spider also sets a five-second request delay and limits concurrent requests to five. You can adjust these values in the spider's `custom_settings` when tuning a run.

The scraper keeps requesting pages until a search has no job listings. Wuzzuf's markup and access controls can change over time, so CSS selectors may need maintenance if results stop being captured.

## Responsible use

Use the scraper in accordance with Wuzzuf's terms, robots policy, and applicable law. Keep request rates conservative and use the collected data responsibly.
