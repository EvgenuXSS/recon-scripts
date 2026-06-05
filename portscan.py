import socket
import sys
import threading
from queue import Queue
from datetime import datetime

# порт сканер на питоне, сделал чтобы не зависеть от nmap на чужих машинах
# работает норм, на 1000 портов уходит секунд 10-15

open_ports = []
lock = threading.Lock()

def scan_port(host, port, timeout=1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        s.close()
        if result == 0:
            with lock:
                open_ports.append(port)
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                print(f"[+] {port}/tcp  open  {service}")
    except:
        pass

def worker(q, host):
    while not q.empty():
        port = q.get()
        scan_port(host, port)
        q.task_done()

def run_scan(host, start=1, end=1024, threads=100):
    print(f"[*] scanning {host} ports {start}-{end}")
    print(f"[*] started at {datetime.now().strftime('%H:%M:%S')}\n")

    q = Queue()
    for port in range(start, end + 1):
        q.put(port)

    thread_list = []
    for _ in range(min(threads, end - start + 1)):
        t = threading.Thread(target=worker, args=(q, host))
        t.daemon = True
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    print(f"\n[*] done. {len(open_ports)} open ports found")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: python3 {sys.argv[0]} <host> [start_port] [end_port]")
        sys.exit(0)

    host = sys.argv[1]
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end = int(sys.argv[3]) if len(sys.argv) > 3 else 1024

    run_scan(host, start, end)
