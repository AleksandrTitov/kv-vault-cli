# kv-vault-cli
**kv_vault_cli.py** is a cli tool for Managing K/V Secrets Engine of Hashicorp Vault.

## How to use

### Actions
Supported the following actions:
#### dump

Dumping Vault K/V data into the file

```
./kv_vault_cli.py dump --vault-addr="VAULT ADDR" --vault-token="VAULT TOKEN"
```
#### restore

Restore Vault K/V data from the file

```
./kv_vault_cli.py restore --vault-addr="VAULT ADDR" --vault-token="VAULT TOKEN" \
                          --file="PATH TO FILE"
```

#### delete

Full delete data from all of the K/V Secrets Engines

```
./kv_vault_cli.py delete --vault-addr="VAULT ADDR" --vault-token="VAULT TOKEN"
```

#### transfer

Transfer K/V data between Vaults

```
./kv_vault_cli.py transfer --vault-addr-src="VAULT ADDR SRC" --vault-token-src="VAULT TOKEN SRC" \
                           --vault-addr-dst="VAULT ADDR DST" --vault-token-dst="VAULT TOKEN DST"
```

Support option ```--not-merge```, by default it False, if it set, all the data form K/V of destination 
Vault will deleted before the transfer operation.

### Options
#### vault-root-path

The option ```--vault-root-path``` allows to use the particular path to the Vault secrets instead of using all the Vault secrets engines, by default, if the option doesn't set then uses all the Vault secret engines.

The option supports the following actions:

* delete
* dump
* transfer

An example of using:

```
./kv_vault_cli.py delete --vault-token="VAULT TOKEN" --vault-addr="VAULT ADDR" \
                         --vault-root-path="secret/super-secret/dont-touch/dont-delete/"
```
## Limitation

The tool doesn't support [KV Secrets Engine - Version 2](https://www.vaultproject.io/api/secret/kv/kv-v2.html)
