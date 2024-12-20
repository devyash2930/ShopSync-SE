"""
Copyright (c) 2021 Rohan Shah
This code is licensed under MIT license (see LICENSE.MD for details)

@author: Slash
"""

from typing import Optional
from pydantic import BaseModel
from bs4 import BeautifulSoup
import requests

# local imports
import scraper_mt as scr
from configs import getCompanies

# cashback = getRakutenList()
companies = getCompanies()

# response type define
class jsonScraps(BaseModel):
    timestamp: str
    title: str
    price: str
    website: str
    link: Optional[str] = None
    
def search_items_API(
    site: str,
    item_name: str,
    relevant: Optional[str] = None,
    order_by_col: Optional[str] = None,
    reverse: Optional[bool] = False,
    listLengthInd: Optional[int] = 10,
    export: Optional[bool] = False
):
    '''Wrapper API to fetch AMAZON, WALMART and TARGET query results

    Parameters
    ----------
    item_name: string of item to be searched

    Returns
    ----------
    itemListJson: JSON List
        list of search results as JSON List
    '''
    # logging in file
    file = open("logger.txt", "a")
    file.write('amazon query:' + str(item_name)+'\n')

    # building argument
    args = {
        'search': item_name,
        'sort': 'pr' if order_by_col == 'price' else 'pr',  # placeholder TDB
        'des': reverse,  # placeholder TBD
        'num': listLengthInd,
        'relevant': relevant
    }

    scrapers = []
    if site == 'wm' or site == 'all':
        scrapers.append('walmart')
    if site == 'az' or site == 'all':
        scrapers.append('amazon')
    #if site == 'wm' or site == 'all':
     #   scrapers.append('walmart')
    if site == 'tg' or site == 'all':
        scrapers.append('target')
    if site == 'cc' or site == 'all':
        scrapers.append('costco')
    if site == 'bb' or site == 'all':
        scrapers.append('bestbuy')
    if site == 'eb' or site == 'all':
        scrapers.append('ebay')

    # calling scraper.scrape to fetch results
    itemList = scr.scrape(args=args, scrapers=scrapers)
    if not export and len(itemList) > 0:
        file.close()
        return itemList
    else:
        # No results
        return None

# def rakuten():
#     for i in range(len(companies)):
#         url = "https://www.rakuten.com/search?term=" + companies[i]
#         response = requests.get(url)
#         # Check if the request was successful (status code 200)
#         if response.status_code == 200:
#             # Parse the HTML content of the page
#             soup = BeautifulSoup(response.text, 'html.parser')
#             # Find the element containing the cashback information
#             cashback_element = soup.find('div', {'class': 'css-1i7dpco'})  # Adjust the class based on the actual HTML structure
#             if cashback_element:
#                 # Extract the cashback value
#                 cashback_value = cashback_element.text.strip()
#                 if (cashback_value):
#                     cashback[i] = cashback_value
#     return cashback