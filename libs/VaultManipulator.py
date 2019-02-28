"""
Hashicorp Vault Manipulator

Support the following action:
    - Dump secrets - return dict with secrets
    - Restore secrets - restore secrets form dict
    - Full delete - delete all the secrets from Vault
"""


class VaultManipulator(object):

    def __init__(self, vault):
        self.vault = vault

    def dump_secrets(self, root, full_path):
        for key, val in root.items():
            full_path = full_path + key
            dirs = self.vault.get_list_of_secrets(full_path)
            for data in dirs:
                if '/' in data:
                    val.append(self.dump_secrets({data: []}, full_path))
                else:
                    root[key].append({'secret': self.vault.get_data(full_path+data), 'full_path': full_path+data})
        return root

    def restore_secrets(self, tree_of_secrets):
        for key, val in tree_of_secrets.items():
            for i in val:
                if 'full_path' in i:
                    self.vault.write_data(i['full_path'], i['secret'])
                else:
                    self.restore_secrets(i)

    def full_delete(self, tree_of_secrets):
        for key, val in tree_of_secrets.items():
            for i in val:
                if 'full_path' in i:
                    self.vault.delete_data(i['full_path'])
                else:
                    self.full_delete(i)

if __name__ == "__main__":
    print(__doc__)
