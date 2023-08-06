#

from __future__ import absolute_import

from logging import getLogger
from socket import socket, AF_INET, SOCK_STREAM
#from codecs import encode, decode

from .error import WhoisException


class WhoisService(object):
    """ Whois service client (RFC-3912)

    client                           server at whois.nic.mil

    open TCP   ---- (SYN) ------------------------------>
               <---- (SYN+ACK) -------------------------
    send query ---- "Smith<CR><LF>" -------------------->
    get answer <---- "Info about Smith<CR><LF>" ---------
               <---- "More info about Smith<CR><LF>" ----
    close      <---- (FIN) ------------------------------
               ----- (FIN) ----------------------------->
    """

    def __init__(self, host="whois.iana.org", port=43, timeout=15):
        self.__log = getLogger('pywhoisclient')
        #
        self._host = host
        self._port = 43
        self._timeout = timeout

    def whois_request(self, domain):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(self._timeout)
        sock.connect((self._host, self._port))
        req = "{domain}\r\n".format(domain=domain)
        sock.send(req.encode("utf-8"))
        buff = b""
        while True:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            buff += data
        #
        sock.close()
        #
        return buff.decode("utf-8")
