import yfinance as yf
from datetime import datetime, timedelta, date

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time 

def get_brvm_asset_investing(asset_keyword: str):
    url = "https://fr.investing.com/equities/ivory-coast"

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    
    try:
        driver.get(url)

        # 1. Accepter les cookies
        try:
            accept_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'I Accept')]"))
            )
            accept_btn.click()
        except:
            pass

        # 2. Attendre le tableau
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tr td"))
        )
        # print(driver.page_source)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find("table")
        if not table:
            driver.save_screenshot("debug.png")
            return {"error": "Table not found. Screenshot saved."}

        for row in table.select("tbody tr"):
            cols = row.select("td")
            if len(cols) >= 6:
                # 🧠 Correction : nom de l'actif est dans un <a title="...">
                name_tag = cols[1].find("a", title=True)
                if not name_tag:
                    continue
                asset_name = name_tag["title"].strip().lower()
                
                if asset_keyword.lower() in asset_name:
                    return {
                        "asset": asset_name,
                        "last_price": cols[2].text.strip(),
                        "high": cols[3].text.strip(),
                        "low": cols[4].text.strip(),
                        "variation": cols[5].text.strip(),
                        "variation_percent": cols[6].text.strip(),
                        "volume": cols[7].text.strip(),
                        "date": cols[8].text.strip()
                    }

        return {"error": f"Asset '{asset_keyword}' not found."}

    except Exception as e:
        driver.save_screenshot("error.png")
        return {"error": f"{str(e)}. Screenshot saved as error.png"}

    finally:
        driver.quit()



def get_open_close_price(ticker_symbol: str, date: str = None):
    """
    Fetch opening and closing prices for a given asset on Yahoo Finance.

    Parameters:
        ticker_symbol (str): The Yahoo Finance ticker (e.g., 'AAPL', 'BTC-USD').
        date (str): Date in 'YYYY-MM-DD' format. If None, defaults to yesterday.

    Returns:
        dict: { 'date': ..., 'open': ..., 'close': ... } or error message.
    """
    try:
        if date is None:
            date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        next_day = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        
        data = yf.download(ticker_symbol, start=date, end=next_day, progress=False)
        
        if data.empty:
            return {"error": "No data found for the given date or asset."}
        
        open_price = float(data['Open'].iloc[0].item())
        close_price = float(data['Close'].iloc[0].item())

        return {
            'date': date,
            'open': open_price,
            'close': close_price
        }

    except Exception as e:
        return {"error": str(e)}

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def scrap_brvm_company_all_stats(url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(5)  # attendre chargement JS

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        data = {}

        # ✅ Titre principal
        title = soup.find('h1')
        if title:
            data['name'] = title.text.strip()

        # ✅ Prix actuel
        price = soup.select_one('div[data-test="instrument-price-last"]')
        data['current_price'] = price.text.strip() if price else "N/A"

        # ✅ Variation
        change = soup.select_one('div[data-test="instrument-price-change"]')
        data['change'] = change.text.strip() if change else "N/A"

        # ✅ Résumé rapide (ex: rendement, BPA, capitalisation)
        stat_block = soup.find_all("div", class_="instrument-profile_overview__1uLqz")
        for block in stat_block:
            for row in block.select("div.instrument-profile_overview-row__1gq5z"):
                try:
                    label = row.select_one(".instrument-profile_overview-label__2upIh").text.strip()
                    value = row.select_one(".instrument-profile_overview-value__3pBmv").text.strip()
                    data[label] = value
                except:
                    continue

        # ✅ Statistiques détaillées (tableau en 2 colonnes)
        stats_section = soup.find_all("table")
        for table in stats_section:
            for row in table.find_all("tr"):
                try:
                    cols = row.find_all("td")
                    if len(cols) == 2:
                        label = cols[0].text.strip()
                        value = cols[1].text.strip()
                        data[label] = value
                except:
                    continue

        return data

    finally:
        driver.quit()

# def scrap_brvm_company_all_stats(url):
#     options = Options()
#     options.add_argument("--headless=new")  # You can comment this out for debugging
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--window-size=1920,1080")
#     options.add_argument("user-agent=Mozilla/5.0")

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     driver.set_page_load_timeout(15)  # Prevent infinite loading

#     try:
#         try:
#             driver.get(url)
#         except Exception as e:
#             print(f"[WARN] Page load timeout: {e} — proceeding with partial content")

#         # ✅ Wait only for key content (like the main title)
#         try:
#             WebDriverWait(driver, 15).until(
#                 EC.presence_of_element_located((By.TAG_NAME, "h1"))
#             )
#         except:
#             print("[WARN] Key element h1 not found — parsing anyway")

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         data = {}

#         # ✅ Main Title
#         title = soup.find('h1')
#         if title:
#             data['name'] = title.text.strip()

#         # ✅ Current Price
#         price = soup.select_one('div[data-test="instrument-price-last"]')
#         data['current_price'] = price.text.strip() if price else "N/A"

#         # ✅ Price Change
#         change = soup.select_one('div[data-test="instrument-price-change"]')
#         data['change'] = change.text.strip() if change else "N/A"

#         # ✅ Overview block (Rendement, PER, etc.)
#         stat_block = soup.find_all("div", class_="instrument-profile_overview__1uLqz")
#         for block in stat_block:
#             for row in block.select("div.instrument-profile_overview-row__1gq5z"):
#                 try:
#                     label = row.select_one(".instrument-profile_overview-label__2upIh").text.strip()
#                     value = row.select_one(".instrument-profile_overview-value__3pBmv").text.strip()
#                     data[label] = value
#                 except:
#                     continue

#         # ✅ Detailed Stats from Tables
#         stats_section = soup.find_all("table")
#         for table in stats_section:
#             for row in table.find_all("tr"):
#                 try:
#                     cols = row.find_all("td")
#                     if len(cols) == 2:
#                         label = cols[0].text.strip()
#                         value = cols[1].text.strip()
#                         data[label] = value
#                 except:
#                     continue

#         # ✅ Optional: Stats in mb-[30px] block
#         key_stats_section = soup.find("div", class_="mb-[30px] flex flex-col items-start gap-5")
#         if key_stats_section:
#             for row in key_stats_section.find_all("div", recursive=False):
#                 try:
#                     all_spans = row.find_all(["span", "div", "p", "strong"])
#                     texts = [s.text.strip() for s in all_spans if s.text.strip()]
#                     if len(texts) >= 2:
#                         label = texts[0]
#                         value = texts[1]
#                         data[label] = parse_stats_text(value)
#                 except:
#                     continue

#         return data

#     finally:
#         driver.quit()

# import requests
# from bs4 import BeautifulSoup

def scrap_brvm_company_selenium(url):
    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0")

    print(10)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print(10)   
    # driver.set_page_load_timeout(10)
    try:
        driver.get(url)
        # time.sleep(5)  # Laisser le temps au JS de charger
        print(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print(20)
        data = {}

        # ✅ Nom de l’entreprise
        title = soup.find('h1')
        print(0)
        if title:
            data['name'] = title.text.strip()

        # ✅ Prix actuel
        price = soup.select_one('div[data-test="instrument-price-last"]')
        data['current_price'] = price.text.strip() if price else "N/A"

        # ✅ Variation
        change = soup.select_one('div[data-test="instrument-price-change"]')
        data['change'] = change.text.strip() if change else "N/A"

        # ✅ Infos complémentaires dans la fiche
        stat_block = soup.find_all("div", class_="instrument-profile_overview__1uLqz")
        print(00)
        for block in stat_block:
            for row in block.select("div.instrument-profile_overview-row__1gq5z"):
                try:
                    label = row.select_one(".instrument-profile_overview-label__2upIh").text.strip()
                    value = row.select_one(".instrument-profile_overview-value__3pBmv").text.strip()
                    data[label] = value
                except:
                    continue

        print(1)
        # ✅ Statistiques clés depuis le bloc mb-[30px]...
        key_stats_section = soup.find("div", class_="mb-[30px] flex flex-col items-start gap-5")
        if key_stats_section:
            for row in key_stats_section.find_all("div", recursive=False):
                print(2)
                try:
                    all_spans = row.find_all(["span", "div", "p", "strong"])
                    texts = [s.text.strip() for s in all_spans if s.text.strip()]
                    if len(texts) >= 1:
                        
                        label = texts[0]
                        # print()
                        value = texts[1]
                        # print(value)
                        # print(label)
                        # print("1")
                        data.update(parse_open_close(texts[0]))
                        # print("22")
                        data.update(parse_open_close(texts[1]))
                        # print("ici")
                        # print(data)
                        # print("ici fin")
                        if "close" in data and "open" in data:
                            break
                except:
                    continue
            
        # print(data)
        res = {}
        res["date"] = datetime.now().strftime("%Y-%m-%d")
        res["open"] = data['open']
        res["close"] = data['close']
        
        return res
    finally:
        driver.quit()

import re

def parse_stats_text(raw_text):
    # Supprimer les mentions inutiles
    text = raw_text.replace("Modifier", "").replace("Débloquer", "").replace("Voir plus:", "").strip()

    # Liste des labels connus qu'on veut extraire (adapté à Investing.com BRVM)
    labels = [
        "Clôture précédente", "Ouverture", "Ecart journalier", "Ecart 52 sem.",
        "Volume", "Volume moyen", "Variation sur 1 an", "Valeur comptable / Action",
        "Capitalisation", "Act. en circulation", "Chiffre d'affaires", "Résultat net",
        "BPA", "Dividende", "PER", "Rendement des Actifs", "Rendement des fonds propres",
        "Ratio P/B", "RSI", "ISIN"
    ]

    data = {}
    for label in labels:
        pattern = rf"{label}\s*([^\n\r:]+)"
        match = re.search(pattern, text)
        if match:
            data[label] = match.group(1).strip()

    return data

def parse_open_close(raw_text):
    # Remove unnecessary spaces
    text = raw_text.replace("\n", "").strip()

    data = {}

    # Patterns for close and open
    match_close = re.search(r"Clôture précédente\s*([\d.,KMBT]+)", text)
    match_open  = re.search(r"Ouverture\s*([\d.,KMBT]+)", text)

    if match_close:
        data["open"] = match_close.group(1).replace(",", ".")
    if match_open:
        data["close"] = match_open.group(1).replace(",", ".")
    return data

def test_open_close():
    result = get_open_close_price('CEU.PA', '2024-11-01')
    print(result)
def test_get_brvm_asset_investing():
    print(get_brvm_asset_investing("Bank of Africa Cote d’Ivoire"))
    
def test_sib():
    url = "https://fr.investing.com/equities/societe-ivoirienne-de-banque-sa"
    import time 
    print("start")
    deb = time.time()
    info = scrap_brvm_company_selenium(url)
    print("end")
    for key, value in info.items():
        print(f"{key}: {value}")

# test_sib()