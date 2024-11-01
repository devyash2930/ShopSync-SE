import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
import src.frontend.favourites as favourites

class TestFavorites(unittest.TestCase):

    @patch('favourites.firestore')  # Mock Firestore interactions
    def setUp(self, mock_firestore):
        # Initialize session state for each test
        if 'favorites' not in st.session_state:
            st.session_state['favorites'] = []

        # Set up Firestore mock
        self.mock_firestore = mock_firestore
        self.mock_firestore.collection.return_value.document.return_value = MagicMock()

    def tearDown(self):
        # Clean up session state after each test
        st.session_state['favorites'] = []

    @patch('favourites.firestore')
    def test_add_to_favorites(self, mock_firestore):
        """ Test adding an item to favorites """
        # Test data
        item = {
            "product": "Laptop",
            "description": "High-end gaming laptop",
            "price": 1500,
            "url": "http://example.com",
            "website": "ShopSync",
            "rating": [4, 5, 5]
        }

        # Add item
        favourites.add_to_favorites(**item)

        # Assert item is added to session state and Firestore is called
        self.assertIn(item, st.session_state['favorites'])
        mock_firestore.collection.return_value.document.return_value.set.assert_called_once_with(item)

    @patch('favourites.firestore')
    def test_view_favorites(self, mock_firestore):
        """ Test viewing favorite items """
        # Mock data retrieval from Firestore
        mock_firestore.collection.return_value.document.return_value.get.return_value.to_dict.return_value = {
            "favorites": [
                {"product": "Laptop", "description": "Gaming laptop", "price": 1500, "url": "http://example.com", "website": "ShopSync", "rating": [5, 5, 5]},
                {"product": "Phone", "description": "Smartphone", "price": 700, "url": "http://example.com", "website": "ShopSync", "rating": [4, 4, 5]}
            ]
        }

        # Call view_favorites
        result = favourites.view_favorites()

        # Assert retrieved items match the mock data
        self.assertEqual(result, st.session_state['favorites'])

    @patch('favourites.firestore')
    def test_remove_from_favorites(self, mock_firestore):
        """ Test removing an item from favorites """
        # Add initial items to session state
        st.session_state['favorites'] = [
            {"product": "Laptop", "description": "Gaming laptop", "price": 1500, "url": "http://example.com", "website": "ShopSync", "rating": [5, 5, 5]},
            {"product": "Phone", "description": "Smartphone", "price": 700, "url": "http://example.com", "website": "ShopSync", "rating": [4, 4, 5]}
        ]

        # Remove "Laptop" from favorites
        favourites.remove_from_favorites("Laptop")

        # Assert "Laptop" is removed
        self.assertNotIn({"product": "Laptop", "description": "Gaming laptop", "price": 1500, "url": "http://example.com", "website": "ShopSync", "rating": [5, 5, 5]}, st.session_state['favorites'])

    @patch('favourites.firestore')
    def test_duplicate_item_addition(self, mock_firestore):
        """ Test handling of duplicate item addition """
        item = {
            "product": "Laptop",
            "description": "Gaming laptop",
            "price": 1500,
            "url": "http://example.com",
            "website": "ShopSync",
            "rating": [5, 5, 5]
        }

        # Add the same item twice
        favourites.add_to_favorites(**item)
        favourites.add_to_favorites(**item)

        # Assert item appears only once in session state
        self.assertEqual(st.session_state['favorites'].count(item), 1)

    @patch('favourites.firestore')
    def test_invalid_input(self, mock_firestore):
        """ Test invalid input handling (missing required fields) """
        # Add item with missing fields (e.g., no 'product')
        with self.assertRaises(TypeError):  # assuming code raises TypeError for missing arguments
            favourites.add_to_favorites(description="Gaming laptop", price=1500, url="http://example.com", website="ShopSync", rating=[5, 5, 5])

    @patch('favourites.firestore')
    def test_empty_favorites_display(self, mock_firestore):
        """ Test display when favorites list is empty """
        # Clear session state
        st.session_state['favorites'] = []

        # Call view_favorites
        result = favourites.view_favorites()

        # Assert result is empty
        self.assertEqual(result, [])

    @patch('favourites.firestore')
    def test_update_favorite_item(self, mock_firestore):
        """ Test updating an item in favorites """
        item = {
            "product": "Laptop",
            "description": "Gaming laptop",
            "price": 1500,
            "url": "http://example.com",
            "website": "ShopSync",
            "rating": [5, 5, 5]
        }

        # Add initial item
        favourites.add_to_favorites(**item)

        # Update item with a new price
        updated_item = item.copy()
        updated_item["price"] = 1200
        favourites.add_to_favorites(**updated_item)

        # Assert the updated price is reflected in session state
        self.assertIn(updated_item, st.session_state['favorites'])

    @patch('favourites.firestore')
    def test_firestore_session_state_sync(self, mock_firestore):
        """ Test synchronization between Firestore and session state """
        # Mock Firestore favorites list
        mock_favorites = [
            {"product": "Laptop", "description": "Gaming laptop", "price": 1500, "url": "http://example.com", "website": "ShopSync", "rating": [5, 5, 5]},
            {"product": "Phone", "description": "Smartphone", "price": 700, "url": "http://example.com", "website": "ShopSync", "rating": [4, 4, 5]}
        ]
        mock_firestore.collection.return_value.document.return_value.get.return_value.to_dict.return_value = {
            "favorites": mock_favorites
        }

        # Sync session state with Firestore
        favourites.sync_session_state_with_firestore()

        # Assert session state matches Firestore mock data
        self.assertEqual(st.session_state['favorites'], mock_favorites)

if __name__ == '__main__':
    unittest.main()
