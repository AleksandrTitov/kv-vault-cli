#!/usr/bin/env python

from libs.VaultClient import VaultClient
from libs.VaultManipulator import VaultManipulator

#####
# Aries for improvement
#
# TODO transfer secrets between vaults:
# TODO  save to file
# TODO  namespaces ?
#
#####

vault_token = "s.5rP2baKEwkOImTHh8sKojBMs"
vault_adr = "http://127.0.0.1:8200"

vault = VaultClient(vault_adr, vault_token, 'v1')

action = VaultManipulator(vault)

secret_root_n = {'secret/': []}

tree_to_restore = {'secret/': [{'secret': {'secret2': 'suslo222', 'secret3': 'suslo223'}, 'full_path': 'secret/main2'}, {'secret': {'secret': '2'}, 'full_path': 'secret/main1'}, {'main/': [{'hello/': [{'hello2/': [{'secret': {'secret2': 'suslo222', 'secret3': 'suslo223'}, 'full_path': 'secret/main/hello/hello2/hello3'}]}]}, {'secret': {'secret2': 'suslo222', 'secret3': 'suslo223'}, 'full_path': 'secret/main/hello'}]}, {'a1/': [{'a2/': [{'a3/': [{'a4/': [{'a5/': [{'a6/': [{'a7/': [{'secret': {'end': 'yes\nyes\nno\nyes'}, 'full_path': 'secret/a1/a2/a3/a4/a5/a6/a7/end'}]}]}]}]}]}]}]}]}

#to_delete = action.dump_secrets(secret_root_n, '')
#action.full_delete(to_delete)
action.restore_secrets(tree_to_restore)

def dump_secrets(root, full_path):
    for key, val in root.items():
        full_path = full_path + key
        dirs = vault.get_list_of_secrets(full_path)
        while len(dirs) != 0:
            data = dirs.pop()
            if '/' in data:
                val.append(dump_secrets({data: []}, full_path))
            else:
                root[key].append({'secret': vault.get_data(full_path+data), 'full_path': full_path+data})
    return root


def restore_secrets(tree_of_secrets):
    for key, val in tree_of_secrets.items():
        for i in val:
            if 'full_path' in i:
                vault.write_data(i['full_path'], i['secret'])
            else:
                restore_secrets(i)


def full_delete(tree_of_secrets):
    for key, val in tree_of_secrets.items():
        for i in val:
            if 'full_path' in i:
                vault.delete_data(i['full_path'])
            else:
                full_delete(i)

#tree_to_restore = {'secret/': [{'secret': {'secret2': 'suslo222', 'secret3': 'suslo223'}, 'full_path': 'secret/main2'}, {'secret': {'secret': '2'}, 'full_path': 'secret/main1'}, {'main/': [{'hello/': [{'hello2/': [{'secret': {'secret2': 'suslo222', 'secret3': 'suslo223'}, 'full_path': 'secret/main/hello/hello2/hello3'}]}]}, {'secret': {'secret2': 'suslo222', 'secret3': 'suslo223'}, 'full_path': 'secret/main/hello'}]}, {'a1/': [{'a2/': [{'a3/': [{'a4/': [{'a5/': [{'a6/': [{'a7/': [{'secret': {'end': 'yes\nyes\nno\nyes'}, 'full_path': 'secret/a1/a2/a3/a4/a5/a6/a7/end'}]}]}]}]}]}]}]}]}

#tree = dump_secrets(secret_root_n, '')
#print(tree)

#restore_secrets(tree_to_restore)
#full_delete(tree)



'''
secret_list = vault.get_list_of_secrets(secret_root)
print(secret_list)

data = vault.get_data('secret')
print(data)

vault.write_data('secret/main', data={"secret": "suslo22"})
vault.write_data('secret/main2', data={"secret2": "suslo222", "secret3": "suslo223"})
vault.write_data('secret/main/hello/hello2/hello3', data={"secret2": "suslo222", "secret3": "suslo223"})

data = vault.get_data('secret/main')
data2 = vault.get_data('secret/main2')
print(data)
print(data2)

'''


'''
secrets = get_list_of_secrets('secret', vault_token=vault_token)
get_data('secret/main', vault_token=vault_token)
delete_data('secret/main/1', vault_token=vault_token)
write_data('secret/main', data={"secret": "suslo22"}, vault_token=vault_token)
get_data('secret/main', vault_token=vault_token)

#print(secrets)
'''
