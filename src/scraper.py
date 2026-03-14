import time
import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from src.parser import count_properties, get_properties, extract_properties_data


BASE_URL = "https://www.openrent.co.uk/properties-to-rent"

AREAS = {
    "Camden": "camden",
}

# AREAS = {
#     "Camden": "camden",
#     "Hackney": "hackney",
#     "Islington": "islington",
#     "Westminster": "westminster",
#     "Kensington and Chelsea": "kensington-and-chelsea",
#     "Hammersmith and Fulham": "hammersmith-and-fulham",
#     "Southwark": "southwark",
#     "Tower Hamlets": "tower-hamlets",
#     "Greenwich": "greenwich",
#     "Ealing": "ealing",
#     "Wandsworth": "wandsworth",
#     "Haringey": "haringey",
#     "Brent": "brent",
#     "Barnet": "barnet",
#     "Lewisham": "lewisham",
#     "Merton": "merton",
#     "Newham": "newham",
#     "Lambeth": "lambeth",
#     "Redbridge": "redbridge",
#     "Bromley": "bromley"
# }


def fetch_page(url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1400,2000")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(url)
        time.sleep(5)

        previous_count = 0
        same_count_rounds = 0

        for i in range(15):
            cards = driver.find_elements("css selector", "a.pli.search-property-card")
            current_count = len(cards)

            print(f"scroll {i+1}: {current_count} cards")

            if current_count == previous_count:
                same_count_rounds += 1
            else:
                same_count_rounds = 0

            if same_count_rounds >= 3:
                break

            previous_count = current_count

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        return driver.page_source

    finally:
        driver.quit()


def run_scraper():
    all_data = []

    for area_name, area_path in AREAS.items():
        url = f"{BASE_URL}/{area_path}"

        html = fetch_page(url)

        count = count_properties(html)
        print(f"{area_name}: {count} properties")

        properties = get_properties(html)

        for prop in properties:
            data = extract_properties_data(prop, area_name)

            if data is not None and data["rent"] is not None and data["beds"] is not None:
                all_data.append(data)

    with open("data/raw_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["area", "rent", "beds"])

        for row in all_data:
            writer.writerow([row["area"], row["rent"], row["beds"]])

    print("saved to data/raw_data.csv")
