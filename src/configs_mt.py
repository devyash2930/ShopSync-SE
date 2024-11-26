"""
Copyright (c) 2021 Rohan Shah
This code is licensed under MIT license (see LICENSE.MD for details)

@author: Slash
"""

# package imports
from datetime import datetime
import requests
from ebaysdk.finding import Connection
from threading import Thread
import html
import json


# configs
WALMART = {
    'site': 'walmart',
    'url': 'https://www.walmart.com/search?q=',
    'item_component': 'div',
    'item_indicator': {
        'data-item-id': True
    },
    'title_indicator': 'span.lh-title',
    'price_indicator': 'div[data-automation-id="product-price"] span.w_iUH7',
    'link_indicator': 'a',
    'image_indicator': 'img.absolute.top-0.left-0',
    'review_indicator': 'span.stars-container'
}

# AMAZON = {
#     'site': 'amazon',
#     'url': 'https://www.amazon.com/s?k=',
#     'item_component': 'div',
#     'item_indicator': {
#         'data-component-type': 's-search-result'
#     },
#     'title_indicator': 'h2 a span',
#     'price_indicator': 'span.a-price span',
#     'link_indicator': 'h2 a.a-link-normal',
#     'image_indicator': 'img.s-image',
#     'review_indicator': 'span.a-declarative a i span'
# }

COSTCO = {
    'site': 'costco',
    'url': 'https://www.costco.com/CatalogSearch?dept=All&keyword=',
    'item_component': 'div',
    'item_indicator': {
        'data-testid': 'Grid'
    },
    'title_indicator': 'div[data-testid^="Text_ProductTile_"]',  # Extract the title from the span
    'price_indicator': 'div.MuiTypography-root',  # Extract the price element
    'link_indicator': 'a',  # Anchor element for the product link
    'image_indicator': 'img',  # Use `img` tag for the product image
    'review_indicator': 'div.product-rating'  # Review container (verify its presence)
}

# TARGET = {
#     'site': 'target',
#     'url': 'https://www.target.com/s?searchTerm=',
#     'item_component': 'div',
#     'item_indicator': {
#         'data-test': '@web/ProductCard/ProductCardVariantDefault'
#     },
#     'title_indicator': 'a[data-test="product-title"]',
#     'price_indicator': 'span[data-test="product-price"]',
#     'link_indicator': 'a[data-test="product-title"]',
#     'image_indicator': 'img[data-test="product-image"]',
#     'review_indicator': 'div[data-test="average-rating"]'
# }

BESTBUY = {
    'site': 'bestbuy',
    'url': 'https://www.bestbuy.com/site/searchpage.jsp?st=',
    'item_component': 'div',
    'item_indicator': {
        'class': 'embedded-sku'
    },
    'title_indicator': 'h4.sku-title a',
    'price_indicator': 'div.priceView-customer-price span',
    'link_indicator': 'a.image-link',
    'image_indicator': 'img.product-image',
    'review_indicator': 'div.c-ratings-reviews p'  
}


# individual scrapers
class scrape_target(Thread):
    def __init__(self, query):
        self.result = []
        self.query = query
        super(scrape_target,self).__init__()

    def run(self):
        """Scrape Target's api for data

        Parameters
        ----------
        query: str
            Item to look for in the api

        Returns
        ----------
        items: list
            List of items from the dict
        """

        params = {
            'api_key': 'A6D50D2FA74944AEB91D4B18CBFDE4B0',
            'search_term': self.query,
            'type': 'search',
            'sort_by': 'best_match'
            }

        # make the http GET request to RedCircle API
        api_result = requests.get('https://api.redcircleapi.com/request', params).json()
        items = []
        # print("Requests Remaining on this account: " + api_result['request_info']['credits_remaining'])
        # print(api_result)
        if (api_result['request_info']['success']):
            for product in api_result['search_results']:
                try:
                    item = {
                        'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        'title': product['product']['title'],
                        'price': product['offers']['primary']['symbol'] + str(product['offers']['primary']['price']),
                        'website': 'target',
                        'link': product['product']['link']
                    }
                except:
                    continue
                items.append(item)
            # print(items)
        self.result = items


class scrape_ebay(Thread):
    def __init__(self, query):
        self.result = {}
        self.query = query
        super(scrape_ebay,self).__init__()

    def run(self):
        """Scrape Target's api for data

        Parameters
        ----------
        query: str
            Item to look for in the api

        Returns
        ----------
        items: list
            List of items from the dict
        """

        EBAY_APP = 'BradleyE-slash-PRD-2ddd2999f-2ae39cfa'

        try:
            api = Connection(appid=EBAY_APP, config_file=None, siteid='EBAY-US')
            response = api.execute('findItemsByKeywords', {'keywords': self.query})
        except ConnectionError as e:
            print(e)
            self.result = []

        data = response.dict()
        print(data)
        items = []
        for p in data['searchResult']['item']:
            item = {
                'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'title': html.unescape(p['title']),
                'price': '$' + p['sellingStatus']['currentPrice']['value'],
                'website': 'ebay',
                #'link': shorten_url(p['viewItemURL'])
                'link': p['viewItemURL'],
                'image_url': p['galleryURL'] if 'galleryURL' in p else 'https://via.placeholder.com/150',
                'review': p['sellerInfo']['positiveFeedbackPercent'] + '%' if 'sellerInfo' in p and 'positiveFeedbackPercent' in p['sellerInfo'] else 'No Reviews'
            }
            items.append(item)

        self.result = items




class scrape_amazon(Thread):
    def __init__(self, query):
        self.result = []
        self.query = query
        super(scrape_amazon, self).__init__()

    def run(self):
        """Scrape Amazon product data using Rainforest API

        Parameters
        ----------
        query: str
            Item to look for in the API

        Returns
        ----------
        items: list
            List of items from the API response
        """
        API_KEY = '34C1B2689C074F3BB120B22625C22F72'
        BASE_URL = 'https://api.rainforestapi.com/request'

        params = {
            'api_key': API_KEY,
            'type': 'search',
            'amazon_domain': 'amazon.com',
            'search_term': self.query,
        }

        try:
            # Send request to Rainforest API
            response = requests.get(BASE_URL, params=params)
            data = response.json()

            # Extract items from response
            items = []
            if "search_results" in data:
                for product in data["search_results"]:
                    try:
                        item = {
                            'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            'title': product['title'] if 'title' in product else 'No Title',
                            'price': f"${product['price']['value']}" if 'price' in product and 'value' in product['price'] else 'No Price',
                            'currency': product['price']['currency'] if 'price' in product and 'currency' in product['price'] else 'USD',
                            'website': 'amazon',
                            'link': product['link'] if 'link' in product else 'No Link',
                            'review': f"{product['rating']} stars" if 'rating' in product else 'No Rating',
                            'image_url': product['image'] if 'image' in product else 'https://via.placeholder.com/150'
                            
                        }
                        items.append(item)
                    except Exception as e:
                        print(f"Error processing product: {e}")
                        continue

            self.result = items

        except Exception as e:
            print(f"Error fetching data from Amazon API: {e}")
            self.result = []


CONFIGS = [WALMART, COSTCO, BESTBUY]
