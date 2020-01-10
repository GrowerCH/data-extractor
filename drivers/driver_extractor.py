import re

from drivers.driver import Performance, Driver
from utils.extract_utils import init_browser


def start_driver_extractor():
    print("\nstarted loading drivers...")

    browser = init_browser()

    driver_data = extract_performances(browser)
    print("drivers done")

    browser.close()

    return driver_data


def extract_performances(browser):
    url = "https://www.jameco.com/jameco/content/Mean-Well-Constant-Current-PFC-LED-Driver.html"

    browser.get(url)

    table = browser.find_element_by_class_name("table-container")

    result = []
    current_driver = None
    for row in table.find_elements_by_tag_name("tr"):
        cells = row.find_elements_by_tag_name("td")

        if len(cells) == 1:
            model = cells[0].text.replace(" Series", "")

            if not re.match(r"(ELG|HLG|HVGC)-", model):
                current_driver = None
                continue

            current_driver = Driver(model, [])
            result.append(current_driver)
            print("done " + current_driver.model)
            continue

        if current_driver is None:
            continue

        if len(cells) == 8:

            product_code = cells[0].text
            if not product_code.endswith("B"):
                continue

            voltage = cells[3].text.split("-")
            min_voltage = float(voltage[0])
            max_voltage = float(voltage[1])
            current = float(cells[4].text)

            performance = Performance(current, min_voltage, max_voltage)
            current_driver.performances.append(performance)
    return result
