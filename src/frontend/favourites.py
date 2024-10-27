# import streamlit as st
# from firebase_admin import firestore, auth
# import pandas as pd

# def app():
#     # Initialize Firestore
#     db = firestore.client()

#     # Get the current user's UID using the email stored in session state
#     user = auth.get_user_by_email(st.session_state.user_email)  # Ensure user_email is set in session
#     uid = user.uid

#     # Reference to the user's document in the "favourites" collection
#     user_fav_ref = db.collection("favourites").document(uid)

#     # Fetch the user's favorites document
#     user_fav_doc = user_fav_ref.get()

#     if user_fav_doc.exists:
#         user_fav_data = user_fav_doc.to_dict()

#         # Convert Firestore data into a DataFrame for display
#         favorites_df = pd.DataFrame({
#             "Product": user_fav_data.get("Product", []),
#             "Description": user_fav_data.get("Description", []),
#             "Price": user_fav_data.get("Price", []),
#             "Link": user_fav_data.get("Link", []),
#             # "Rating": user_fav_data.get("Rating", []),
#             "Website": user_fav_data.get("Website", [])
#         })

#         st.title("Your Favorites")
#         st.dataframe(favorites_df.style.format({
#             "Link": lambda x: f'<a href="{x}" target="_blank">Link</a>',
#             "Website": lambda x: f'<a href="{x}" target="_blank">Website</a>',
#         }), unsafe_allow_html=True)

#         if favorites_df.empty:
#             st.write("You have no favorites yet.")
#     else:
#         st.title("Your Favorites")
#         st.write("You have no favorites yet.")


import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth
import pandas as pd
db = firestore.client()

def app():
    st.title("Favorites Page")

    # Fetch the user ID (UID) from Firebase Authentication
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
