import time

from utils.extract_utils import init_browser


def start_price_extractor(module_data):
    print("\nstarted loading prices...")

    browser = init_browser()

    for module in module_data:
        for version in module["versions"]:
            price = load_price_from_octopart(browser, version["product_code"])
            if price:
                version["price"] = price
        print("done " + module["model"])

    print("prices done")

    browser.close()

    return module_data


def load_price_from_octopart(browser, product_code):
    url = "https://octopart.com/search?q=" + product_code
    browser.get(url)
    time.sleep(1)

    div = browser.find_element_by_class_name("serp-wrap-all")

    if len(div.find_elements_by_class_name("nrf-alert")) > 0:
        return

    table = div.find_element_by_class_name("serp-part-card")

    lowest_price = 99999
    for row in table.find_elements_by_tag_name("tr"):

        if not row.get_attribute("data-seller"):
            continue

        class_name = row.get_attribute("class")
        if "sibling" in class_name or "belowFold" in class_name:
            continue

        available_text = row.find_element_by_class_name("col-avail").text.replace(",", "")
        if available_text == "" or int(available_text) <= 0:
            continue

        price_cell = row.find_elements_by_class_name("col-price")[1]
        price = float(price_cell.get_attribute("data-price"))
        if not price == -1 and price < lowest_price:
            lowest_price = price

    if lowest_price != 99999:
        return lowest_price
