import json
import os
import re
import time

import requests
from selenium import webdriver

from modules.module import Module, Dimensions, Version
from modules.performance_calculator import calculate_performance


def start_module_extractor(currents):
    print("\nstarted loading modules...")

    browser = init_browser()

    url = "https://www.samsung.com/etc/designs/led/global/business/calculator/engine-calculator-control/js/data.js"
    text = read_text_from_url(url)
    text_json = extract_module_json(text)

    modules_json = json.loads(text_json[0])
    products_json = json.loads(text_json[1])

    result = list(extract_module_data(products_json, modules_json, currents, browser))
    print(json.dumps(result, default=lambda o: o.__dict__))

    browser.close()


def read_text_from_url(url):
    return requests.get(url).text


def extract_module_json(text):
    return re.findall(r"TAFFY\(\'(.*)\'\)", text)


def extract_module_data(products_json, modules_json, currents, browser):
    for module in modules_json:
        model = module["Model"]
        model_index = module["ModelIndex"]

        led = module["InstalledLed"]

        max_current = float(module["MaxIf"])

        parallel_number = int(float(module["ParallelNumber"]))
        series_number = int(float(module["seriesNumber"]))

        dimensions = extract_dimensions(module["Size"])

        versions = []

        yield Module(model, led, parallel_number, series_number, dimensions, versions)
        print("done " + model)

        for product in products_json:

            if product["ModelIndex"] != model_index:
                continue

            product_code = product["ProductCode"]

            cct = int(float(product["CCT"]))
            cri = int(float(product["CRI"]))

            price = load_price(browser, product_code)
            time.sleep(1)

            performances = calculate_performances(product, module, currents, max_current)

            versions.append(
                Version(product_code, cct, cri, price, performances))


def get_module_from_index(modules, model_index):
    for module in modules:
        if module["ModelIndex"] == model_index:
            return module


def calculate_performances(product, module, currents, max_current):
    performances = []
    for current in currents:
        if current > max_current:
            break
        performance = calculate_performance(module, product, current)
        performances.append(performance)

    return performances


def extract_dimensions(text):
    regex = re.findall(r"(\d+(?:\.\d+)?)\((?:L|W|D)\)", text)
    length = float(regex[0])
    width = length
    if len(regex) == 2:
        width = float(regex[1])
    return Dimensions(length, width)


def init_browser():
    os.environ["MOZ_HEADLESS"] = "1"
    browser = webdriver.Firefox()
    return browser


def load_price(browser, product_code):
    url = "https://octopart.com/search?q=" + product_code
    browser.get(url)

    table = browser.find_element_by_class_name("serp-part-card")

    lowest_price = 9999
    for row in table.find_elements_by_tag_name("tr"):
        seller = row.get_attribute("data-seller")
        if seller:
            price_cell = row.find_elements_by_class_name("col-price")[1]
            price = float(price_cell.get_attribute("data-price"))
            if not price == -1 and price < lowest_price:
                lowest_price = price

    if lowest_price != 9999:
        return lowest_price
