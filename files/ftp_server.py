#!/usr/bin/env python

import argparse
import os
import re
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# http://pythonhosted.org/pyftpdlib/api.html#users
DEFAULT_PERMISSIONS = 'elramdfw'


def IPPortString(v):
    try:
        return re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,}?$", v).group(0)
    except:
        raise argparse.ArgumentTypeError("Value '{}' does not match required format: <ip>:<port>".format(v))


def ftp_server(opts):

    authorizer = DummyAuthorizer()
    authorizer.add_user(opts.username, opts.password, opts.root, perm=opts.permissions)

    handler = FTPHandler
    handler.authorizer = authorizer

    # TODO: eventually add configuration option for passive ports / port range
    handler.passive_ports = range(60000, 65535)

    server = FTPServer(opts.bind.split(':'), handler)
    server.serve_forever()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Say hello')

    parser.add_argument('-u', '--username', dest='username', required=True)
    parser.add_argument('-p', '--password', dest='password', required=True)
    parser.add_argument('-r', '--root', dest='root', default=os.getcwd())
    parser.add_argument('-b', '--bind', dest='bind', default='0.0.0.0:2121', type=IPPortString)
    parser.add_argument('--permissions', dest='permissions', default=DEFAULT_PERMISSIONS)

    opts = parser.parse_args()

    ftp_server(opts)
