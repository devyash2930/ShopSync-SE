# -*- coding: utf-8 -*-
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from src.main_streamlit import search_items_API

def test_api_costco():
    product = 'Airpods'
    site = 'cc'
    result = search_items_API(site, product)
    assert result is not None
