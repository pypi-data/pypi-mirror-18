import re

from ..items import Item

from . import Spider


_DATE_RE = re.compile("^(.*?) by.*$")


class Hackage(Spider):
    name = 'hackage'

    @staticmethod
    def extract(response, field_name, sub_xpath='text()'):
        return response.xpath(
            '//table[re:test(@class, \'\\bproperties\\b\')]/tbody/'
            'tr[re:test(th/text(), \'\\s*{}\\s*\')]/'
            'td/{}'.format(field_name, sub_xpath)).extract_first().strip()

    def parse(self, response):
        date = _DATE_RE.match(self.extract(response, 'Uploaded')).group(1)
        version = self.extract(response, 'Versions', 'strong/text()')
        url = response.url + '-' + version
        return Item(date=date, response=response, url=url, version=version)

    def first_request(self, data):
        return 'http://hackage.haskell.org/package/{}'.format(
            data.get('package', data['id']))
