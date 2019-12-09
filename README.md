# Sentiment-analysis-of-financial-news-data
This was developed as part of a study oriented project for 6th sem 2016-2017. It has been evolving since then.

Currently it fetches all the urls and scrapes data from the google search results and news archives of  
  * economictimes.indiatimes.com
  * reuters.com
  * ndtv.com
  * thehindubusinessline.com
  * moneycontrol.com
  * thehindu.com.

## Setup
Download the chrome driver from here [link](http://chromedriver.chromium.org/downloads).

Unzip it and then place the chromedriver in the root directory.

To setup the dependencies, do the following: 
```
pip install -r requirements.txt.
```
## Usage
Currently the pipeline is available till merging step. **Scrapy and sentiment integration are to be done.**

The complete help to use the following repo is as follows:
```
usage: parser.py [-h] -s START -e END -w [WEB [WEB ...]] [-r REGEXP]

Runs the entire pipeline from scraping to extracting sentiments.

optional arguments:
  -h, --help            show this help message and exit
  -s START, --start START
                        Start date,format-(dd/mm/yy)
  -e END, --end END     End date,format-(dd/mm/yy)
  -w [WEB [WEB ...]], --web [WEB [WEB ...]]
                        Specify the website number to scrape from separated by space						
                        0=economictimes.indiatimes.com						
                        1=reuters.com						
                        2=ndtv.com						
                        3=thehindubusinessline.com						
                        4=moneycontrol.com						
                        5=thehindu.com
  -r REGEXP, --regexp REGEXP
                        Complete path to the regex list file for companies. 
                        For template refer regesList file at root directory of this repo.
                         By default, it runs the regexList file present at root directory of this repo.
```
A sample run from **01/01/2014** to **01/10/2014** for 
* economictimes
* reuters
* thehindubusinessline 


would be given as follows:
```
python parser.py -s 01/01/2014 -e 01/10/2014 -w 0 1 3
```
Note: This assumes that the companies for which the data have to be fetched are specified in the default file,regexList. If user wants to specify some other file, it can be provided by using the **-r** parameter. Make sure to follow the template as given in regexList file.

## File Structure
```
.
├── code
│   ├── archive_scraper.py
│   ├── filter.py
│   ├── merger.py
|   ├── parser.py
│   ├── quick_scraper
│   │   ├── quick_scraper
│   │   │   ├── __init__.py
|   |   |   ..   
│   │   │   ├── settings.py
│   │   │   └── spiders
│   │   │       ├── __init__.py
│   │   │       ├── quick_scraper.py
│   │   │       └── scrape_with_bs4.py
│   │   └── scrapy.cfg
│   ├── search_scrape.py
│   └── sentiment.py
├── data
│   └── empty.txt
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

## Contribute

If you would like to contribute to this repo or have any ideas to make this better, feel free to submit a pull request or contact me at gyaneshmalhotra [at] gmail [dot] com.
For starters, there are some tasks available in the project tab of this repo on which you can start working on.
