from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def get_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # Runs browser in background
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def search_leads(role, company):
    driver = get_browser()
    search_query = f'site:linkedin.com/in/ "{role}" "{company}"'
    driver.get(f"https://www.google.com/search?q={search_query}")
    
    time.sleep(2) # Let page load
    results = []
    links = driver.find_elements(By.CSS_SELECTOR, "div.g a")
    
    for link in links[:5]: # Take top 5 results
        url = link.get_attribute("href")
        if "linkedin.com/in/" in url:
            results.append({"company": company, "url": url})
            
    driver.quit()
    return results