#!/usr/bin/env python

import argparse
import json
import time
import socket
import requests
from requests.exceptions import ConnectionError

DEFAULT_INTERVAL = 60 * 15
DEFAULT_BASE_URL = 'http://service.digris.net'
#DEFAULT_BASE_URL = 'http://10.40.10.40:8080'

class ServiceClient(object):

    def __init__(self, opts):
        self.client_id = opts.client_id
        self.token = opts.token
        self.base_url = opts.base_url

    def ping(self):

        url = '{base_url}/api/v1/infrastructure/encoder/{client_id}/'.format(
            base_url=self.base_url, client_id=self.client_id
        )

        payload = {
            'internal_ip': self.get_internal_ip(),
        }

        headers = {
            'Authorization': 'Token {}'.format(opts.token)
        }

        print('ping {} with payload:  {}'.format(url, payload))

        try:
            r = requests.patch(url=url, json=payload, headers=headers, timeout=5.0)
        except requests.exceptions.ConnectionError as e:
            print('{}'.format(e))


    def get_internal_ip(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        return s.getsockname()[0]




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Bongiorno')

    parser.add_argument('-i', '--client-id', dest='client_id', required=True)
    parser.add_argument('-t', '--token', dest='token', required=True)
    parser.add_argument('-u', '--base-url', dest='base_url', default=DEFAULT_BASE_URL)
    parser.add_argument('-s', '--sleep', dest='sleep', type=int, default=DEFAULT_INTERVAL)

    opts = parser.parse_args()

    client = ServiceClient(opts)

    while True:
        client.ping()

        time.sleep(opts.sleep)

