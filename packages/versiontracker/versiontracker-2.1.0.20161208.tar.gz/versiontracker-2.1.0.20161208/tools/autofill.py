"""Given a list of package names, it attempts to fill `data.json` with entries
for them based on non-generic built-in spiders."""

from collections import OrderedDict
import re

import requests

from tools.common import load_data, save_data, download_as_soup
from tools.lint import main as lint


_PYTHON_RE = re.compile(r"^py(?:thon[23]?-)?(.*)")


def github(software_id, software_ids_in_use):
    if software_id.startswith('python'):
        return
    url = "https://github.com/search?utf8=%E2%9C%93&q=" + software_id
    soup = download_as_soup(url)
    item = soup.find("li", "repo-list-item")
    if not item:
        return
    parts = item.h3.a['href'].split('/')
    if parts[-1].lower() != software_id:
        return
    favorite_count = int(
        item.find("a", {"aria-label": "Stargazers"}).get_text().replace(
            ",", ""))
    if favorite_count < 8:
        return  # Not popular enough.
    project = parts[-2]
    url = "https://github.com/{}/{}/tags".format(project, software_id)
    soup = download_as_soup(url)
    if not soup.find("span", "tag-name"):
        return
    entry = {
        "spider": {
            "name": "github"
        }
    }
    if project != software_id:
        entry['spider']['project'] = project
    return software_id, entry


def kde_for_id(software_id, software_ids_in_use):
    soup = download_as_soup("https://quickgit.kde.org/?p={}.git".format(
        software_id))
    for a in soup.find_all("a", "title"):
        if a.string.strip() == "tags":
            return software_id, {
                "spider": {
                    "name": "gitkde"
                }
            }


def kde(software_ids_in_use):
    soup = download_as_soup("https://quickgit.kde.org/")
    software_ids = [td.span.string.strip()[:-4]
                    for td in soup.find_all("td", "projectName")]
    unused_software_ids = [id for id in software_ids
                           if id not in software_ids_in_use]
    for software_id in unused_software_ids:
        if "/" in software_id:
            return  # Reached clones.
        entry = kde_for_id(software_id)
        if entry:
            yield software_id, entry[1]


def launchpad(software_id, software_ids_in_use):
    if software_id.startswith('python'):
        return
    url = "https://launchpad.net/" + software_id
    if requests.head(url).status_code != 200:
        return
    soup = download_as_soup(url)
    if soup.find("div", "version"):
        return software_id, {
            "spider": {
                "name": "launchpad"
            }
        }


def pypi(software_id, software_ids_in_use):
    url = "https://pypi.python.org/pypi/" + software_id
    if requests.head(url).status_code == 200:
        return software_id, {
            "spider": {
                "name": "pypi"
            }
        }
    match = _PYTHON_RE.search(software_id)
    if not match:
        return
    actual_software_id = match.group(1)
    if not actual_software_id:
        return
    if actual_software_id in software_ids_in_use:
        return
    url = "https://pypi.python.org/pypi/" + actual_software_id
    if requests.head(url).status_code == 200:
        return actual_software_id, {
            "spider": {
                "name": "pypi"
            }
        }


def sourceforge(software_id, software_ids_in_use):
    if software_id.startswith('python'):
        return
    url = "https://sourceforge.net/projects/{}/files/".format(software_id)
    if requests.head(url).status_code != 200:
        return
    soup = download_as_soup(url)
    if soup.find("div", "download-bar"):
        return software_id, {
            "spider": {
                "name": "sourceforge"
            }
        }


# Sorted by guessed chance of getting a match.
_ENTRY_BUILDERS_FOR_ID = OrderedDict((
    ("GitHub", github),
    ("SourceForge", sourceforge),
    ("Launchpad", launchpad),
    ("PyPI", pypi),
    ("KDE Git", kde_for_id),
))
_STANDALONE_ENTRY_BUILDERS = {
    "KDE Git": kde,
}


def main(software_ids=()):
    data = load_data()
    existing_software_ids = list(data.keys())
    if software_ids:
        for software_id in software_ids:
            if software_id in existing_software_ids:
                continue
            for source, entry_builder in _ENTRY_BUILDERS_FOR_ID.items():
                entry = entry_builder(software_id, existing_software_ids)
                if not entry:
                    continue
                actual_software_id, entry = entry
                data[actual_software_id] = entry
                existing_software_ids.append(actual_software_id)
                if actual_software_id == software_id:
                    print(u"Generated an entry for '{}' based on '{}'.".format(
                        software_id, source))
                else:
                    print(u"Generated an entry for '{}' ('{}') based on "
                          u"'{}'.".format(
                        software_id, actual_software_id, source))
    else:
        for source in sorted(_STANDALONE_ENTRY_BUILDERS.keys()):
            entry_builder = _STANDALONE_ENTRY_BUILDERS[source]
            for software_id, entry in entry_builder(existing_software_ids):
                data[software_id] = entry
                existing_software_ids.append(software_id)
                print(u"Generated an entry for '{}' based on '{}'.".format(
                    software_id, source))
    save_data(data)
    lint()


if __name__ == "__main__":
    from sys import argv
    software_ids = ()
    if len(argv) == 2:
        with open(argv[1]) as f:
            software_ids = tuple(line.strip() for line in f)
    main(software_ids)
