import re

from scrapy import Request

from ..items import Item

from . import Spider


class MozJS(Spider):
    name = 'mozjs'

    def parse(self, response):
        xpath = '//h2[@id=\'Current_release\']/following-sibling::ul//a/@href'
        response.meta['url'] = response.url
        return Request(response.urljoin(response.xpath(xpath).extract_first()),
                       callback=self.parse_article,
                       meta=response.meta)

    def parse_article(self, response):
        base_xpath = '//article[@id=\'wikiArticle\']' \
                     '//div[re:test(@class, \'\\bnote\\b\')]'
        xpath = base_xpath + '//a/@href'
        download_link = response.xpath(xpath).extract_first()
        version = re.search('mozjs-(\\d+(\\.\\d+)+)', download_link).group(1)
        xpath = base_xpath + '//span[re:test(@class, \'\\bgI\\b\')]/text()'
        date = response.xpath(xpath).extract_first()
        return Item(date=date, response=response, version=version)

    def first_request(self, data):
        return 'https://developer.mozilla.org/en-US/docs/Mozilla/Projects' \
               '/SpiderMonkey/Releases'
