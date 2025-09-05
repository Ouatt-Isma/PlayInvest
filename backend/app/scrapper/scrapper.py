from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Set up Chrome options
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0")

def get(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Create a webdriver instance
    driver = webdriver.Chrome(options=options)


    # Open the page in the browser
    driver.get(url)

    html = driver.page_source
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table with historical data
    table = soup.find('table', {'class': 'freeze-column-w-1 w-full overflow-x-auto text-xs leading-4'})

    # Parse the rows of the table
    rows = table.find_all('tr')

    # Extract the first row (excluding the header) for the first date
    first_row = rows[1]  # Skip the header row

    # Extract the relevant columns: Date, Open (Ouv.), and Close (Dernier)
    columns = first_row.find_all('td')
    date = columns[0].text.strip()  # Date
    open_value = columns[1].text.strip()  # Open (Ouv.)
    close_value = columns[4].text.strip()  # Close (Dernier)

    # Print the values
    # print(f"Date: {date}")
    # print(f"Open (Ouv.): {open_value}")
    # print(f"Close (Dernier): {close_value}")
    date_obj = datetime.strptime(date, "%d/%m/%Y")

    # Format to new string format %Y-%m-%d
    formatted_date = date_obj.strftime("%Y-%m-%d")
    # Close the browser window
    driver.quit()
    
    return {"date": formatted_date, "open": float(open_value), "close": float(close_value)}

def test():
    print(get('https://fr.investing.com/equities/societe-generale-de-banques-historical-data'))