<p align="center"><img width="500" src="./assets/shopsync-logos.jpeg"></p>

[![Made With](https://img.shields.io/badge/made%20with-python-blue)](https://www.python.org/)
[![GitHub stars](https://badgen.net/github/stars/Neel317/ShopSync)](https://badgen.net/github/stars/Neel317/ShopSync)
[![DOI](https://zenodo.org/badge/866275389.svg)](https://doi.org/10.5281/zenodo.14020467)
[![codecov](https://codecov.io/github/devyash2930/ShopSync-SE/branch/testing/graph/badge.svg?token=TP83NH85TA)](https://codecov.io/github/devyash2930/ShopSync-SE)
[![Run Tests On Push](https://github.com/Neel317/ShopSync/actions/workflows/unit_test.yml/badge.svg)](https://github.com/devyash2930/ShopSync-SE/actions/workflows/unit_test.yml)
[![Lint Python](https://github.com/Neel317/ShopSync/actions/workflows/main.yml/badge.svg)](https://github.com/devyash2930/ShopSync-SE/actions/workflows/main.yml)
[![Running Code Coverage](https://github.com/Neel317/ShopSync/actions/workflows/code_cov.yml/badge.svg)](https://github.com/devyash2930/ShopSync-SE/actions/workflows/code_cov.yml)



<!--Badges-->
<a href="https://github.com/Neel317/ShopSync/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/Neel317/ShopSync"></a>
<a href="https://github.com/Neel317/ShopSync/pulse"><img alt="GitHub forks" src="https://img.shields.io/github/forks/Neel317/ShopSync"></a>
<a href="https://github.com/Neel317/ShopSync/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/Neel317/ShopSync"></a>
<img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/Neel317/ShopSync">
<img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/Neel317/ShopSync">


<p align="center">
    <a href="https://github.com/devyash2930/ShopSync-SE/issues/new/choose">Report Bug</a>
    ·
    <a href="https://github.com/devyash2930/ShopSync-SE/issues/new/choose">Request Feature</a>
</p>

Are you a shopping enthusiast on the hunt for fantastic online deals? Look no further – Shopsync is your ultimate ally in the quest for the best bargains! Shopsync is a publicly accessible web API framework designed for convenient price comparison across popular e-commerce platforms. It supports well-known websites such as Amazon, Walmart, Target, BestBuy, Costco, and eBay. Currently supported websites include [Amazon](https://www.amazon.com/), [Walmart](https://www.walmart.com/), [Target](https://www.target.com/), [BestBuy](https://www.bestbuy.com/), [Costco](https://www.costco.com/) and [EBay](https://www.ebay.com/).

The key benefits of using Shopsync are:

- **Efficiency**: By utilizing Shopsync, you can drastically reduce the time spent comparing deals on various websites, often saving more than 50% of your time.
- **Simplicity**: Shopsync offers user-friendly public APIs that simplify filtering, sorting, and searching for the best deals among search results.
- **Versatility**: It generates JSON responses that are highly adaptable, allowing you to easily tailor the output to suit your specific needs.

---

<p align="center">
  <a href="#movie_camera-checkout-our-video">Checkout our video</a>
  ::
  <a href="#rocket-installation">Installation</a>
  ::
  <a href="#computer-technology-used">Technology Used</a>
  ::
  <a href="#bulb-use-case">Use Case</a>
  ::
  <a href="#page_facing_up-why">Why</a>
  ::
  <a href="#golf-future-roadmap">Future Roadmap</a>
  ::
  <a href="#sparkles-contributors">Contributors</a>
  ::
  <a href="#Acknowledgement">Acknowledgement</a>
  ::
  <a href="#email-support">Support</a>
</p>

---

:movie_camera: Checkout our video
---

https://github.com/user-attachments/assets/3f7740ea-8326-4627-8c4f-3800d20a09fb

---

:blue_book: Project Documentation
---

[Link to Docs in REPO...](https://github.com/Neel317/ShopSync/tree/main/docs)

---

:rocket: Installation
---
1. Clone the Github repository to a desired location on your computer. You will need [git](https://git-scm.com/) preinstalled on your machine. Once the repository is cloned, you will then ```cd``` into the local repository.

    git clone https://github.com/Neel317/ShopSync.git

2. Build the local enviroment
   for mac
   make env: python3 -m venv venv
   run env : source venv/bin/activate

   for windows
   make env: python -m venv venv
   run env : venv\Scripts\activate

3. This project uses Python 3, so make sure that [Python](https://www.python.org/downloads/) and [Pip](https://pip.pypa.io/en/stable/installation/) are preinstalled. All requirements of the project are listed in the ```requirements.txt``` file. Use pip to install all of those.

    pip3 install -r requirements.txt

4. Once all the requirements are installed, you will have to ```cd``` into the ```src``` folder. Once in the ```src``` folder, use the python command to run the ```main.py``` file.
 
    cd src

    For Mac python3 main.py

    For Windows python main.py

5. To run the Streamlit application go on different terminal and go to frontend folder:
streamlit run app.py


:computer: Technology Used
---
![Streamlit](https://img.shields.io/badge/Streamlit-FF4F00?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=white)


## 🔄 Work Flow

<table border="2" bordercolorlight="#b9dcff" bordercolordark="#006fdd">
  <tr style="background: #010203 ">
    <td valign="top"> 
      <p style="color: #FF7A59"> Login Page
      </p>
      <a href="./media/Login.jpg"> 
        <img src="./media/Login.jpg" >      
      </a>
    </td>
    <td valign="top">
     <p style="color: #FF7A59"> Signup Page
      </p>
     <a href="./media/Signup.jpg">
        <img src="./media/Signup.jpg"> 
      </a> 
    </td>
  </tr>
  
  <tr style="background: #010203;"> 
    <td valign="top">
     <p style="color: #FF7A59"> Home
      </p>
     <a href="./media/Home.png">
        <img src="./media/Home.png"> 
      </a> 
    </td>
    <td valign="top"> 
      <p style="color: #FF7A59"> Favourites
      </p>
      <a href="./media/Favourites.png"> 
        <img src="./media/Favourites.png">      
      </a>
    </td>
  </tr>
</table>

---

:bulb: Use Case
---
- **User**: John, a shopping enthusiast, is looking for the best price for a smartphone across various e-commerce platforms.
- **Process**:
  1. John opens the Shopsync app and enters "smartphone" in the search bar.
  2. Shopsync fetches real-time data from multiple online retailers and displays the results.
  3. John filters the results by price and finds the best deal.
  4. He clicks the link to purchase the smartphone directly from the retailer's website.

:page_facing_up: Why
---
1. Shopping can be time-consuming, especially when comparing prices across different platforms. Shopsync aims to streamline this process, making it faster and more efficient.
2. The app's user-friendly interface allows users to easily navigate and find the best deals.
3. With Shopsync, users can save time and money, enhancing their online shopping experience.

Δ Deltas
Phase 5:
- [x] Implemented a robust user authentication system using Firestore for secure access and a personalized experience.
- [x] Added a dedicated favorites page, allowing users to store and manage preferred items with Firestore persistence.
- [x] Introduced comprehensive sorting and filtering options, including ascending/descending order and checkboxes for individual company filtering.
- [x] Implemented a reset button for users to quickly clear selections and start fresh.
- [x] Enhanced navigation with a sidebar feature for intuitive access to different sections of the application.
- [x] Significantly improved the user interface with consistent text sizes, interactive checkboxes, and filter buttons for a more engaging experience.

:golf: Future Roadmap
---
- Search History: Users can revisit previous searches for a convenient shopping experience.
- Cookies: Enhances user experience by remembering preferences and maintaining session information.
- Images for Items: Each item in search results includes images for better visual engagement.
- Remove from Favorites: Users can easily manage their favorites by removing items as needed.

:sparkles: Contributors
---
- **Devyash Shah** - [devyash2930](https://github.com/devyash2930)
- **Smit Raval** - [smitraval24 ](https://github.com/smitraval24)
- **Vatsal Patel** - [vatsal-dp](https://github.com/vatsal-dp)

---

:bulb: Acknowledgement
---
We would like to thank Professor Dr Timothy Menzies for helping us understand the process of building a good Software Engineering project. We would also like to thank the teaching assistants Liwen, Andre Lustosa, Sam Gilson, Rishabh Jain, and Amirali for their support throughout the project. We would also like to extend our gratitude to the previous groups: https://github.com/Kashika08/ShopSync and https://github.com/Neel317/ShopSync

https://streamlit.io/

https://shields.io/

:email: Support
---
For any inquiries, suggestions, or support requests, please contact us at [info@shopsync.com](mailto:info@shopsync.com).

