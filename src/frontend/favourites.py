import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth
import pandas as pd
import os

def fetch_title():
    return "Favourites"

def initialize_firebase(mock=False):
    if mock:
        if not firebase_admin._apps:
            firebase_admin.initialize_app()
        return True

    json_path = os.path.join(os.path.dirname(__file__), 'shopsync-9ecdc-firebase-adminsdk-60nyc-7e5a173fe8.json')
    try:
        cred = credentials.Certificate(json_path)
        firebase_admin.initialize_app(cred)
        return True
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        raise e

def app(firestore_client=None):
    if not firebase_admin._apps:
        initialize_firebase(mock=False)

    if firestore_client is None:
        firestore_client = firestore.client()

    st.title("Favorites")

    user_email = st.session_state.user_email  # Ensure this is set
    user = auth.get_user_by_email(user_email)  # Get the user by email
    uid = user.uid

    # Reference to the user's document in the "favourites" collection
    user_fav_ref = firestore_client.collection("favourites").document(uid)
    user_fav_doc = user_fav_ref.get()

    if user_fav_doc.exists:
        user_fav_data = user_fav_doc.to_dict()

        # Convert user's favorites into a DataFrame
        favorites_df = pd.DataFrame({
            "Description": user_fav_data["Description"],
            "Link": user_fav_data["Link"],
            "Price": user_fav_data["Price"],
            "Product": user_fav_data["Product"],
            "Website": user_fav_data["Website"],
        })

        # Display the favorites DataFrame
        print("there")
        for index, row in favorites_df.iterrows():
            st.write(f"### {row['Product']}")
            st.write(f"**Description:** {row['Description']}")
            st.write(f"**Price:** {row['Price']}")
            st.write(f"**Website:** {row['Website']}")
            st.markdown(f"[View Product]({row['Link']})", unsafe_allow_html=True)

            # Add a "Remove from Favorites" button
            print("here")
            if st.button(f"Remove {row['Product']}", key=f"remove_{index}"):
                # Remove the product from Firestore
                updated_favorites = {
                    "Description": [d for i, d in enumerate(user_fav_data["Description"]) if i != index],
                    "Link": [l for i, l in enumerate(user_fav_data["Link"]) if i != index],
                    "Price": [p for i, p in enumerate(user_fav_data["Price"]) if i != index],
                    "Product": [p for i, p in enumerate(user_fav_data["Product"]) if i != index],
                    "Website": [w for i, w in enumerate(user_fav_data["Website"]) if i != index],
                }
                user_fav_ref.set(updated_favorites)
                st.success(f"{row['Product']} removed from favorites.")
                #st.experimental_rerun()  # Refresh the page after removal
    else:
        st.write("You have no favorites yet.")
