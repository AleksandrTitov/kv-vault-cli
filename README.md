# kv-vault-cli
**kv_vault_cli.py** is a cli tool for Managing K/V Secrets Engine of Hashicorp Vault.

## How to use

Supported the following actions:
### dump

Collect a Vault K/V data into the file.

```
./kv_vault_cli.py dump --vault-addr="VAULT ADDR" --vault-token="VAULT TOKEN"
```
### restore

Restore a Vault K/V data from the file.

```
./kv_vault_cli.py restore --vault-addr="VAULT ADDR" --vault-token="VAULT TOKEN" \
                          --file="PATH TO FILE"
```

### delete

Full delete data from all of the K/V Secrets Engine

```
./kv_vault_cli.py delete --vault-addr="VAULT ADDR" --vault-token="VAULT TOKEN"
```

### transfer

Transfer K/V data between Vaults

```
./data_vault_cli.py transfer --vault-addr-src="VAULT ADDR SRC" --vault-token-src="VAULT TOKEN SRC" \
                             --vault-addr-dst="VAULT ADDR DST" --vault-token-dst="VAULT TOKEN DST"
```

Support option ```--not-merge```, by default it False, if it set, all the data form K/V of destination 
Vault will deleted before the transfer operation.

## Limitation

The tool not supports [KV Secrets Engine - Version 2](https://www.vaultproject.io/api/secret/kv/kv-v2.html)
