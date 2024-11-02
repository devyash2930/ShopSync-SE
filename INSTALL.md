# Installation Guide for ShopSync

Welcome to the installation guide for ShopSync! Follow these steps to set up the project on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Git](https://git-scm.com/) for cloning the repository.
- [Python](https://www.python.org/downloads/) (below version 3.12 and above 3.10 ) for running the application.
- [Pip](https://pip.pypa.io/en/stable/installation/) for managing Python packages.

## Steps to Install

1. Clone the Github repository to a desired location on your computer. You will need git preinstalled on your machine. Once the repository is cloned, you will then cd into the local repository.

    git clone https://github.com/devyash2930/ShopSync-SE.git

2. Build the local enviroment for mac make env: python3 -m venv venv run env : source venv/bin/activate

    for windows 
    make env: python -m venv venv 
    run env : venv\Scripts\activate

3. This project uses Python 3, so make sure that Python and Pip are preinstalled. All requirements of the project are listed in the requirements.txt file. Use pip to install all of those.

    pip3 install -r requirements.txt

4. Once all the requirements are installed, you will have to cd into the src folder. Once in the src folder, use the python command to run the main.py file.

    cd src

    For Mac python3 main.py

    For Windows python main.py

5. To run the Streamlit application go on different terminal and go to frontend folder:
   
    streamlit run app.py
