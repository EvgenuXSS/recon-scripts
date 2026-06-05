import requests
import sys
import urllib3
urllib3.disable_warnings()

# проверяю security headers на целях
# хорошо находит missing headers для отчётов

HEADERS_TO_CHECK = [
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-XSS-Protection",
    "Referrer-Policy",
    "Permissions-Policy",
    "X-Powered-By",  # это наоборот плохо если есть
    "Server",        # и это тоже
]

def check_headers(url):
    if not url.startswith("http"):
        url = "https://" + url

    try:
        r = requests.get(url, timeout=5, verify=False, allow_redirects=True)
    except Exception as e:
        print(f"[-] error: {e}")
        return

    print(f"[*] {url} -> {r.status_code}\n")

    missing = []
    present = []
    info_leak = []

    for h in HEADERS_TO_CHECK:
        val = r.headers.get(h)
        if h in ["X-Powered-By", "Server"]:
            if val:
                info_leak.append(f"  {h}: {val}")
        else:
            if val:
                present.append(f"  {h}: {val}")
            else:
                missing.append(f"  {h}")

    if present:
        print("[+] present headers:")
        for p in present:
            print(p)

    if missing:
        print("\n[-] missing headers (potential findings):")
        for m in missing:
            print(m)

    if info_leak:
        print("\n[!] info disclosure:")
        for i in info_leak:
            print(i)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: python3 {sys.argv[0]} <url>")
        sys.exit(0)
    check_headers(sys.argv[1])
