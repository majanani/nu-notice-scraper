import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# আপনার গুগল ওয়েব অ্যাপ ইউআরএল
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzcDyJZ2W_pKUzcLkQfKPvRlW06og5mdJc-3hDMmfGLJvb0uj15GqnAmlbb0O8pCytW9Q/exec"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

tabs_to_check = [
    {"name": "Honours", "xpath": "//a[contains(text(), 'Honours')]"},
    {"name": "Degree Pass", "xpath": "//a[contains(text(), 'Degree Pass')]"},
    {"name": "Masters", "xpath": "//a[contains(text(), 'Master\'s/M.Phil/Ph.D/PGD')]"}
]

try:
    driver.get("http://app11.nu.edu.bd/")
    time.sleep(5)
    
    for tab in tabs_to_check:
        print(f"Checking Tab: {tab['name']}")
        try:
            tab_element = driver.find_element(By.XPATH, tab["xpath"])
            driver.execute_script("arguments[0].click();", tab_element)
            time.sleep(3)
            
            rows = driver.find_elements(By.CSS_SELECTOR, "table.table tr, table tr")
            
            for i in range(1, min(len(rows), 31)):
                cols = rows[i].find_elements(By.TAG_NAME, "td")
                if len(cols) >= 3:
                    title = cols[1].text.strip()
                    date = cols[2].text.strip()
                    
                    try:
                        link_element = rows[i].find_element(By.TAG_NAME, "a")
                        link = link_element.get_attribute("href")
                    except:
                        link = ""
                    
                    if link and ".pdf" in link:
                        payload = {'titleEn': title, 'date': date, 'link': link}
                        response = requests.get(WEB_APP_URL, params=payload)
                        print(f"Processed: {title} -> Status: {response.text}")
                        
        except Exception as tab_err:
            print(f"Error processing tab {tab['name']}: {tab_err}")

finally:
    driver.quit()
    print("Scraping Completed.")