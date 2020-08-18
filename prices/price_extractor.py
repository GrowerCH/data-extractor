import time

from selenium.common.exceptions import NoSuchElementException

from modules.module import ModulePrice
from utils.extract_utils import init_browser


def start_price_extractor(module_data, old_module_data):
    print("\nstarted loading prices...")

    browser = init_browser()

    price_list = []

    for module in module_data:
        for version in module["versions"]:
            product_code = version["product_code"]

            price = load_price_from_octopart(browser, product_code)
            if price:
                version["price"] = price

                led_count = module["parallel_count"] * module["series_count"]
                identifier = module["model"] + " " + str(version["cct"]) + "K (" + module["led"] + ")"
                price_list.append(ModulePrice(identifier, price / led_count))

            print_old_price(old_module_data, product_code, price)

        print("done " + module["model"])

    print("prices done")

    print("=====[Sorted price/diode]=====")
    for element in sorted(price_list, key=lambda x: x.diode_price):
        print(element.identifier + " > " + str(int(element.diode_price * 1000) / 1000) + " €")
    print("==============================")

    browser.close()

    return module_data


def print_old_price(old_module_data, code, price):
    old_price = None
    for module in old_module_data:
        for version in module["versions"]:
            if version["product_code"] != code:
                continue
            if "price" in version:
                old_price = version["price"]
                break

    if price:
        if old_price:
            diff = price - old_price
            print(code + ": " + ("+" if diff >= 0 else "") + str(diff))
        else:
            pass
            print(code + ": >" + str(price))
    else:
        pass
        print(code + ": <")


DOLLAR_TO_EURO_CONVERSION = 0.84


def load_price_from_octopart(browser, product_code):
    url = "https://octopart.com/search?q=" + product_code
    browser.get(url)
    time.sleep(3)

    try:
        browser.find_element_by_id("px-captcha")
        input("Captcha Alarm! Press Enter to continue...")
        print("Continuing.")
    except NoSuchElementException:
        pass

    try:
        browser.find_element_by_xpath("//div[contains(@class, 'no-results-found')]")
        return
    except NoSuchElementException:
        pass

    div = browser.find_element_by_xpath("//div[contains(@class, 'prices-view')]")

    try:
        table = div.find_element_by_tag_name("tbody")
    except NoSuchElementException:
        return

    lowest_price = 99999
    for row in table.find_elements_by_tag_name("tr"):

        cells = row.find_elements_by_tag_name("td")

        stock = int(cells[3].text.replace(".", ""))
        if stock < 1:
            continue

        price_text = cells[8].text.replace(",", ".")
        if not price_text:
            continue

        price = float(price_text)
        if price < lowest_price:
            lowest_price = price

    if lowest_price != 99999:
        return lowest_price * DOLLAR_TO_EURO_CONVERSION
