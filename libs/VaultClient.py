"""Hashicorp Vault Client

Authorization use Vault token

"""

import urllib3
import json
import logging

logger = logging.getLogger('[Vault Client]')
logging.basicConfig(level=logging.INFO)


class VaultClient(object):

    def __init__(self, vault_addr='http://127.0.0.1:8200', vault_token=None, api_ver='v1'):
        self.vault_addr = vault_addr
        self.vault_token = vault_token
        self.api_ver = api_ver

    def _http_request(self, method, path, data=None):

        url = f'{self.vault_addr}/{self.api_ver}/{path}'
        body = json.dumps(data)

        if self.vault_token:
            headers = {
                'X-Vault-Token': self.vault_token
            }
        else:
            headers = None

        http = urllib3.PoolManager()
        request = http.request(method=method, url=url, body=body, headers=headers)

        return request

    def get_list_of_secrets(self, path):

        request = self._http_request('LIST', path)

        if request.status != 200:
            list_of_secrets = ['none']
            logger.warning(f'The path {path} is incorrect, set the value "none"')
        else:
            logger.info(f'The key/value from {path} got')
            list_of_secrets = json.loads(request.data)['data']['keys']

        return list_of_secrets

    def get_data(self, path):

        request = self._http_request('GET', path)

        if request.status != 200:
            data = 'none'
            logger.warning(f'The path {path} is incorrect, set the data "none"')
        else:
            logger.info(f'The data from {path} got')
            data = json.loads(request.data)['data']

        return data

    def write_data(self, path, data):

        request = self._http_request('GET', path)

        if request.status != 404:
            self.delete_data(path=path)

        request = self._http_request('POST', path, data)
        if request.status == 204:
            print('Write is successful...')

    def delete_data(self, path):

        request = self._http_request('DELETE', path)

        if request.status == 204:
            logger.info(f'Key {path} successful deleted')
