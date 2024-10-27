import streamlit as st
import pandas as pd
from firebase_admin import firestore, auth

# Firestore client
db = firestore.client()

def get_user_uid():
    """
    Retrieve the user's UID from Firebase.
    This example assumes you have the user’s email stored in session state.
    """
    # Replace 'user_email' with the appropriate variable in your session state
    user_email = st.session_state.get("email")  # Ensure email is stored in session on login
    
    if user_email:
        user = auth.get_user_by_email(user_email)
        return user.uid
    else:
        st.sidebar.write("User not logged in.")
        return None

def get_user_favourites(user_uid):
    """
    Retrieve the favorites of the user from Firestore.
    """
    user_fav_ref = db.collection("favourites").document(user_uid)
    user_fav_doc = user_fav_ref.get()

    if user_fav_doc.exists:
        return user_fav_doc.to_dict()
    else:
        return {
            "Description": [],
            "Link": [],
            "Price": [],
            "Product": [],
            "Rating": [],
            "Website": []
        }

def app():
    user_uid = get_user_uid()
    if not user_uid:
        return

    """
    Display the user's favorites in the Streamlit sidebar.
    """
    # Retrieve the user's favorites
    user_favourites = get_user_favourites(user_uid)

    # Check if there are any favorites
    if not any(user_favourites.values()):
        st.sidebar.write("No favorites added yet.")
        return

    # Convert to DataFrame for easier display
    favourites_df = pd.DataFrame({
        "Product": user_favourites["Product"],
        "Description": user_favourites["Description"],
        "Price": user_favourites["Price"],
        "Website": user_favourites["Website"],
        "Rating": user_favourites["Rating"],
        "Link": user_favourites["Link"]
    })

    # Display favorites in the sidebar
    st.sidebar.write("### Your Favorites")
    for index, row in favourites_df.iterrows():
        st.sidebar.write(f"**Product:** {row['Product']}")
        st.sidebar.write(f"Description: {row['Description']}")
        st.sidebar.write(f"Price: {row['Price']}")
        st.sidebar.write(f"Website: {row['Website']}")
        st.sidebar.write(f"Rating: {row['Rating']}")
        st.sidebar.markdown(f"[Visit Link]({row['Link']})", unsafe_allow_html=True)
        st.sidebar.write("---")

# Example usage (you can call this from the main Streamlit app)
# user = auth.get_user_by_email(st.session_state.email) # Replace with your user email
# display_favourites_in_sidebar(user.uid)
