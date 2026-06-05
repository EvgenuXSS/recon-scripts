import requests
import sys
import time

# простая проверка сабдоменов по вордлисту
# использую для разведки перед багбаунти

def check_sub(domain, wordlist_path):
    try:
        with open(wordlist_path, 'r') as f:
            subs = f.read().splitlines()
    except FileNotFoundError:
        print(f"[-] wordlist not found: {wordlist_path}")
        sys.exit(1)

    found = []
    print(f"[*] checking {len(subs)} subdomains for {domain}\n")

    for sub in subs:
        target = f"http://{sub}.{domain}"
        try:
            r = requests.get(target, timeout=3, allow_redirects=True)
            print(f"[+] {target} -> {r.status_code}")
            found.append(target)
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        except Exception as e:
            pass
        time.sleep(0.1)  # чтоб не банили

    print(f"\n[*] done. found {len(found)} subdomains")
    return found

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"usage: python3 {sys.argv[0]} <domain> <wordlist>")
        print(f"example: python3 {sys.argv[0]} example.com wordlists/small.txt")
        sys.exit(0)

    results = check_sub(sys.argv[1], sys.argv[2])
    if results:
        print("\nfound subdomains:")
        for r in results:
            print(f"  {r}")
