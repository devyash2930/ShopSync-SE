# test_app.py

import streamlit as st
import sys,os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'frontend')))

from favourites import fetch_title as fav
from account import fetch_title as acc
from logout import fetch_title as logt
from logout import fetch_state as logst
from slash_user_interface import fetch_title as slsh


def test_fav_navigation():
    # Define the pages to test
    assert fav()=="Favourites"
    # if firebase_admin._apps:
    #     firebase_admin.delete_app(firebase_admin._apps[0])

def test_acc_navigation():
    # Define the pages to test
    assert acc()=="Account"
    # if firebase_admin._apps:
    #     firebase_admin.delete_app(firebase_admin._apps[0])

def test_logout():
    assert logst()==False

def test_logt_navigation():
    # Define the pages to test
    assert logt()=="Logout"
    
    # if firebase_admin._apps:
    #     firebase_admin.delete_app(firebase_admin._apps[0])

def test_slsh_navigation():
    # Define the pages to test
    assert slsh()=="Home"
    # if firebase_admin._apps:
    #     firebase_admin.delete_app(firebase_admin._apps[0])