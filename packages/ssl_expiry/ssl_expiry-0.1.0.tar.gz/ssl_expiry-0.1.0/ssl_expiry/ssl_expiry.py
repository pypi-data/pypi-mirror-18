#!/usr/bin/env python

import certifi
import errno
import socket
import ssl
import sys

from datetime import datetime


CONNECTION_TIMEOUT = 5.0


class SSLConnectionFailed(Exception):
    pass


class UnknownSSLFailure(Exception):
    pass


class LookupFailed(Exception):
    pass


def get_ssl_expiry(domain):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(CONNECTION_TIMEOUT)
        ssl_sock = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_REQUIRED, ca_certs=certifi.where())
        ssl_sock.settimeout(CONNECTION_TIMEOUT)
        ssl_sock.connect((domain, 443))
        cert = ssl_sock.getpeercert()
        end = datetime.fromtimestamp(ssl.cert_time_to_seconds(cert['notAfter']))
        return str(end.date())
    except socket.gaierror:
        raise LookupFailed
    except socket.error as e:
        if e.errno == errno.ECONNREFUSED:
            # connection to port 443 was confused
            raise SSLConnectionFailed
        raise UnknownSSLFailure


def ssl_expiry():
    domain = sys.argv[-1]

    try:
        print(get_ssl_expiry(domain))
    except SSLConnectionFailed:
        print('Could not connect on port 443')
    except UnknownSSLFailure:
        print('Issues parsing SSL certificate')
    except LookupFailed:
        print('DNS lookup failed')


if __name__ == '__main__':
    ssl_expiry()
