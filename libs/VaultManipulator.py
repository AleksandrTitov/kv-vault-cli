"""
Hashicorp Vault Manipulator

Support the following action:
    - Dump secrets - return dict with secrets;
    - Restore secrets - restore secrets form dict;
    - Full delete - delete all the secrets from Vault;
    - Get KV mounts - get KV secrets engine;
"""


class VaultManipulator(object):
    """
    Works with Vault KV secrets engines;
    To connect to Vault uses VaultClient class;
    """

    def __init__(self, vault):
        self.vault = vault

    def dump_secrets(self, root, full_path=''):
        """
        The method finds the secrets, supports multiple KV secrets engines,
        and return it in the dictionary

        :param root: the dictionary in the following format:
            {
              "secret1/":
                {
                  "data": [],
                  "type": "root"
                },
              "secret2/":
                {
                  "data": [],
                  "type": "root"
                }
            }
        :param full_path: path to the secret
        :return: the dictionary in the following format:
            {
              "secret1/": {
                "data": [
                  {
                    "dir/": {
                      "data": [
                        {
                          "secret": {
                            "data1": "secret1",
                            "data2": "secret2"
                          },
                          "full_path": "kv/dir/sensitive_data",
                          "type": "secret"
                        }
                      ],
                      "type": "dir"
                    }
                  }
                ],
                "type": "root"
              }
            }
        """

        for key, val in root.items():

            if val['type'] == 'root':
                full_path = ''

            full_path = full_path + key

            dirs = self.vault.get_list_of_secrets(full_path)
            for data in dirs:
                if '/' in data:
                    val['data'].append(self.dump_secrets({
                        data:
                            {
                                'data': [],
                                'type': 'dir'
                            }
                    }, full_path))
                else:
                    root[key]['data'].append({
                        'secret': self.vault.get_data(full_path + data),
                        'full_path': full_path + data,
                        'type': 'secret'
                    })
        return root

    def restore_secrets(self, tree_of_secrets):
        """
        The method restore secrets form dictionary.
        If the KV secret engine doesn't exist, it'll be created.

        :param tree_of_secrets: it's a dictionary, which return "dump_secrets" method
        """

        for key, val in tree_of_secrets.items():
            if val['type'] == 'root' and key not in self.vault.list_mounted_secrets_engines():
                self.vault.enable_secrets_engine(key[:-1])
            for i in val['data']:
                if 'full_path' in i:
                    self.vault.write_data(i['full_path'], i['secret'])
                else:
                    self.restore_secrets(i)

    def full_delete(self, tree_of_secrets):

        """
        Deleting all the secrets from KV secret engine

        :param tree_of_secrets: it's a dictionary, which return "dump_secrets" method
        """

        for key, val in tree_of_secrets.items():
            for i in val['data']:
                if 'full_path' in i:
                    self.vault.delete_data(i['full_path'])
                else:
                    self.full_delete(i)

    def get_kv_mounts(self):
        """
        Getting all the KV secret engine

        :return: dictionary in the following format:
            {
              "secret1/":
                {
                  "data": [],
                  "type": "root"
                },
              "secret2/":
                {
                  "data": [],
                  "type": "root"
                }
            }
        """

        kv_mounts = {}
        secrets_engines = self.vault.list_mounted_secrets_engines()

        # Support bough type of secrets engines kv and generic
        # https://github.com/hashicorp/vault/blob/master/CHANGELOG.md#083-september-19th-2017
        for key, val in secrets_engines.items():
            try:
                if val['type'] == 'kv' or val['type'] == 'generic':
                    kv_mounts[key] = {'data': [], 'type': 'root'}
            except:
                pass

        return kv_mounts

if __name__ == "__main__":
    print(__doc__)
