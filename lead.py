import requests
import re
from bs4 import BeautifulSoup
import csv
import googlesearch


# Google
def goo_search(word, location):
    ua = googlesearch.get_random_user_agent()
    result = googlesearch.search(word + " " + location, num=30, start=0, stop=30, user_agent=ua, pause=5.0)
    for url in result:
        urls.append(url)
    for url in urls:
        for x in result:
            if x[:17] not in url:
                continue
            if x[:17] in url:
                dups.append(url)
        
    for x in dups:
        if x in urls:
            urls.remove(x)

# Scraping Function
def scraper(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    page_text = page.text
    try:
        address = address_search.findall(page_text)[0]
    except Exception:
        address = ''
    try:
        phone = phone_search.findall(page_text)[0]
    except Exception:
        phone = ''
    business = soup.title.get_text()
    writer.writerow({'Name': business, 'Phone': phone, 'Address': address})
    


urls = []
dups = []


# Input
kw = input('Keyword? ')
location = input('Location? ')

# Search Functions
address_search = re.compile(r"(\d{2,6}\s\w*\s*\w{3,9} (Avenue|Lane|Road|Boulevard|Drive|Street|Ave|Dr|Rd|Blvd|Ln|St))")
phone_search = re.compile(r"\(*\d\d\d\)*-\d\d\d-\d\d\d\d")

# Create Spreasheet
export = open('export.csv', 'w', newline='')
writer = csv.DictWriter(export, ['Name', 'Phone', 'Address'])
writer.writeheader()

# Get URLS
goo_search(kw, location)

# Scrape Urls
for x in urls:
    if 'yelp' not in x:
        scraper(x)

# Done
export.close()
print('Done')
