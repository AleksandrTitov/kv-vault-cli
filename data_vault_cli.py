#!/usr/bin/env python3

import json
import datetime
import argparse

from libs.VaultClient import VaultClient
from libs.VaultManipulator import VaultManipulator

#####
# Aries for improvement
#
# TODO namespaces
# TODO tests
#
#####


def delete_data_from_vault(vault_addr, vault_token):

    secret_root = {'secret/': []}

    vault = VaultClient(vault_addr, vault_token)
    action = VaultManipulator(vault)
    to_delete = action.dump_secrets(secret_root, '')
    action.full_delete(to_delete)


def dump_data_from_vault(vault_addr, vault_token, file="vault_dump", time_stamp=True):

    secret_root = {'secret/': []}

    vault = VaultClient(vault_addr, vault_token)
    action = VaultManipulator(vault)
    data = action.dump_secrets(secret_root, '')

    if time_stamp:
        file = f'{file}_{datetime.datetime.now().isoformat()}.json'
    else:
        file = f'{file}.json'

    with open(file, 'w') as df:
        df.write(json.dumps(data, indent=2,))


def restore_data_to_vault(vault_addr, vault_token, file="vault_dump"):

    with open(file, 'r') as df:
        data = json.load(df)

    vault = VaultClient(vault_addr, vault_token)
    action = VaultManipulator(vault)

    action.restore_secrets(data)


def transfer_data(vault_addr_src, vault_token_src, vault_addr_dst, vault_token_dst, merge=True):

    vault_src = VaultClient(vault_addr_src, vault_token_src)
    vault_dst = VaultClient(vault_addr_dst, vault_token_dst)

    action_src = VaultManipulator(vault_src)
    action_dst = VaultManipulator(vault_dst)

    secret_root = {'secret/': []}

    data = action_src.dump_secrets(secret_root, '')

    if merge:
        action_dst.restore_secrets(data)
    else:
        to_delete = action_dst.dump_secrets(secret_root, '')
        action_dst.full_delete(to_delete)
        action_dst.restore_secrets(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('action', metavar='action', choices=['dump', 'restore', 'delete', 'transfer'],
                        type=str, help='Action: dump, restore, delete, transfer')

    parser.add_argument('--vault-addr', help='Vault address')
    parser.add_argument('--vault-token', help='Vault token')
    parser.add_argument('--vault-addr-src', help='Vault Source address')
    parser.add_argument('--vault-addr-dst', help='Vault Destination addres')
    parser.add_argument('--vault-token-src', help='Vault Source token')
    parser.add_argument('--vault-token-dst', help='Vault Destination token')

    parser.add_argument('--file', help='File with secrets to restore')

    parser.add_argument('--merge', '-m', action='store_true',
                        help='Merge')

    args = parser.parse_args()

    if args.action == 'dump':
        if args.vault_addr and args.vault_token:
            dump_data_from_vault(args.vault_addr, args.vault_token)
        else:
            print('Usage: \n\n'
                  'data_vault_cli.py dump \\\n'
                  '\t\t--vault-addr=<vault address> \\\n'
                  '\t\t--vault-token=<vault token>\n\n'
                  'Dump Vault data into the file.')
    elif args.action == 'restore':
        if args.vault_addr and args.vault_token and args.file:
            restore_data_to_vault(args.vault_addr, args.vault_token, args.file)
        else:
            print('Usage: \n\n'
                  'data_vault_cli.py restore \\\n'
                  '--vault-addr=<vault address> \\\n'
                  '\t\t--vault-token=<vault token> \\\n'
                  '\t\t--file=<file>\n\n'
                  'Restore Vault data from the file.')
    elif args.action == 'delete':
        if args.vault_addr and args.vault_token:
            delete_data_from_vault(args.vault_addr, args.vault_token)
        else:
            print('Usage: \n\n'
                  'data_vault_cli.py delete \\\n'
                  '\t\t--vault-addr=<vault address> \\\n'
                  '\t\t--vault-token=<vault token>\n\n'
                  'Full delete Vaults secrets.')
    elif args.action == 'transfer':
        if args.vault_addr_src and args.vault_token_src and args.vault_addr_dst and args.vault_token_dst:
            delete_data_from_vault(args.vault_addr, args.vault_token)
            transfer_data(args.vault_addr_src, args.vault_token_src, args.vault_addr_dst, args.vault_token_dst, )
        else:
            print('Usage: \n\n'
                  'data_vault_cli.py transfer \\\n'
                  '\t\t--vault-addr-src=<vault address source> \\\n'
                  '\t\t--vault-token-src=<vault token source> \\\n'
                  '\t\t--vault-addr-dst=<vault address destination> \\\n'
                  '\t\t--vault-token-dst=<vault token destination>\n\n'
                  'Transfer data between Vaults.')
