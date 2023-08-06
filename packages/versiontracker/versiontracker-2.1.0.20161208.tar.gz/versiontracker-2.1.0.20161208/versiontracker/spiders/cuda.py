import re

from scrapy import Request

from ..items import Item

from . import Spider


class Cuda(Spider):
    name = 'cuda'

    def parse(self, response):
        response.meta['major_version'] = re.match(
            'CUDA (\\d+(?:\\.\\d+)+) Downloads',
            response.xpath('//title/text()').extract_first()).group(1)
        response.meta['url'] = response.url
        return Request(
            "http://developer.download.nvidia.com/compute/cuda/" \
            "{}/Prod/docs/sidebar/md5sum.txt".format(
                response.meta['major_version']),
            callback=self.parse_md5_url,
            meta=response.meta)

    def parse_md5_url(self, response):
        response.meta['version'] = re.search(
            'cuda_(?P<version>\\d+(\\.\\d+)+)_linux\\.run',
            response.text).group("version")
        url = 'https://developer.nvidia.com/compute/cuda/{}/prod/' \
              'local_installers/cuda_{}_linux-run'.format(
                    *(response.meta[k] for k in ('major_version', 'version')))
        return Request(
            url,
            callback=self.parse_file_url,
            meta=response.meta,
            method='HEAD',)

    def parse_file_url(self, response):
        return Item(date=response.headers['Last-Modified'].decode('utf-8'),
                    response=response)

    def first_request(self, data):
        return 'https://developer.nvidia.com/cuda-downloads'
