import json
import os
from time import sleep

from bs4 import BeautifulSoup
import requests


data_path = os.path.join(
    os.path.dirname(__file__), "..", "versiontracker", "data.json")


def download(url):
    """Returns the content at the specified URL.

    The target content must be a text file, it cannot be binary content.

    This method retries downloads up to 3 times before it gives up and it
    raises an exception.

    Communications using this method do no check that the target server has a
    valid SSL certificate. You should never use this method if your URL
    includes sensitive information, such as passwords.
    """
    time_to_sleep = 15
    maximum_failed_attempts = 3
    failed_attempts = 0
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:48.0) "
                      "Gecko/20100101 Firefox/48.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;"
                  "q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }
    while True:
        try:
            return requests.get(
                url, headers=headers, timeout=32, verify=False).text
        except (requests.exceptions.ChunkedEncodingError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout):
            failed_attempts += 1
            if failed_attempts >= maximum_failed_attempts:
                raise
            sleep(time_to_sleep)
            time_to_sleep *= 2


def download_as_soup(url):
    """Downloads the HTML file at the specified URL and returns an instance of
    BeautifulSoup that wraps it.

    This method retries downloads up to 3 times before it gives up and it
    raises an exception.

    Communications using this method do no check that the target server has a
    valid SSL certificate. You should never use this method if your URL
    includes sensitive information, such as passwords.
    """
    return html_to_soup(download(url))


def html_to_soup(html):
    """Returns a BeautifulSoup object for the specified HTML content.

    The `lxml` parser of BeautifulSoup is used.
    """
    return BeautifulSoup(html, "lxml")


def load_data():
    with open(data_path) as f:
        return json.load(f)


def save_data(data):
    with open(data_path, "w") as f:
        json.dump(data, f, indent=4, separators=(",", ": "))
        f.write('\n')
