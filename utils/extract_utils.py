import json
import os
import re

import requests
from selenium import webdriver


def read_text_from_url(url):
    return requests.get(url).text


def extract_json_from_text(text):
    return re.findall(r"TAFFY\('?(.+?)'?\);", text, re.DOTALL)


def save_data_to_file(data, file_name):
    with open(file_name, "w") as file:
        json.dump(data, file, default=lambda o: o.__dict__)


def load_json_from_file(file_name):
    with open(file_name) as file:
        return json.load(file)


def init_browser():
    os.environ["MOZ_HEADLESS"] = "1"

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False)

    browser = webdriver.Firefox(profile)

    return browser
