#!/usr/bin/env python3
# =====================================================
# MFX OFFICIAL | WIFI ANALYZER
# Passive Wi-Fi information scanner for Termux:API
# =====================================================

import json
import subprocess
import sys
import time
import os
import socket
import urllib.request
import urllib.error
import re

# ---------- COLOURS ----------
GOLD = "\033[38;5;220m"
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
WHITE = "\033[97m"
GREY = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"

WIDTH = 100

def line(char="=", color=GOLD):
    print(color + char * WIDTH + RESET)

def box(text, color=CYAN):
    print(color + "║ " + text + RESET)

def header():
    os.system("clear")
    line()
    print(GOLD + BOLD + "  MFX OFFICIAL | WIRELESS NETWORK ANALYZER".center(WIDTH) + RESET)
    print(CYAN + "  PASSIVE WIFI SCAN  |  TERMUX:API".center(WIDTH) + RESET)
    line()

def get_channel(freq):
    if 2412 <= freq <= 2472:
        return str((freq - 2407) // 5)
    if freq == 2484:
        return "14"
    if 5000 <= freq < 5925:
        return str((freq - 5000) // 5)
    if 5955 <= freq <= 7115:
        return str((freq - 5950) // 5)
    return "N/A"

def get_band(freq):
    if 2400 <= freq < 2500:
        return "2.4 GHz"
    if 4900 <= freq < 5925:
        return "5 GHz"
    if 5955 <= freq <= 7125:
        return "6 GHz"
    return "Unknown"

def signal_status(rssi):
    if rssi >= -50:
        return "VERY STRONG"
    elif rssi >= -60:
        return "STRONG"
    elif rssi >= -70:
        return "MEDIUM"
    elif rssi >= -80:
        return "WEAK"
    return "VERY WEAK"

def scan():
    try:
        result = subprocess.run(
            ["termux-wifi-scaninfo"],
            capture_output=True,
            text=True,
            timeout=20
        )

        if result.returncode != 0 and not result.stdout.strip():
            print(RED + " [!] Termux:API error" + RESET)
            print(result.stderr)
            return

        data = json.loads(result.stdout)

        if isinstance(data, dict):
            print(RED + "\n [!] " + str(data.get("error", data)) + RESET)
            return

        print(GREEN + f"\n [+] Records detected: {len(data)}" + RESET)
        print(GREY + " [i] Data supplied by Android Wi-Fi scan results." + RESET)

        line("-")

        for index, wifi in enumerate(data, 1):
            ssid = wifi.get("ssid") or "HIDDEN / UNKNOWN"
            bssid = wifi.get("bssid", "N/A")
            freq = wifi.get("frequency_mhz", 0)
            rssi = wifi.get("rssi", 0)
            security = wifi.get("capabilities", "N/A")
            bandwidth = wifi.get("channel_bandwidth_mhz", "N/A")

            print(GOLD + BOLD + f"\n┌─ ACCESS POINT [{index:02d}]" + RESET)
            print(CYAN + "│" + RESET)

            box(f"ID          : {index:02d}")
            box(f"SSID        : {ssid}")
            box(f"BSSID       : {bssid}")
            box(f"RSSI        : {rssi} dBm")
            box(f"SIGNAL      : {signal_status(rssi)}")
            box(f"FREQUENCY   : {freq} MHz")
            box(f"BAND        : {get_band(freq)}")
            box(f"CHANNEL     : {get_channel(freq)}")
            box(f"BANDWIDTH   : {bandwidth} MHz")
            box(f"SECURITY    : {security}")

            print(GOLD + "└" + "─" * 35 + RESET)

        line()
        print(GREEN + " [✓] ANALYSIS COMPLETED" + RESET)
        print(GREY + " [i] Passive scanning only. No connection or attack." + RESET)
        line()

    except FileNotFoundError:
        print(RED + "[!] termux-wifi-scaninfo not found." + RESET)
        print("Install Termux:API and pkg install termux-api")

    except subprocess.TimeoutExpired:
        print(RED + "[!] Scan command timed out." + RESET)

    except json.JSONDecodeError:
        print(RED + "[!] Invalid JSON response." + RESET)

    except Exception as error:
        print(RED + f"[!] Error: {error}" + RESET)


# ---------- TAMBAHAN MODUL ANALISIS IP & TOOLS ----------

def get_local_net_info():
    iface = "N/A"
    gateway = "N/A"
    local_ip = "N/A"

    try:
        route_res = subprocess.run(["ip", "route"], capture_output=True, text=True, timeout=5)
        for ln in route_res.stdout.splitlines():
            m_gw = re.search(r"default via (\S+) dev (\S+)", ln)
            if m_gw:
                gateway = m_gw.group(1)
                iface = m_gw.group(2)
                break
    except Exception:
        pass

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(3)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass

    if local_ip == "N/A" and iface != "N/A":
        try:
            addr_res = subprocess.run(["ip", "-4", "addr", "show", "dev", iface], capture_output=True, text=True, timeout=5)
            m_ip = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", addr_res.stdout)
            if m_ip:
                local_ip = m_ip.group(1)
        except Exception:
            pass

    dns_servers = []
    try:
        if os.path.exists("/etc/resolv.conf"):
            with open("/etc/resolv.conf", "r", encoding="utf-8", errors="ignore") as f:
                for ln in f:
                    if ln.strip().startswith("nameserver"):
                        parts = ln.strip().split()
                        if len(parts) >= 2:
                            dns_servers.append(parts[1])
    except Exception:
        pass

    if not dns_servers:
        for prop in ["net.dns1", "net.dns2"]:
            try:
                p_res = subprocess.run(["getprop", prop], capture_output=True, text=True, timeout=3)
                val = p_res.stdout.strip()
                if val:
                    dns_servers.append(val)
            except Exception:
                pass

    return {
        "interface": iface,
        "local_ip": local_ip,
        "gateway": gateway,
        "dns": ", ".join(dns_servers) if dns_servers else "N/A"
    }

def get_public_ip_info():
    info = {
        "ip": "N/A",
        "org": "N/A",
        "city": "N/A",
        "region": "N/A",
        "country": "N/A",
        "timezone": "N/A"
    }
    try:
        req = urllib.request.Request(
            "https://ipinfo.io/json",
            headers={"User-Agent": "MFX-Analyzer/1.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="ignore"))
            info["ip"] = payload.get("ip", "N/A")
            info["org"] = payload.get("org", "N/A")
            info["city"] = payload.get("city", "N/A")
            info["region"] = payload.get("region", "N/A")
            info["country"] = payload.get("country", "N/A")
            info["timezone"] = payload.get("timezone", "N/A")
            return info
    except Exception:
        pass

    try:
        req = urllib.request.Request(
            "https://api.ipify.org?format=json",
            headers={"User-Agent": "MFX-Analyzer/1.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="ignore"))
            info["ip"] = payload.get("ip", "N/A")
    except Exception:
        pass

    return info

def ip_analysis():
    print(GREEN + "\n [*] Analyzing main IP & network interfaces..." + RESET)
    local_info = get_local_net_info()
    pub_info = get_public_ip_info()

    line("-")
    print(GOLD + BOLD + "\n┌─ MAIN IP & NETWORK ANALYSIS" + RESET)
    print(CYAN + "│" + RESET)
    box(f"INTERFACE   : {local_info['interface']}")
    box(f"LOCAL IP    : {local_info['local_ip']}")
    box(f"GATEWAY IP  : {local_info['gateway']}")
    box(f"DNS SERVER  : {local_info['dns']}")
    box(f"PUBLIC IP   : {pub_info['ip']}")
    box(f"ASN / ISP   : {pub_info['org']}")
    box(f"LOCATION    : {pub_info['city']}, {pub_info['region']} ({pub_info['country']})")
    box(f"TIMEZONE    : {pub_info['timezone']}")
    print(GOLD + "└" + "─" * 35 + RESET)
    line()
    print(GREEN + " [✓] IP ANALYSIS COMPLETED" + RESET)
    line()

def ping_tool():
    target = input(CYAN + "\n Enter target IP or host (default: 8.8.8.8): " + RESET).strip() or "8.8.8.8"
    count = input(CYAN + " Packet count (default: 4): " + RESET).strip() or "4"
    if not count.isdigit() or int(count) <= 0:
        count = "4"

    print(GREEN + f"\n [*] Pinging {target} ({count} packets)..." + RESET)
    line("-")
    try:
        res = subprocess.run(
            ["ping", "-c", count, "-W", "3", target],
            capture_output=True,
            text=True,
            timeout=25
        )
        output = res.stdout.strip() or res.stderr.strip()
        print(WHITE + (output if output else "No output from ping.") + RESET)
    except FileNotFoundError:
        print(RED + " [!] 'ping' command not found. Install iputils (pkg install iputils)." + RESET)
    except subprocess.TimeoutExpired:
        print(RED + " [!] Ping timed out." + RESET)
    except Exception as e:
        print(RED + f" [!] Error: {e}" + RESET)
    line()

def dns_and_port_tool():
    target = input(CYAN + "\n Enter domain or IP: " + RESET).strip()
    if not target:
        print(RED + " [!] Target cannot be empty." + RESET)
        return

    print(GREEN + f"\n [*] Resolving DNS & checking common ports for {target}..." + RESET)
    line("-")
    print(GOLD + BOLD + "\n┌─ DNS RESOLUTION" + RESET)
    print(CYAN + "│" + RESET)
    try:
        addr_info = socket.getaddrinfo(target, None)
        ips = []
        for item in addr_info:
            ip_val = item[4][0]
            if ip_val not in ips:
                ips.append(ip_val)
        box(f"HOST        : {target}")
        box(f"RESOLVED IP : {', '.join(ips) if ips else 'N/A'}")
    except socket.gaierror as e:
        box(f"DNS ERROR   : {e}", RED)
    print(GOLD + "└" + "─" * 35 + RESET)

    ports_raw = input(CYAN + "\n Enter ports separated by comma (default: 80,443,22,53): " + RESET).strip() or "80,443,22,53"
    ports = []
    for p in ports_raw.split(","):
        p = p.strip()
        if p.isdigit() and 1 <= int(p) <= 65535:
            ports.append(int(p))

    if ports:
        print(GOLD + BOLD + "\n┌─ TCP PORT CHECK" + RESET)
        print(CYAN + "│" + RESET)
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.5)
            try:
                code = sock.connect_ex((target, port))
                status = GREEN + "OPEN" + RESET + CYAN if code == 0 else GREY + "CLOSED / FILTERED" + RESET + CYAN
            except Exception as ex:
                status = RED + f"ERR ({ex})" + RESET + CYAN
            finally:
                sock.close()
            box(f"PORT {port:<5} : {status}")
        print(GOLD + "└" + "─" * 35 + RESET)

    line()

def active_wifi_info():
    print(GREEN + "\n [*] Reading active Wi-Fi connection info..." + RESET)
    line("-")
    try:
        res = subprocess.run(
            ["termux-wifi-connectioninfo"],
            capture_output=True,
            text=True,
            timeout=15
        )
        if res.returncode != 0 and not res.stdout.strip():
            print(RED + " [!] Termux:API error or no active Wi-Fi." + RESET)
            if res.stderr.strip():
                print(res.stderr.strip())
            line()
            return

        data = json.loads(res.stdout)
        print(GOLD + BOLD + "\n┌─ ACTIVE WIFI CONNECTION" + RESET)
        print(CYAN + "│" + RESET)
        if isinstance(data, dict):
            for k, v in data.items():
                box(f"{str(k).upper():<18} : {v}")
        else:
            box(str(data))
        print(GOLD + "└" + "─" * 35 + RESET)
    except FileNotFoundError:
        print(RED + " [!] termux-wifi-connectioninfo not found." + RESET)
    except json.JSONDecodeError:
        print(RED + " [!] Invalid JSON response." + RESET)
    except Exception as e:
        print(RED + f" [!] Error: {e}" + RESET)
    line()


def main():
    header()

    print(CYAN + "\n [1] Scan Wi-Fi")
    print(" [2] Main IP Analysis (Local, Gateway, DNS & Public IP)")
    print(" [3] Ping & Latency Check")
    print(" [4] DNS & TCP Port Quick Check")
    print(" [5] Active Wi-Fi Connection Info")
    print(" [6] Exit" + RESET)

    choice = input(GOLD + "\n MFX@WIFI > " + RESET).strip()

    if choice == "1":
        header()
        print(GREEN + " [*] Reading Wi-Fi scan results..." + RESET)
        scan()
        input("\n Press ENTER to return...")
        main()

    elif choice == "2":
        header()
        ip_analysis()
        input("\n Press ENTER to return...")
        main()

    elif choice == "3":
        header()
        ping_tool()
        input("\n Press ENTER to return...")
        main()

    elif choice == "4":
        header()
        dns_and_port_tool()
        input("\n Press ENTER to return...")
        main()

    elif choice == "5":
        header()
        active_wifi_info()
        input("\n Press ENTER to return...")
        main()

    elif choice == "6":
        print(GOLD + "\n MFX OFFICIAL - SESSION CLOSED" + RESET)

    else:
        print(RED + "\n Invalid selection." + RESET)
        time.sleep(1)
        main()


if __name__ == "__main__":
    main()
