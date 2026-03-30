from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import time
import os
from dotenv import load_dotenv
from discordwebhook import Discord

load_dotenv()

def headless_scrape(url, latitude, longitude):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": 100
    })

    found = False

    try:
        driver.get(url)
        time.sleep(3)

        params = parse_qs(urlparse(url).query)
        if "fromdate" in params:
            target = datetime.strptime(params["fromdate"][0], "%Y-%m-%d")
            target_day = str(target.day)
            date_items = driver.find_elements(By.CSS_SELECTOR, "[class*='DatesMobileV2_cinemaDates']")
            for d in date_items:
                if d.text.split("\n")[0] == target_day:
                    driver.execute_script("arguments[0].click();", d)
                    time.sleep(3)
                    break

        imax = driver.find_elements(By.CSS_SELECTOR, ".MDPFilterPills_filterPill__HNE8k")

        for i in imax:
            if "IMAX" in i.text:
                print(f"IMAX available: {i.text}")
                found = True
                break
            else:
                print("IMAX not available")

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()
        return found

def loop_scarpe(url, latitude, longitude, delay, notification, discord_webhook):
    number = 0

    discord = Discord(url=discord_webhook)

    while True:
        print(f"Pass {number}")
        found = headless_scrape(url, latitude, longitude)
        number = number + 1
        if(found):
            discord.post(content=notification)
            break

        time.sleep(delay)


if __name__ == "__main__":
    url = os.getenv("SCRAPE_URL")
    latitude = float(os.getenv("LATITUDE"))
    longitude = float(os.getenv("LONGITUDE"))
    delay = int(os.getenv("DELAY"))
    discord_webhook = os.getenv("DISCORD_WEBHOOK")
    notification = os.getenv("NOTIFICATION")

    loop_scarpe(url, latitude, longitude, delay, notification, discord_webhook)