"""Hashicorp Vault Client

Authorization use Vault token

"""

import urllib3
import json


class VaultClient(object):

    def __init__(self, vault_adr, vault_token, api_ver):
        self.vault_adr = vault_adr
        self.vault_token = vault_token
        self.api_ver = api_ver

    def get_list_of_secrets(self, path):
        http = urllib3.PoolManager()
        url = f'{self.vault_adr}/{self.api_ver}/{path}'

        r = http.request('LIST',
                         url,
                         headers={
                             'X-Vault-Token': self.vault_token
                         }
                         )

        if r.status != 200:
            list_of_secrets=['none']
        else:
            list_of_secrets = json.loads(r.data)['data']['keys']

        return list_of_secrets

    def get_data(self, path):
        http = urllib3.PoolManager()
        url = f'{self.vault_adr}/{self.api_ver}/{path}'

        r = http.request('GET',
                         url,
                         headers={
                             'X-Vault-Token': self.vault_token
                         }
                         )
        if r.status != 200:
            data = 'none'
        else:
            data = json.loads(r.data)['data']

        return data

    def write_data(self, path, data):
        http = urllib3.PoolManager()
        url = f'{self.vault_adr}/{self.api_ver}/{path}'

        r = http.request('GET',
                         url,
                         headers={
                             'X-Vault-Token': self.vault_token
                         }
                         )
        if r.status != 404:
            self.delete_data(path=path)

        r = http.request('POST',
                         url,
                         headers={
                             'X-Vault-Token': self.vault_token
                         },
                         body=json.dumps(data)
                         )
        if r.status == 204:
            print('Write is successful...')

    def delete_data(self, path):
        http = urllib3.PoolManager()
        url = f'{self.vault_adr}/{self.api_ver}/{path}'

        r = http.request('DELETE',
                         url,
                         headers={
                             'X-Vault-Token': self.vault_token
                         }
                         )
        if r.status == 204:
            print('Delete is successful...')

    def get_catalog(self):
        http = urllib3.PoolManager()
        url = f'{self.vault_adr}/{self.api_ver}/sys/plugins/catalog'

        r = http.request('GET',
                         url,
                         headers={
                             'X-Vault-Token': self.vault_token
                         }
                         )

        if r.status != 200:
            list_of_secrets = ['none']
        else:
            list_of_secrets = json.loads(r.data)

        return list_of_secrets