# Sentiment-analysis-of-financial-news-data
This is part of a study oriented project for 6th sem 2016-2017

Currently it fetches all the urls and scrapes data from the google search results and news archives of  
  * economictimes.indiatimes.com
  * reuters.com
  * ndtv.com
  * thehindubusinessline.com
  * moneycontrol.com
  * thehindu.com.

You have to specify the starting date , ending date ,entity/company name and webpage url.

## File Structure 

	USEFUL_FILES
  
      -> search_scrape.py- Scrapes urls from the google search results.
      -> filter.py- Filters the relevant urls collected from google search results.
      -> archive_scraper.py - Scrapes urls from archives of various websites.
      -> scrape_with_bs4.py- Scrapes the content from the scraped urls.
      -> quick_scraper.py- Scrapes content parallely and faster by sending multiple requests per second.
      -> merger.py- Merges the data collected from google search results and news archive.
      -> sentiment.py - Calculates the sentiment of the collected data.
	
	
  
