#

from logging import getLogger
import re


class WhoisParserEx(object):
    mapping = {
        'refer': [
            'refer:\s*(?P<val>.+)',
        ],
        'domain': [
            'domain:\s*(?P<val>.+)',
        ],
        'ds-rdata': [
            'ds-rdata:\s*(?P<val>.+)',
        ],
        'whois': [
            'whois:\s*(?P<val>.+)',
        ],
        'status': [
            'status:\s*(?P<val>.+)',

#            '\[Status\]\s*(?P<val>.+)',
#            'Status\s*:\s?(?P<val>.+)',
#            '\[State\]\s*(?P<val>.+)',
#            '^state:\s*(?P<val>.+)'
        ],
        'remarks': [
            'remarks:\s*(?P<val>.+)',
        ],
        'source': [
            'source:\s*(?P<val>.+)',
        ],


        'id': [
#            'Domain ID:[ ]*(?P<val>.+)'
        ],
        'creation_date': [
            'created:\s*(?P<val>.+)',

#            '\[Created on\]\s*(?P<val>.+)',
#            'Created on[.]*: [a-zA-Z]+, (?P<val>.+)',
#            'Creation Date:\s?(?P<val>.+)',
#            'Creation date\s*:\s?(?P<val>.+)',
#            'Registration Date:\s?(?P<val>.+)',
#            'Created Date:\s?(?P<val>.+)',
                    'Created on:\s?(?P<val>.+)',
                    'Created on\s?[.]*:\s?(?P<val>.+)\.',
                    'Date Registered\s?[.]*:\s?(?P<val>.+)',
                    'Domain Created\s?[.]*:\s?(?P<val>.+)',
                    'Domain registered\s?[.]*:\s?(?P<val>.+)',
                    'Domain record activated\s?[.]*:\s*?(?P<val>.+)',
                    'Record created on\s?[.]*:?\s*?(?P<val>.+)',
                    'Record created\s?[.]*:?\s*?(?P<val>.+)',
                    'Created\s?[.]*:?\s*?(?P<val>.+)',
                    'Registered on\s?[.]*:?\s*?(?P<val>.+)',
                    'Registered\s?[.]*:?\s*?(?P<val>.+)',
                    'Domain Create Date\s?[.]*:?\s*?(?P<val>.+)',
                    'Domain Registration Date\s?[.]*:?\s*?(?P<val>.+)',
                    '\[Registered Date\]\s*(?P<val>.+)',
                    'created-date:\s*(?P<val>.+)',
                    'Domain Name Commencement Date: (?P<val>.+)',
                    'registered:\s*(?P<val>.+)',
                    'registration:\s*(?P<val>.+)'
                ],
                'expiration_date': [
                    'expire:\s*(?P<val>.+)',
                    '\[Expires on\]\s*(?P<val>.+)',
                    'Registrar Registration Expiration Date:[ ]*(?P<val>.+)-[0-9]{4}',
                                         'Expires on[.]*: [a-zA-Z]+, (?P<val>.+)',
                                         'Expiration Date:\s?(?P<val>.+)',
                                         'Expiration date\s*:\s?(?P<val>.+)',
                                         'Expires on:\s?(?P<val>.+)',
                                         'Expires on\s?[.]*:\s?(?P<val>.+)\.',
                                         'Exp(?:iry)? Date\s?[.]*:\s?(?P<val>.+)',
                                         'Expiry\s*:\s?(?P<val>.+)',
                                         'Domain Currently Expires\s?[.]*:\s?(?P<val>.+)',
                                         'Record will expire on\s?[.]*:\s?(?P<val>.+)',
                                         'Domain expires\s?[.]*:\s*?(?P<val>.+)',
                                         'Record expires on\s?[.]*:?\s*?(?P<val>.+)',
                                         'Record expires\s?[.]*:?\s*?(?P<val>.+)',
                                         'Expires\s?[.]*:?\s*?(?P<val>.+)',
                                         'Expire Date\s?[.]*:?\s*?(?P<val>.+)',
                                         'Expired\s?[.]*:?\s*?(?P<val>.+)',
                                         'Domain Expiration Date\s?[.]*:?\s*?(?P<val>.+)',
                                         'paid-till:\s*(?P<val>.+)',
                                         'expiration_date:\s*(?P<val>.+)',
                                         'expire-date:\s*(?P<val>.+)',
                                         'renewal:\s*(?P<val>.+)',
                ],
                'updated_date': [
                    '\[Last Updated\]\s*(?P<val>.+)',
                                         'Record modified on[.]*: (?P<val>.+) [a-zA-Z]+',
                                         'Record last updated on[.]*: [a-zA-Z]+, (?P<val>.+)',
                                         'Updated Date:\s?(?P<val>.+)',
                                         'Updated date\s*:\s?(?P<val>.+)',
                                         #'Database last updated on\s?[.]*:?\s*?(?P<val>.+)\s[a-z]+\.?',
                                         'Record last updated on\s?[.]*:?\s?(?P<val>.+)\.',
                                         'Domain record last updated\s?[.]*:\s*?(?P<val>.+)',
                                         'Domain Last Updated\s?[.]*:\s*?(?P<val>.+)',
                                         'Last updated on:\s?(?P<val>.+)',
                                         'Date Modified\s?[.]*:\s?(?P<val>.+)',
                                         'Last Modified\s?[.]*:\s?(?P<val>.+)',
                                         'Domain Last Updated Date\s?[.]*:\s?(?P<val>.+)',
                                         'Record last updated\s?[.]*:\s?(?P<val>.+)',
                                         'Modified\s?[.]*:\s?(?P<val>.+)',
                                         '(C|c)hanged:\s*(?P<val>.+)',
                                         'last_update:\s*(?P<val>.+)',
                                         'Last Update\s?[.]*:\s?(?P<val>.+)',
                                         'Last updated on (?P<val>.+) [a-z]{3,4}',
                                         'Last updated:\s*(?P<val>.+)',
                                         'last-updated:\s*(?P<val>.+)',
                                         '\[Last Update\]\s*(?P<val>.+) \([A-Z]+\)',
                                         'Last update of whois database:\s?[a-z]{3}, (?P<val>.+) [a-z]{3,4}'
                  ],
                'registrar': [
                         'registrar:\s*(?P<val>.+)',
                                         'Registrar:\s*(?P<val>.+)',
                                         'Sponsoring Registrar Organization:\s*(?P<val>.+)',
                                         'Registered through:\s?(?P<val>.+)',
                                         'Registrar Name[.]*:\s?(?P<val>.+)',
                                         'Record maintained by:\s?(?P<val>.+)',
                                         'Registration Service Provided By:\s?(?P<val>.+)',
                                         'Registrar of Record:\s?(?P<val>.+)',
                                         'Domain Registrar :\s?(?P<val>.+)',
                                         'Registration Service Provider: (?P<val>.+)',
                                         '\tName:\t\s(?P<val>.+)'
                ],
                'whois_server': [
                      'Whois Server:\s?(?P<val>.+)',
                      'Registrar Whois:\s?(?P<val>.+)'
                ],
                'nameservers': [
                          'Name Server:[ ]*(?P<val>[^ ]+)',
                                         'Nameservers:[ ]*(?P<val>[^ ]+)',
                                         '(?<=[ .]{2})(?P<val>([a-z0-9-]+\.)+[a-z0-9]+)(\s+([0-9]{1,3}\.){3}[0-9]{1,3})',
                                         'nameserver:\s*(?P<val>.+)',
                                         'nserver:\s*(?P<val>[^[\s]+)',
                                         'Name Server[.]+ (?P<val>[^[\s]+)',
                                         'Hostname:\s*(?P<val>[^\s]+)',
                                         'DNS[0-9]+:\s*(?P<val>.+)',
                                         '   DNS:\s*(?P<val>.+)',
                                         'ns[0-9]+:\s*(?P<val>.+)',
                                         'NS [0-9]+\s*:\s*(?P<val>.+)',
                                         '\[Name Server\]\s*(?P<val>.+)',
                                         'Nserver:\s*(?P<val>.+)'
                ]
    }

    def __init__(self):
        self.__log = getLogger('pywhoisclient')
        self._mapping_cache = {}

    def _create_mapping_compile_program_cache(self):
        if not self._mapping_cache:
            for name, patterns in WhoisParserEx.mapping.items():
                compiled_patterns = []
                for pattern in patterns:
                    compiled_patterns.append(re.compile(pattern, 0))
                self._mapping_cache[name] = compiled_patterns

    def parse(self, raw_data):
        result = []
        # Step 1. Create compile pattern cache
        self._create_mapping_compile_program_cache()
        # Step 2. Parsing
        for line in [x.strip() for x in raw_data.splitlines()]:
            for name, patterns in self._mapping_cache.items():
                for pattern in patterns:
                    match = pattern.match(line)
                    if match:
                        val = match.group('val')
                        self.__log.debug("Detect: name = {name!r}, val = {val!r}".format(val=val, name=name))
                        result.append((name, val))
        # Step 3.
        return result

