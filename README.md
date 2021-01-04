Random scripts I worked on

#kontowecker-tracker
The only way to keep track of your Sparkasse account balance (without having to log in each time) is via their daily mailing service called "Kontowecker".
This Google Apps Script checks your GMail account for a new "Kontowecker"-mailing, extracts the current balance of the Sparkasse account and saves it in a Google spreadsheet (afterwards the mailing will be deleted).

#scraper.py
scraper.py is a Python script that simplifies the usage of three different scraping APIs (ScraperAPI, ScrapingBee & Wintr - to use this script, it is necessary to be registered with these services and to genereate API keys).
Best used as a replacement for requests, scraper.py checks the free tiers of the scraping services and scrapes provided urls with the service with the most remaining free api calls.
