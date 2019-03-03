"""
Hashicorp Vault Client

Support the following action:
    - Get list of secrets
    - Get data
    - Write data
    - Delete data
"""

import urllib3
import json
from libs.setup_logger import logger


class VaultClient(object):
    """Hashicorp Vault Client"""

    def __init__(self, vault_addr='http://127.0.0.1:8200', vault_token=None, api_ver='v1'):
        self.vault_addr = vault_addr
        self._vault_token = vault_token
        self.api_ver = api_ver
        self.log = logger

    def _http_request(self, method, path, data=None):

        url = f'{self.vault_addr}/{self.api_ver}/{path}'
        body = json.dumps(data)

        if self._vault_token:
            headers = {
                'X-Vault-Token': self._vault_token
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
            self.log.warning(f'Path {path} is incorrect, set the value "none"')
        else:
            self.log.info(f'List of secrets from {path} successfully got')
            list_of_secrets = json.loads(request.data)['data']['keys']

        return list_of_secrets

    def get_data(self, path):

        request = self._http_request('GET', path)

        if request.status != 200:
            data = 'none'
            self.log.warning(f'Path {path} is incorrect, set the data to {data}')
        else:
            self.log.info(f'Data from {path} successfully got')
            data = json.loads(request.data)['data']

        return data

    def write_data(self, path, data):

        request = self._http_request('GET', path)

        if request.status != 404:
            self.delete_data(path=path)
            self.log.info(f'Path {path} contain the data, delete it')
        request = self._http_request('POST', path, data)
        if request.status == 204:
            self.log.info(f'Data successfully wrote to {path}...')
        else:
            self.log.warning(f'Alarm! Something goes wrong...')

    def delete_data(self, path):

        request = self._http_request('DELETE', path)

        if request.status == 204:
            self.log.info(f'Key {path} successfully deleted')
        else:
            self.log.warning(f'Alarm! Something goes wrong...')

    def list_mounted_secrets_engines(self):

        path = 'sys/mounts'
        request = self._http_request('GET', path)

        data = json.loads(request.data)

        return data

    def enable_secrets_engine(self, name, type="kv"):

        path = f'sys/mounts/{name}'

        logger.info(f'Create {type} secrets engine "{name}" ...')
        request = self._http_request('POST', path, data={
            'type': type
        })

        if request.status == 204:
            self.log.info(f'Secrets engine "{name}" is successfully created!')
        else:
            self.log.warning(f'Alarm! Something goes wrong...')


if __name__ == "__main__":
    print(__doc__)
