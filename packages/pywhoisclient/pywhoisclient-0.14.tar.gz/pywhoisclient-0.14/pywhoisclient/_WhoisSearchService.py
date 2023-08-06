#

from __future__ import absolute_import

from logging import getLogger

from ._WhoisService import WhoisService

from ._WhoisParser import WhoisParser
from ._WhoisParserEx import WhoisParserEx

from .parser import DateParser


class WhoisSearchService(object):
    def __init__(self):
        self.__log = getLogger('pywhoisclient')

    def search(self, domain, host=None, strict=True):
        """ Search
        """
        result = None
        #
        if host:
            service = WhoisService(host=host)
        else:
            service = WhoisService()
        #
        raw_data = service.whois_request(domain)
        self.__log.debug('raw_data = {raw_data!r}'.format(raw_data=raw_data))
        #
        if strict:
            parser = WhoisParser()
        else:
            parser = WhoisParserEx()
        #
        values = parser.parse(raw_data)
        #
        self.__log.debug(values)
        #
        refer = None
        for name, value in values:
            if name == 'refer':
                refer = value
        #
        if refer:
            search_service = WhoisSearchService()
            return search_service.search(domain, host=refer, strict=strict)
        #
        d_parser = DateParser()
        #
        result = []
        for name, value in values:
            if name in ['creation_date', 'expiration_date']:
                val = d_parser.parse(value)
                if val:
                    result.append((name, val))
                else:
                    result.append((name, value))
            else:
                result.append((name, value))
        #
        return result
