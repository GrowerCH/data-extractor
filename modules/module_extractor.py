import json
import re

from modules.module import Module, Dimensions, Version
from utils.extract_utils import read_text_from_url, extract_json_from_text


def start_module_extractor(selected_leds):
    print("\nstarted loading modules...")

    url = "https://www.samsung.com/etc/designs/led/global/business/calculator/engine-calculator-control/js/data.js"
    text = read_text_from_url(url)
    json_text = extract_json_from_text(text)

    modules_data = json.loads(json_text[0])
    products_data = json.loads(json_text[1])

    module_data = list(extract_module_data(products_data, modules_data, selected_leds))
    print("modules done")

    return module_data


def extract_module_data(product_data, module_data, selected_leds):
    for module in module_data:
        model = module["Model"]
        seller = "Samsung"
        model_index = module["ModelIndex"]

        led = module["InstalledLed"]
        if led not in selected_leds:
            continue

        parallel_count = int(float(module["ParallelNumber"]))
        series_count = int(float(module["seriesNumber"]))

        dimensions = extract_dimensions(module["Size"])

        versions = []

        yield Module(model, seller, led, parallel_count, series_count, dimensions, versions)

        for product in product_data:

            if product["ModelIndex"] != model_index:
                continue

            product_code = product["ProductCode"]

            cct = int(float(product["CCT"]))
            cri = int(float(product["CRI"]))

            versions.append(
                Version(product_code, cct, cri))


def extract_dimensions(text):
    regex = re.findall(r"(\d+(?:\.\d+)?)\((?:L|W|D)\)", text)
    length = float(regex[0])
    width = length
    if len(regex) == 2:
        width = float(regex[1])
    return Dimensions(length, width)


def get_needed_led_cct_cri(module_data):
    result = {"led": [], "cct": [], "cri": []}
    for module in module_data:

        led = module["led"]
        if led not in result["led"]:
            result["led"].append(led)

        for version in module["versions"]:

            cct = version["cct"]
            if cct not in result["cct"]:
                result["cct"].append(cct)

            cri = version["cri"]
            if cri not in result["cri"]:
                result["cri"].append(cri)
    return result
