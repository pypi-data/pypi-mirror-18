#!/usr/bin/python3

from logging import getLogger


class Application(object):
    """ Service make domain name combination and check
    """
    def __init__(self):
        self.__log = getLogger('pywc')

    def make_names(self):
        result = []
        with open("keyword.txt", "r") as stream:
            for line in stream:
               result.append(line.strip())
        return result

    def make_mult(self, names):
        result = []
        for n1 in names:
            for n2 in names:
                if n1 != n2:
                    domain = "{n1}{n2}.com".format(n1=n1, n2=n2)
                    if domain not in result:
                        result.append(domain)
        return result

    def make_request(self, domain):
        result = None
        from pywhoisclient import WhoisSearchService
        search_service = WhoisSearchService()
        values = search_service.search(domain)
        print(values)
        w = dict(values)
        print(w)
        registrar = w.get('registrar')
        if not registrar:
            result = domain
            print(domain)
        #
        return result

    def run(self):
        domains = self.make_mult(self.make_names()) 
        for domain in domains:
            self.make_request(domain)

if __name__ == "__main__":
    app = Application()
    app.run()
