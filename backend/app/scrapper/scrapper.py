from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
# from app.utils.conv import to_float_inv
import tempfile 
# Set up Chrome options
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0")
profile_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={profile_dir}")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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
    
    # return {"date": formatted_date, "open": to_float_inv(open_value), "close": to_float_inv(close_value)}


def clean_number(value):
    """Convert Sika formatted numbers like '25 950' to float 25950.0"""
    value = value.replace('\xa0', '').replace(' ', '')
    if value in ["-", ""]:
        return None
    return float(value)

def get_sika(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(url)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    # The correct table for the historical data
    table = soup.find("table", {"id": "tblhistos"})
    if table is None:
        raise Exception("Historical table not found")

    rows = table.find_all("tr")
    if len(rows) < 2:
        raise Exception("No data rows found")

    # First data row (after header)
    first_row = rows[1]
    columns = first_row.find_all("td")

    date_str = columns[0].text.strip()
    close_value = columns[1].text.strip()     # Clôture
    open_value = columns[4].text.strip()      # Ouverture

    # Convert date
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")

    return {
        "date": formatted_date,
        "open": clean_number(open_value),
        "close": clean_number(close_value)
    }
def test():
    # print(get_sika('https://fr.investing.com/equities/societe-generale-de-banques-historical-data'))
    print(get_sika("https://www.sikafinance.com/marches/historiques/SNTS.sn"))