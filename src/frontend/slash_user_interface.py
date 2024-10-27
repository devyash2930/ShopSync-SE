"""
Copyright (c) 2021 Anshul Patel
This code is licensed under MIT license (see LICENSE.MD for details)

@author: slash
"""
# gh
# Import Libraries
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit.components.v1 as components
import re
import pandas as pd
import configs as conf
from url_shortener import shorten_url
from main_streamlit import search_items_API
import streamlit as st
# sys.path.append('../')
# st.set_page_config(layout= "wide")
# st.title("ShopSync")
def app():
    page_bg = """
    <style>
        .appview-container {
            background-color: white !important;
        }
        .blur {
            filter: blur(5px);
            transition: filter 0.3s;
        }
        .loading {
            display: flex;
            justify-content: center;
            align-items: flex-start; /* Align to the top */
            height: 100vh; /* Full height of the viewport */
            position: absolute;
            top: 0; /* Position at the top */
            left: 0;
            right: 0;
            background-color: rgba(255, 255, 255, 0.8);
            z-index: 9999;
        }
        .spinner {
            border: 8px solid #f3f3f3; /* Light grey */
            border-top: 8px solid #3498db; /* Blue */
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: left; margin-bottom: -65px; color: #343434;'>Search For the Product to compare</h1>", unsafe_allow_html=True)
    def split_description(description):
        words = description.split()
        lines = []
        line = ""
        for word in words:
            if len(line) + len(word) + 1 <= 6:
                if line:
                    line += " "
                line += word
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        return '\n'.join(lines)
        '''words = description.split()
        lines = [' '.join(words[i:i+6]) for i in range(0, len(words), 6)]
        return '\n'.join(lines)'''
    st.markdown(page_bg, unsafe_allow_html=True)
    # Hide Footer in Streamlit
    hide_menu_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    if 'dataframe' not in st.session_state:
        st.session_state.dataframe = None


    # def highlight_row(dataframe):

    #     df = dataframe.copy()
    #     df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    #     minimumPrice = df['Price'].min()

    #     mask = df['Price'] == minimumPrice
    #     df.loc[mask, :] = 'background-color: lightgreen'
    #     df.loc[~mask, :] = 'background-color: #DFFFFA'
    #     return df

    # Display Image
    # st.image("assets/ShopSync_p.png")
    # st.markdown('<div class="text-input"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        /* Adjust the text input width */
        .stTextInput {
            font-size: 400px !important;
            width: 100% !important;
            max-width: 500px;
            margin-top: -40px;
        }
        /* Adjust the select box width */
        .stSelectbox {
            font-size: 400px !important;
            width: 100% !important;
            max-width: 500px;
            margin-top: -40px;
        }
        .stSlider{
        margin-top: -30px;
        margin-left: 5px;
        width: 400px !important;}
        </style>
        """,
        unsafe_allow_html=True
    )

    custom_css = """
    <style>
        .my-label {
            font-size: 20px;
            color: #5F5E5F;  /* Change this value to your desired font size */
            font-weight: bold; /* Optional: make the label bold */
        }
    </style>
    """
    price_custom_css = """
    <style>
        .my-label {
            font-size: 20px;
            color: #5F5E5F;  /* Change this value to your desired font size */
            font-weight: bold;
            margin-top: -60px;
            margin-bottom: -100px; /* Optional: make the label bold */
        }
    </style>
    """
    # Add the custom CSS to the app
    st.markdown(custom_css, unsafe_allow_html=True)
    prod, web = st.columns(2)
    with prod:
        # Create a text input with a custom label
        st.markdown('<span class="my-label">Enter the product item name</span>', unsafe_allow_html=True)
        product = st.text_input('', key='product',
                                placeholder='Type product name...', 
                                label_visibility="visible",
                                on_change=None, 
                                type='default', 
                                value='')  # Use the custom class
        # product = st.text_input('Enter the product item name', key='product', help="Enter the name of the product you are searching for")
        st.markdown(custom_css, unsafe_allow_html=True)
    with web:

        # Create a text input with a custom label
        st.markdown('<span class="my-label">Select Website</span>', unsafe_allow_html=True)
        website = st.selectbox('', ('All', 'Walmart',
                        'Amazon', 'Ebay', 'BestBuy', 'Target', 'Costco', 'All'))

    website_dict = {
        'Walmart': 'wm',
        'Amazon': 'az',
        'Ebay': 'eb',
        'BestBuy': 'bb',
        'Target': 'tg',
        'Costco': 'cc',
        'All': 'all'
    }


    # Initialize a variable to control loading state
    if 'loading' not in st.session_state:
        st.session_state.loading = False

    # Add a placeholder for loading spinner
    loading_placeholder = st.empty()

    # Add blur class if loading
    if st.session_state.loading:
        st.markdown('<div class="blur"></div>', unsafe_allow_html=True)

    # if 'selected_websites' not in st.session_state:
    #     st.session_state.selected_websites = []
    def reset_button():
        for website_name in website_dict.keys():
            if website_name.lower() != "all":  # Skip the 'all' entry
                # continue
                st.session_state[website_name] = False  # Set checkbox state to False
        # st.session_state['selected_websites'] = []  # Clear selected websites list

        # st.session_state["p"] = False  # Reset the checkbox value


    # Pass product and website to method
    if st.button('Search') and product and website:
        # Reset selected websites and price range before new search
        selected_websites = []
        selected_websites.clear()  # Reset selected websites
        reset_button()
        # st.session_state.price_range = (st.session_state.dataframe['Price'].min(), st.session_state.dataframe['Price'].max())  # Reset price range


        # Start loading
        st.session_state.loading = True
        loading_placeholder.markdown('<div class="loading"><div class="spinner"></div></div>', unsafe_allow_html=True)

        # rakuten_discount = rakuten()
        company_list = conf.getCompanies()
        results = search_items_API(website_dict[website], product)
        # Use st.columns based on return values
        description = []
        url = []
        price = []
        site = []
        # rakuten = []
        rating = []

        import random

        def get_random_value_from_list(lst):
            if not lst:
                return None  # Return None if the list is empty
            return random.choice(lst)

        my_list = [4.3, 4.0, 3.9, 4.8, 4.6, 4.4, 3.7, 3.5]

    # After the for loop populating the lists
        print("Lengths of lists:")
        print("Description length:", len(description))
        print("URL length:", len(url))
        print("Price length:", len(price))
        print("Site length:", len(site))
        # print("Rakuten length:", len(rakuten))
        print("Rating length:", len(rating))


        if results is not None and isinstance(results, list):
            for result in results:
                if result != {} and result['price'] != '':
                    description.append(result['title'])
                    url.append(result['link'])
                    price_str = result['price']
                    rating_value = get_random_value_from_list(my_list)

                    # Clean and extract price
                    clean_price_str = re.sub(r'[^\d\.\,]', '', price_str)  # Remove unwanted characters
                    match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)', clean_price_str)

                    if match:
                        price_str = match.group(0).replace(',', '')  # Remove commas for conversion
                        price_f = float(price_str)
                        price.append(price_f)
                        rating.append(rating_value)  # Append rating only if price is valid
                    else:
                        print("Unable to extract a valid price from the string:", price_str)
                        price.append(None)  # Append None if price extraction fails
                        rating.append(None)  # Append None for rating if price fails

                    site.append(result['website'])

        
        # for i in range(len(site)):
        #     k = company_list.index(site[i])
        #     rakuten.append(str(rakuten_discount[k]) + "%")

        if len(price):

            dataframe = pd.DataFrame(
                {'Description': description, 'Price': price, 'Link': url, 'Website': site,'Ratings': rating})
            dataframe['Description'] = dataframe['Description'].apply(
                split_description)
            dataframe['Product'] = dataframe['Description'].str.split(
            ).str[:3].str.join(' ')
            dataframe['Product'] = dataframe['Product'].str.replace(
                '[,"]', '', regex=True)
            product_column = dataframe.pop('Product')
            dataframe.insert(0, 'Product', product_column)

            dataframe['Price'] = dataframe['Price'].apply(
                lambda x: float(f'{x:.2f}'))
            # dataframe = dataframe.sort_values(by='Price', ascending=True)
            dataframe = dataframe.reset_index(drop=True)
            dataframe['Price'] = [f'{x:.2f}' for x in dataframe['Price']]

            def add_http_if_not_present(url):
                if url.startswith('http://') or url.startswith('https://'):
                    return url
                else:
                    return 'https://' + url
            dataframe['Link'] = dataframe['Link'].apply(add_http_if_not_present)

            st.session_state['dataframe'] = dataframe
            st.success("Data successfully scraped and cached.")

            # st.balloons()
            st.session_state.dataframe = dataframe

        else:
            st.error('Sorry!, there is no other website with same product')
        st.session_state.loading = False
        loading_placeholder.empty()  # Remove loading spinner

    def style_button_row(clicked_button_ix, n_buttons):
        def get_button_indices(button_ix):
            return {
                'nth_child': button_ix,
                'nth_last_child': n_buttons - button_ix + 1
            }

        clicked_style = """
        div[data-testid*="stHorizontalBlock"] > div:nth-child(%(nth_child)s):nth-last-child(%(nth_last_child)s) button {
            border-color: rgb(255, 75, 75);
            color: rgb(255, 75, 75);
            box-shadow: rgba(255, 75, 75, 0.5) 0px 0px 0px 0.2rem;
            outline: currentcolor none medium;
        }
        """
        unclicked_style = """
        div[data-testid*="stHorizontalBlock"] > div:nth-child(%(nth_child)s):nth-last-child(%(nth_last_child)s) button {
            pointer-events: none;
            cursor: not-allowed;
            opacity: 0.65;
            filter: alpha(opacity=65);
            -webkit-box-shadow: none;
            box-shadow: none;
        }
        """
        style = ""
        for ix in range(n_buttons):
            ix += 1
            if ix == clicked_button_ix:
                style += clicked_style % get_button_indices(ix)
            else:
                style += unclicked_style % get_button_indices(ix)
        st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)

    if 'dataframe' in st.session_state and isinstance(st.session_state.dataframe, pd.DataFrame):

        st.markdown("<h1 style='text-align: left; margin-bottom: -65px; color: #343434; margin-bottom: -20px;'>RESULT</h1>",
                    unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])# adjust the columns for price range and filters
        with col1:

            st.session_state.dataframe['Price'] = pd.to_numeric(
                st.session_state.dataframe['Price'], errors='coerce')
            
            st.markdown(price_custom_css, unsafe_allow_html=True)
            st.markdown('<span class="my-label">Price Range</span>', unsafe_allow_html=True)
            price_range = st.slider("", min_value=st.session_state.dataframe['Price'].min(), max_value=st.session_state.dataframe['Price'].max(
            ), value=(st.session_state.dataframe['Price'].min(), st.session_state.dataframe['Price'].max()))

            # Create two columns for sorting buttons
            button_col1, button_col2 = st.columns(2)

            # Add sorting buttons in separate columns
            with button_col1:
                sort_asc = st.button("Sort Asc", on_click=style_button_row, kwargs={
                    'clicked_button_ix': 1, 'n_buttons': 3
                })
                # sort_asc = st.button("Sort Ascending")
            with button_col2:
                sort_desc = st.button("Sort Desc", on_click=style_button_row, kwargs={
                    'clicked_button_ix': 2, 'n_buttons': 3
                })

            # Sort the DataFrame based on button clicks
            if sort_asc:
                st.session_state.dataframe = st.session_state.dataframe.sort_values(by='Price', ascending=True)
            elif sort_desc:
                st.session_state.dataframe = st.session_state.dataframe.sort_values(by='Price', ascending=False)

        with col2:
            st.markdown('<span class="my-label">Filter by Website</span>', unsafe_allow_html=True)

            # Define the number of checkboxes per row
            num_columns = 3  
            columns = st.columns(num_columns)

            # Iterate over the website dictionary and place each checkbox in a column
            selected_websites = []
            # selected_websites.clear()
            for idx, (website_name, website_code) in enumerate(website_dict.items()):
                if website_name.lower() == "all":
                    continue
                # Check if the website is in the selected_websites list
                col = columns[idx % num_columns]  # Place checkbox in the next column
                is_checked = col.checkbox(website_name, key=website_name)
                # Check if the checkbox is checked
                if is_checked:
                    selected_websites.append(website_name.lower())

            reset = st.button('Reset', on_click=reset_button)


        # Filter the dataframe by price range and selected websites
        filtered_df = st.session_state.dataframe[
            (st.session_state.dataframe["Price"] >= price_range[0]) &
            (st.session_state.dataframe["Price"] <= price_range[1])
        ]
        if selected_websites:
            filtered_df = filtered_df[filtered_df["Website"].isin(selected_websites)]
        # filtered_df = st.session_state.dataframe[(st.session_state.dataframe["Price"] >= price_range[0]) & (
        #     st.session_state.dataframe["Price"] <= price_range[1])]
        
        # Display the filtered dataframe at maximum width
        st.markdown("<h2 style='text-align: left; color: #343434;'>Filtered Results</h2>", unsafe_allow_html=True)
        styled_df = (
            filtered_df.style
            # .apply(highlight_row, axis=None)
            .set_table_attributes('style="width: 100%; border-collapse: collapse;"')
            .set_properties(**{
                'text-align': 'center',
                'font-size': '20px',
                'border': '1px solid #ddd',
                'padding': '8px',
            })
            .set_table_styles([
                {'selector': 'thead th', 'props': [('background-color', '#4a4e69'), ('color', 'white'), ('font-weight', 'bold')]},
                {'selector': 'tbody tr:hover', 'props': [('background-color', '#e8e8e8')]},  # Row hover effect
                {'selector': 'tbody td', 'props': [('border', '1px solid #ddd')]},  # Border for cells
            ])
        )

        # Display styled DataFrame
        st.dataframe(
            styled_df,
            column_config={"Link": st.column_config.LinkColumn("URL to website")},
            use_container_width=True  # Ensure the DataFrame uses the maximum width
        )
        st.write('<span style="font-size: 24px;">Add for favorites</span>', unsafe_allow_html=True)
        # //////////////////////////////////////////////////////////////////////////////////////////////
        # Prints the websites names from filter and dataframe to check
        # st.write("Unique Website values in the dataframe:")
        # st.write(st.session_state.dataframe["Website"].unique())

        # # Print the selected websites list
        # st.write("Selected websites for filtering:")
        # st.write(selected_websites)
       
        #///////////////////////////////////////////////////////////////////////////////////////////////

    if st.session_state.dataframe is not None:
        selected_index = st.selectbox("Select an index to get the corresponding row:", [
                                    None] + list(range(len(st.session_state.dataframe))))

        if selected_index is not None:
            fav = pd.DataFrame([st.session_state.dataframe.iloc[selected_index]])
            if 'fav' in st.session_state:
                st.session_state.fav = pd.concat(
                    [st.session_state.fav, fav], axis=0).drop_duplicates()
                st.dataframe(st.session_state.fav.style, column_config={"Link": st.column_config.LinkColumn(
                    "URL to website"), "Button": st.column_config.LinkColumn("Add to fav")},)

            else:
                st.session_state.fav = fav.copy()
                st.dataframe(fav.style, column_config={"Link": st.column_config.LinkColumn(
                    "URL to website"), "Button": st.column_config.LinkColumn("Add to fav")},)


    # Add footer to UI
    footer = """
    <style>
        a:link , a:visited{
        color: blue;
        background-color: transparent;
        text-decoration: underline;
    }

    a:hover,  a:active {
        color: red;
        background-color: transparent;
        text-decoration: underline;
    }

    .footer {
        position: fixed;
        left: 0;
        bottom: 0%;
        width: 100%;
        background-color: #DFFFFA;
        color: black;
        text-align: center;
    }

    a, a:link, a:visited {
        text-decoration: none;
        color: #6c63ff;
        font-weight: bold;
        }
    </style>
    <div class="footer">
        <p style='margin-bottom: 4px; display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        gap: 6px;'>Developed with ❤ by <a style='display: block; text-align: center;' href="https://github.com/devyash2930/ShopSync-SE" target="_blank">ShopSync</a></p>
        <p style='margin-bottom: 4px;'><a style='display: block; text-align: center;' href="https://github.com/Kashika08/CSC510_ShopSync_Group40/blob/main/LICENSE" target="_blank">MIT License Copyright (c) 2023</a></p>
        <p style='margin-bottom: 8px;'>Contributors: Devyash, Vatsal, Smit</p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)
