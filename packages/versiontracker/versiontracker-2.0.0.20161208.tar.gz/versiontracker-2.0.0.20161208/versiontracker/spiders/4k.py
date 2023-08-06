from .xpath import XPath


class FourK(XPath):
    name = '4k'

    def parse(self, response):
        meta = response.meta
        meta.update(XPath.params)
        meta['base'] = '//a[re:test(@href, \'/app/{}_\')]/parent::td/' \
                        'following-sibling::td'.format(meta['id'])
        meta['date'] = '/following-sibling::td'
        return super().parse(response)

    def first_request(self, data):
        return 'https://www.4kdownload.com/download'
