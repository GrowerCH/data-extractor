import json
import re

import requests

from leds.led import LED


def start_led_extractor():
    print("\nstarted loading leds...")

    url = "https://www.samsung.com/etc/designs/led/global/business/calculator/component-calculator-control/js/data.js"
    text = read_text_from_url(url)
    text_json = extract_led_json(text)
    data_json = json.loads(text_json[0])

    result = list(extract_led_data(data_json))
    print(json.dumps(result, default=lambda o: o.__dict__))


def read_text_from_url(url):
    return requests.get(url).text


def extract_led_json(text):
    return re.findall(r"TAFFY\((.+?)\);", text, re.DOTALL)


def extract_led_data(data_json):
    for led in data_json:
        name = led["Name"].replace("(", " ").replace(")", "")
        max_current = float(led["IF_max"])

        yield LED(name, max_current, [])

        print("done " + name)
