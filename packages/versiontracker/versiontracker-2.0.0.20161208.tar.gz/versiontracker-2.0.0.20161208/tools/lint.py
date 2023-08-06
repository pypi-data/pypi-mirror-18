from collections import OrderedDict
import re

from tools.common import download_as_soup, load_data, save_data


_formatter = 'formatter'
_name = 'name'
_spider = 'spider'
_url = 'url'


def main():
    old_data = load_data()
    sorted_keys = [
        'project',
        'repository',
        _url, 'path', 'tag', 'commit', 'package',
        'base',
        'version',
        'date', 'date-url',
        'url-xpath',
        'ignore-latest', 'no-date'
    ]
    new_data = OrderedDict()
    for key in sorted(old_data.keys()):
        new_data[key] = OrderedDict()
        if _spider in old_data[key]:
            old_spider = old_data[key][_spider]
            new_spider = OrderedDict()
            new_data[key][_spider] = new_spider
            name = old_spider.pop(_name)
            if name == 'gitserver':
                url = old_spider[_url]
                if '?p=' in url:
                    new_spider[_name] = 'paramgitweb'
                elif re.search(r'\bcgit\b', url):
                    new_spider[_name] = 'cgit'
                else:
                    soup = download_as_soup(url)
                    generator = soup.find(
                        'meta', {'name': 'generator'})['content']
                    if 'cgit' in generator:
                        new_spider[_name] = 'cgit'
                    elif 'gitweb' in generator:
                        new_spider[_name] = 'gitweb'
                    else:
                        raise NotImplementedError
            else:
                new_spider[_name] = name
            for sorted_key in sorted_keys:
                if sorted_key in old_spider:
                    new_spider[sorted_key] = old_spider[sorted_key]
            for seeker_key in [seeker_key for seeker_key in old_spider
                               if seeker_key not in new_spider]:
                new_spider[seeker_key] = old_spider[seeker_key]
        if _formatter in old_data[key]:
            new_data[key][_formatter] = old_data[key][_formatter]
        for subkey in [subkey for subkey in old_data[key]
                       if subkey not in new_data[key]]:
            new_data[key][subkey] = old_data[key][subkey]
    save_data(new_data)


if __name__ == "__main__":
    main()
