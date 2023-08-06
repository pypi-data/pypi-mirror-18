from ..items import Item

from . import Spider


class Text(Spider):
    name = 'text'

    def parse(self, response):
        return Item(date=response.text if not response.meta['no-date']
                                       else None,
                    response=response,
                    version=response.text)

    def start_requests(self):
        return super().iter_start_requests(
            params={'no-date': False})

    def first_request(self, data):
        return data['url']
