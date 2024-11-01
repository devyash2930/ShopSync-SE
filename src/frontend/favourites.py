import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth
import pandas as pd
import os

def fetch_title():
    return "Favourites"

def initialize_firebase(suppress_errors=False):
    json_path = os.path.join(os.path.dirname(__file__), 'shopsync-se-firebase-adminsdk-nkzuw-ca6838f54f.json')
    try:
        # Path to Firebase service account key
        cred = credentials.Certificate(json_path)
        firebase_admin.initialize_app(cred)
        return True
    except Exception as e:
        if not suppress_errors:
            print(f"Error initializing Firebase: {e}")
        raise e

# Call the function to initialize Firebase
if not firebase_admin._apps:
    initialize_firebase()

db = firestore.client()

def app():
    st.title("Favorites")

    # Fetch the user ID (UID) from Firebase git stasAuthentication
    user_email = st.session_state.user_email  # Ensure this is set
    user = auth.get_user_by_email(user_email)  # Get the user by email
    uid = user.uid

    # Reference to the user's document in the "favourites" collection
    user_fav_ref = db.collection("favourites").document(uid)
    user_fav_doc = user_fav_ref.get()

    if user_fav_doc.exists:
        user_fav_data = user_fav_doc.to_dict()

        # Create a DataFrame from the user's favorites
        favorites_df = pd.DataFrame({
            "Description": user_fav_data["Description"],
            "Link": user_fav_data["Link"],
            "Price": user_fav_data["Price"],
            "Product": user_fav_data["Product"],
            # "Rating": user_fav_data["Rating"],
            "Website": user_fav_data["Website"],
        })

        # Display the favorites DataFrame
        st.dataframe(favorites_df.style, column_config={
            "Link": st.column_config.LinkColumn("URL to Website"),
            "Button": st.column_config.LinkColumn("Add to fav"),
        })
    else:
        st.write("You have no favorites yet.")

# In your main app file, call favourites.app() to use this