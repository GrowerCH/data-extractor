import json

from leds.led import LED, Version
from modules.module_extractor import get_needed_led_cct_cri
from utils.extract_utils import read_text_from_url, extract_json_from_text


def start_led_extractor(module_data):
    print("\nstarted loading leds...")

    url = "https://www.samsung.com/etc/designs/led/global/business/calculator/component-calculator-control/js/data.js"

    text = read_text_from_url(url)
    json_text = extract_json_from_text(text)

    led_data = json.loads(json_text[0])
    version_data = json.loads(json_text[1])
    performance_data = json.loads(json_text[2])

    needed = get_needed_led_cct_cri(module_data)

    led_data = list(extract_important_led_data(led_data, version_data, performance_data, needed))
    print("leds done")

    return led_data


def extract_important_led_data(led_data, version_data, performance_data, needed):
    for data in led_data:

        name = data["Name"]
        if name not in needed["led"]:
            continue

        index = int(data["Index"])
        max_current = float(data["IF_max"])
        versions = []

        yield LED(name, max_current, versions)

        for version in version_data:
            if version["Name"] != name:
                continue

            cct = int(version["CCT"])
            cri = int(version["CRI"])
            if cri not in needed["cri"]:
                continue

            voltage = float(version["VfRank2"])
            flux = float(version["FluxRank2"])

            code_index = index * cct * cri + cct + cri

            performance = None
            for performances in performance_data:
                if int(performances["CodeIndex"]) == code_index:
                    performance = performances

            versions.append(
                Version(cct, cri, voltage, flux, None, performance))
