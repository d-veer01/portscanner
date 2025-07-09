import socket
import argparse
from datetime import datetime

def scan_ports(target, start_port, end_port):
    print(f"\n[+] Starting scan on {target}")
    print(f"[+] Scanning ports {start_port} to {end_port}")
    open_ports = []

    for port in range(start_port, end_port + 1):
        try:
            s = socket.socket()
            s.settimeout(0.5)
            result = s.connect_ex((target, port))

            if result == 0:
                try:
                    banner = s.recv(1024).decode().strip()
                except:
                    banner = "No banner"
                print(f"[OPEN] Port {port}: {banner}")
                open_ports.append((port, banner))
            s.close()
        except KeyboardInterrupt:
            print("\n[!] Scan aborted.")
            exit()
        except socket.error:
            pass

    return open_ports

def save_results(target, open_ports):
    filename = f"{target}_scan_results.txt"
    with open(filename, "w") as f:
        f.write(f"Scan results for {target} - {datetime.now()}\n")
        for port, banner in open_ports:
            f.write(f"Port {port}: {banner}\n")
    print(f"\n[+] Results saved to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Python Port Scanner with Banner Grabbing")
    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("-sp", "--start-port", type=int, default=1, help="Start port (default=1)")
    parser.add_argument("-ep", "--end-port", type=int, default=1024, help="End port (default=1024)")

    args = parser.parse_args()

    try:
        ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print("[!] Hostname could not be resolved.")
        exit()

    open_ports = scan_ports(ip, args.start_port, args.end_port)
    if open_ports:
        save_results(args.target, open_ports)
    else:
        print("[!] No open ports found.")
