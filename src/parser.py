from bs4 import BeautifulSoup
import re


def count_properties(html):
    soup = BeautifulSoup(html, "lxml")
    properties = soup.select("a.pli.search-property-card")
    return len(properties)


def get_properties(html):
    soup = BeautifulSoup(html, "lxml")
    properties = soup.select("a.pli.search-property-card")
    return properties


def extract_properties_data(prop, area):
    text = prop.get_text(" ", strip=True)

    if "let agreed" in text.lower():
        return None

    price_tag = prop.select_one("span.text-primary")
    price = None

    if price_tag:
        price_text = price_tag.text
        match = re.search(r"£([\d,]+)", price_text)
        if match:
            price = int(match.group(1).replace(",", ""))

    if "studio" in text.lower():
        beds = 0
    else:
        match = re.search(r"(\d+)\s*beds?", text, re.IGNORECASE)
        if match:
            beds = int(match.group(1))
        else:
            beds = None

    return {
        "area": area,
        "rent": price,
        "beds": beds
    }