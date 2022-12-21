# findOrcs.py - Opens several Bingo search results for Russian sites
from bs4 import BeautifulSoup
import openpyxl, os
import time
import datetime
import urllib.parse
import csv
from pathlib import Path
from urllib.error import URLError, HTTPError
import logging

''' since update of Firefox new conditions for webdriver'''
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
binary = FirefoxBinary(r'/usr/bin/firefox')
caps = DesiredCapabilities.FIREFOX.copy()
caps['marionette'] = True
# hide window of Webdriver
options = Options()
options.add_argument('--headless')
''' end of webdriver'''

TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
QUERY_LIST_FILE = Path(f'./keyword_list.csv')
sites = ["https://mil.ru/","http://publication.pravo.gov.ru/","http://www.kremlin.ru/","http://prezident.org/","https://ria.ru/","https://lenta.ru/","https://ren.tv/","https://www.soldati-russian.ru/","https://tsargrad.tv/","https://tvzvezda.ru/","https://tass.ru/","https://myrotvorets.center/","https://ingushetia.ru/"]
candList = []
OUTPUT_FILE = Path(f'./output.csv')

def get_keywords():
    with open(QUERY_LIST_FILE, 'r') as i_file:
        # rows = csv.reader(i_file, delimiter=',')
        rows = csv.reader(i_file)
        global keywords
        keywords = [row[0] for row in rows]
        return keywords

def avoid_duplicates(output_file):
    """Search in outpotfile all ready parsed names ans skip it"""
    if output_file.is_file():
        with open(OUTPUT_FILE, 'r') as i_file:
            rows = csv.reader(i_file, delimiter=',')
            results = [row[0] for row in rows]
    else:
        results = []
    return results

def emit_row(output_file, row): #get data to csv
    if output_file.is_file():
        with open(output_file, 'a') as o_file:
            fieldnames = row.keys()
            writer = csv.DictWriter(o_file, fieldnames=fieldnames)
            writer.writerow(row)
    else:
        with open(output_file, 'w') as o_file:
            fieldnames = row.keys()
            writer = csv.DictWriter(o_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(row)

class CrawlerBingo:
    """getting data for searching"""
    def __init__(self, searchSite, searchRequest):
        self.searchSite = searchSite
        self.searchRequest = searchRequest
        self.siteList = []


    def getUrl (self, pages):
            """using webdriver to get results"""
            newPage = '&first={}&FORM=PERE'.format(1 + pages)
            url = (
                "https://www.bing.com/search?q=%22{}%22+site%3A{}&go=Search&qs=ds{}").format(
                self.searchRequest, self.searchSite, newPage)
            print(url)
            driver = webdriver.Firefox(firefox_binary=binary, capabilities=caps,
                                       executable_path='/usr/bin/geckodriver',
                                       options=options)  # hide window of webdriver
            time.sleep(3)
            driver.get(url)
            time.sleep(3Посада	Обсяг робіт	зп
)
            pageSource = driver.page_source
            driver.close()
            return BeautifulSoup(pageSource, 'html.parser')

    def cycle (self):
        for pages in range(0, 100, 10): # listing pages in Bing results (from 10 to 200)

            bs = self.getUrl(pages)
            nameList = bs.find_all(['h2']) #selecting all h2 tags
            print(f'For name {keywords[searchingRequest]} and site {sites[site]}...')
            if nameList:
                for name in range(len(nameList)):
                    text = nameList[name].get_text() #appending title of news
                    try:
                        href = nameList[name].find('a').get('href') # appending link
                    except AttributeError as e:
                        print(e, 'sleep for 10')
                        time.sleep(60 * 10)
                        break
                    print(f'header is {text} and link is {href}')
                    relation['Name'] = keywords[searchingRequest]
                    relation['Site'] = sites[site]
                    relation['Header'] = text
                    relation['Link'] = href
                    emit_row(OUTPUT_FILE, relation)  # putting all in csv
            else:
                print("Nothing found")
                relation['Name'] = keywords[searchingRequest]
                relation['Site'] = sites[site]
                relation['Header'] = 'No data'
                relation['Link'] = 'No data'
                emit_row(OUTPUT_FILE, relation)  # putting all in csv
                break

    def parse (self):
        """starting our parser"""
        self.cycle()
        return relation


def encodeToUrl(cyrilNames):
    """encoding Cyrilic names to url"""
    searchingRequests = []
    for cyrilName in cyrilNames:
        convNames = urllib.parse.quote(cyrilName)
        searchingRequests.append(convNames)
    return searchingRequests


##########
cyrilNames = get_keywords()
searchingRequests = encodeToUrl(cyrilNames)
results = avoid_duplicates(OUTPUT_FILE)
print(results)
relation = {} # forming dictionary to record key(fields name) and values from e data
for searchingRequest in range(len(searchingRequests)):
    print(f'getting... {keywords[searchingRequest]}')
    if keywords[searchingRequest] not in results:
        for site in range(len(sites)):
            print(f'Searching... {keywords[searchingRequest]} on site {sites[site]}')
            crawlerBingo = CrawlerBingo(sites[site], searchingRequests[searchingRequest])
            crawlerBingo.parse()
    else:
        print(f'This ork {keywords[searchingRequest]} was already parsed. Skipping')
        continue #skip the duplicate
