# Redbus Data Scarping
A Streamlit application for scraping and filtering bus travel data from Redbus. Automates data extraction of routes, schedules, prices, and seat availability using Selenium.

In ***data_scraping.ipynb*** scrape bus details include 10 Government state buses and store the collected data from selenium and store it into csv file. In ***data_preprocessing.ipynb*** preprocess the data 
from csv file, like check for missing values and duplicated rows and remove the duplicate and missing data. Connect MySQL database with PyMySQL if database and table is already exists then use the database and table
else create new database and table and insert the data to database. 

In ***streamlit_app.py*** get information from database and use the data to filter the bus details and information.

1. **Clone the repository**:
   
   ```bash
   git clone https://github.com/sethu45/redbus-data-scarping.git
   cd redbus-data-scarping
   
2. **Set up a virtual environment**:
   
   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt

4. **Run the Streamlit application**:
   
   ```bash
   streamlit run app.py

