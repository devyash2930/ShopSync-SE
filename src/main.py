"""
Copyright (c) 2021 Rohan Shah
This code is licensed under MIT license (see LICENSE.MD for details)

@author: Slash
"""

# package imports
import uvicorn
from typing import Optional
from typing import List
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import csv
import nest_asyncio
import sys
import os
sys.path.append(os.path.abspath("Slash"))

import streamlit as st
from streamlit_option_menu import option_menu

import frontend.account as account
import frontend.slash_user_interface as slash_user_interface

st.set_page_config(page_title='ShopSync', layout= "wide")

class MultiApp:
    def __init__(self):
        self.apps = []
    
    def add_app(self,title,function):
        self.apps.append({
            "title":title,
            "function": function
        })
    
    def run():
        with st.sidebar:
            app = option_menu(
                menu_title='ShopSync',
                options=['Account', 'Home', 'Favourites','Logout'],
                icons=['person-circle', 'house-fill', 'star-fill', 'box-arrow-right'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
            )
        
        if app=="Account":
            account.app()
        
        if app=="Home":
            slash_user_interface.app()
    
    run()
# local imports
import scraper as scr


nest_asyncio.apply()
# response type define


class jsonScraps(BaseModel):
    timestamp: str
    title: str
    price: str
    website: str
    link: Optional[str] = None


app = FastAPI()

# Handling cors policy
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    '''Get documentation of API

    Parameters
    ----------
    None

    Returns
    ----------
    documentation redirect
    '''
    response = RedirectResponse(url='/redoc')
    return response


@app.get("/{site}/{item_name}", response_model=List[jsonScraps])
async def search_items_API(
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

    if site == 'az' or site == 'all':
        scrapers.append('amazon')
    if site == 'wm' or site == 'all':
        scrapers.append('walmart')
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
    elif len(itemList) > 0:
        # returning CSV
        with open('slash.csv', 'w', encoding='utf8', newline='') as f:
            dict_writer = csv.DictWriter(f, itemList[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(itemList)
        return FileResponse('slash.csv', media_type='application/octet-stream', filename='slash_'+item_name+'.csv')
    else:
        # No results
        return []


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5050)
