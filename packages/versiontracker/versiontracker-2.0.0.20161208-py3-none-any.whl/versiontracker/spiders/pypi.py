import json
import re

from .. import compile_pattern
from ..items import Item

from . import parse_date, Spider


class PyPI(Spider):
    name = 'pypi'

    @staticmethod
    def extract(response, field_name):
        return response.xpath(
            '//div[re:test(@class, \'\\bdetails\\b\')]'
            '//div[re:test(@class, \'\\brow\\b\')]'
            '[re:test(span/text(), \'\\b{}\\b\')]'
            '//span[re:test(@class, \'\\bvalue\\b\')]/text()'
            ''.format(field_name)).extract_first().strip()

    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        version = data["info"]["version"]
        meta = response.meta
        version_re = compile_pattern(meta['version'])
        if version_re and not version_re.search(version):
            versions_by_date = {}
            for candidate_version, version_data in data["releases"].items():
                if len(version_data):
                    date = parse_date(version_data[0]["upload_time"])
                    if date not in versions_by_date:
                        versions_by_date[date] = []
                    versions_by_date[date].append(candidate_version)
            version = None
            for date in sorted(versions_by_date.keys()):
                for candidate_version in versions_by_date[date]:
                    if version_re.search(candidate_version):
                        version = candidate_version
                        break
            if version is None:
                raise NotImplementedError
        date = data["releases"][version][0]["upload_time"]
        url = "https://pypi.python.org/pypi/{}/{}".format(
            meta['package'] or meta['id'], version)
        return Item(date=date, response=response, url=url, version=version)

    def start_requests(self):
        return super().iter_start_requests(
            params={'package': None, 'version': None})

    def first_request(self, data):
        return "https://pypi.python.org/pypi/{}/json".format(
            data.get('package', data['id']))
