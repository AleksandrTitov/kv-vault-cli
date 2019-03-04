"""
Hashicorp Vault Client

Support the following action:
    - Get list of secrets
    - Get data
    - Write data
    - Delete data
    - List of mounted secrets
    - Enable KV secret engine
"""

import urllib3
import json
from libs.setup_logger import logger


class VaultClient(object):
    """
    Hashicorp Vault Client, uses API https://www.vaultproject.io/api/
    """

    def __init__(self, vault_addr='http://127.0.0.1:8200', vault_token=None, api_ver='v1'):
        self.vault_addr = vault_addr
        self._vault_token = vault_token
        self.api_ver = api_ver
        self.log = logger

    def _http_request(self, method, path, data=None):
        """
        A common method for HTTP requests

        :param method: HTTP method
        :param path: URL path
        :param data: data of the request
        :return: HTTPResponse object
        """

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
        """
        Get list data from Vault at the given path

        https://www.vaultproject.io/api/secret/kv/kv-v1.html#list-secrets

        :param path: URL path
        :return: list data from Vault at the given path, as an example:
            ['secret/', 'new']
        """

        request = self._http_request('LIST', path)

        if request.status != 200:
            list_of_secrets = ['none']
            self.log.warning(f'Path {path} is incorrect, set the value "none"')
        else:
            self.log.info(f'List of secrets from {path} successfully got')
            list_of_secrets = json.loads(request.data)['data']['keys']

        return list_of_secrets

    def get_data(self, path):
        """
        Get the value of the path

        https://www.vaultproject.io/api/secret/kv/kv-v1.html#read-secret

        :param path: URL path
        :return: dictionary of the secrets, as an example:
            {'secret1': '1', 'secret2': '2'}
        """
        request = self._http_request('GET', path)

        if request.status != 200:
            data = 'none'
            self.log.warning(f'Path {path} is incorrect, set the data to {data}')
        else:
            self.log.info(f'Data from {path} successfully got')
            data = json.loads(request.data)['data']

        return data

    def write_data(self, path, data):
        """
        Sets or updates data in the KV store

        https://www.vaultproject.io/api/secret/kv/kv-v1.html#create-update-secret

        :param path: URL path
        :param data: Value in the following format {'new': '1'}
        """

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
        """
        Delete operation on secrets in Vault

        https://www.vaultproject.io/api/secret/kv/kv-v1.html#delete-secret

        :param path: URL path
        """

        request = self._http_request('DELETE', path)

        if request.status == 204:
            self.log.info(f'Key {path} successfully deleted')
        else:
            self.log.warning(f'Alarm! Something goes wrong...')

    def list_mounted_secrets_engines(self):
        """
        Get secrets engines

        :return: https://www.vaultproject.io/api/system/mounts.html#sample-response
        """

        path = 'sys/mounts'
        request = self._http_request('GET', path)

        data = json.loads(request.data)

        return data

    def enable_secrets_engine(self, name, type="kv"):
        """
        Enable secrets engine

        https://www.vaultproject.io/api/system/mounts.html#enable-secrets-engine

        :param name: name of the secrets engine
        :param type: type of the secrets engine
        """

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
