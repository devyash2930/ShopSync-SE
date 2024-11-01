import streamlit as st
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'frontend')))

from favourites import fetch_title as fav
from account import fetch_title as acc
from logout import fetch_title as logt
from logout import fetch_state as logst
from slash_user_interface import fetch_title as slsh

# Mocking the Firebase initialization and authentication just in case they're used
@patch('firebase_admin.initialize_app')
@patch('firebase_admin.auth')
def test_fav_navigation(mock_auth, mock_initialize):
    # Define the pages to test
    assert fav() == "Favourites"

@patch('firebase_admin.initialize_app')
@patch('firebase_admin.auth')
def test_acc_navigation(mock_auth, mock_initialize):
    # Define the pages to test
    assert acc() == "Account"

@patch('firebase_admin.initialize_app')
@patch('firebase_admin.auth')
def test_logout(mock_auth, mock_initialize):
    assert logst() == False

@patch('firebase_admin.initialize_app')
@patch('firebase_admin.auth')
def test_logt_navigation(mock_auth, mock_initialize):
    # Define the pages to test
    assert logt() == "Logout"

@patch('firebase_admin.initialize_app')
@patch('firebase_admin.auth')
def test_slsh_navigation(mock_auth, mock_initialize):
    # Define the pages to test
    assert slsh() == "Home"
