# Sentiment-analysis-of-financial-news-data
This is part of a study oriented project for 6th sem 2016-2017

Currently it fetches all the urls and scrapes data from the google search results and news archives of  
  * economictimes.indiatimes.com
  * reuters.com
  * ndtv.com
  * thehindubusinessline.com
  * moneycontrol.com
  * thehindu.com.

You have to specify the starting date, ending date, entity/company name and webpage url. Company name is required to be specified only in search_scrape.py. For archive_scraper.py, it iterates over all the names specified in the regexList.
After the results are fetched ,sentiment of each day's news item is calculated by concatenating all the news articles for a day and taking its average.
## Setup
Download the chrome driver from here [link](http://chromedriver.chromium.org/downloads).

Unzip it and then place the chromedriver in the root directory.

To setup the dependencies, do the following: 
```
pip install -r requirements.txt.
```
## File Structure
```
.
├── code
│   ├── archive_scraper.py
│   ├── filter.py
│   ├── merger.py
│   ├── quick_scraper.py
│   ├── scrape_with_bs4.py
│   ├── search_scrape.py
│   └── sentiment.py
├── data
│   ├── content
│   │   └── empty.txt
│   ├── empty.txt
│   └── links
│       └── empty.txt
├── LICENSE
├── README.md
├── regexList
├── requirements.txt
└── tracker.data
```

## File Description 

	USEFUL_FILES
      -> regexList- Contains the regex for the company name to enhance search results and get more relevant results.
      -> search_scrape.py- Scrapes urls from the google search results.
      -> filter.py- Filters the relevant urls collected from google search results.
      -> archive_scraper.py - Scrapes urls from archives of various websites.
      -> scrape_with_bs4.py- Scrapes the content from the scraped urls.
      -> quick_scraper.py- Scrapes content parallely and faster by sending multiple requests per second.
      -> merger.py- Merges the data collected from google search results and news archive.
      -> sentiment.py - Calculates the sentiment of the collected data.
      
  
## Note

* RegexList is used to fetch more relevant urls from the archives and not from the google search results. So there should be consistency in the names of company used across google search ( search_scrape.py ) and those mentioned in the regexList.
