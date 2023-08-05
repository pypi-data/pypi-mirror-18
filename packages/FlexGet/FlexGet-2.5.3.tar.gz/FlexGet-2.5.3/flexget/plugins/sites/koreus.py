from __future__ import unicode_literals, division, absolute_import
from builtins import *  # pylint: disable=unused-import, redefined-builtin

import logging
import re

from flexget import plugin
from flexget.event import event
from flexget.plugins.internal.urlrewriting import UrlRewritingError
from flexget.utils.soup import get_soup

log = logging.getLogger('koreus')


class UrlRewriteKoreus(object):
    """Koreus urlrewriter."""

    # urlrewriter API
    def url_rewritable(self, task, entry):
        url = entry['url']
        if url.startswith('http://www.koreus.com'):
            return True
        return False

    # urlrewriter API
    def url_rewrite(self, task, entry):
        entry['url'] = self.parse_download_page(entry['url'], task.requests)

    @plugin.internet(log)
    def parse_download_page(self, url, requests):
        txheaders = {'User-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        page = requests.get(url, headers=txheaders)
        try:
            soup = get_soup(page.text)
        except Exception as e:
            raise UrlRewritingError(e)
        down_link = soup.find('a', attrs={'href': re.compile(".+mp4")})
        if not down_link:
            raise UrlRewritingError('Unable to locate download link from url %s' % url)
        return down_link.get('href')


@event('plugin.register')
def register_plugin():
    plugin.register(UrlRewriteKoreus, 'koreus', groups=['urlrewriter'], api_ver=2)
