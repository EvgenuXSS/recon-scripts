# recon-scripts

small collection of python scripts i use for ctf prep and bug bounty recon. nothing fancy, just stuff that saves time.

## scripts

### `subdomain_check.py`
checks subdomains from a wordlist using http requests. not as fast as subfinder but works without installing anything extra.

```
python3 subdomain_check.py target.com wordlists/small.txt
```

### `portscan.py`
multithreaded port scanner. faster than scanning with socket one by one.

```
python3 portscan.py 192.168.1.1
python3 portscan.py 192.168.1.1 1 65535
```

### `header_check.py`
checks security headers on a target. useful for finding low-hanging fruit in bug bounty (missing CSP, clickjacking, etc.)

```
python3 header_check.py https://example.com
```

## requirements

```
pip install requests
```

## wordlists

i use [SecLists](https://github.com/danielmiessler/SecLists) mostly. for quick checks `Discovery/DNS/subdomains-top1million-5000.txt` is enough.

---

*use only on targets you have permission to test*
