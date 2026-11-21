<div align="center">

<!-- Ganti URL gambar di bawah dengan banner GitHub repo / logo MFX Official kau jika ada -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:1f2937,100:eab308&height=220&section=header&text=MFX%20OFFICIAL&fontSize=55&fontColor=facc15&animation=fadeIn&fontAlignY=38&desc=WIRELESS%20NETWORK%20ANALYZER%20%7C%20TERMUX%20EDITION&descAlignY=62&descSize=18" width="100%" alt="MFX Official Banner"/>

<br/>

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20Termux-000000?style=for-the-badge&logo=android&logoColor=3DDC84)
![API](https://img.shields.io/badge/Termux:API-Required-06B6D4?style=for-the-badge&logo=gnubash&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-EAB308?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-22C55E?style=for-the-badge)

**Passive Wi-Fi Information Scanner & Network Diagnostic Toolkit for Termux**

[Features](#-features) • [Screenshots](#-screenshots) • [Architecture](#-how-it-works) • [Installation](#-installation) • [Usage](#-usage) • [Disclaimer](#-disclaimer)

</div>

---

## Overview

**MFX OFFICIAL | Wireless Network Analyzer** is a lightweight, color-coded CLI utility built in Python for **Termux** on Android. It combines passive wireless access point scanning via `Termux:API` with essential network diagnostic modules—including local/public IP profiling, latency testing, DNS resolution, and TCP port checks—inside a clean terminal HUD.

---

## Features

| Menu | Module | Description |
| :---: | :--- | :--- |
| **`[1]`** | **Passive Wi-Fi Scan** | Scans surrounding APs via `termux-wifi-scaninfo` and displays SSID, BSSID, RSSI (dBm), signal rating, frequency, band (`2.4 / 5 / 6 GHz`), channel, bandwidth, and security protocols. |
| **`[2]`** | **Main IP Analysis** | Inspects active network interface, Local IP, Default Gateway, DNS servers, and Public IP metadata (ASN/ISP, city, region, country, timezone). |
| **`[3]`** | **Ping & Latency Check** | Measures packet delivery and round-trip latency (`ms`) to any target IPv4 address or domain. |
| **`[4]`** | **DNS & TCP Port Check** | Resolves host IP addresses and probes custom or common TCP ports (`80, 443, 22, 53`, etc.). |
| **`[5]`** | **Active Wi-Fi Info** | Displays real-time metadata of the currently connected Wi-Fi network via `termux-wifi-connectioninfo`. |

---

## Screenshots

> **Tip:** Upload your Termux screenshots into an `assets/` folder in your repository (e.g., `assets/menu.png`, `assets/wifi_scan.png`, `assets/ip_analysis.png`) so they render automatically below.

<div align="center">

| Main Menu HUD | Wi-Fi Scan Output |
| :---: | :---: |
| ![Main Menu](assets/menu.png) | ![Wi-Fi Scan](assets/wifi_scan.png) |

| Main IP Analysis | DNS & Port Check |
| :---: | :---: |
| ![IP Analysis](assets/ip_analysis.png) | ![Port Check](assets/port_check.png) |

</div>

### Terminal Preview

```text
====================================================================================================
                              MFX OFFICIAL | WIRELESS NETWORK ANALYZER
                                  PASSIVE WIFI SCAN  |  TERMUX:API
====================================================================================================

 [1] Scan Wi-Fi
 [2] Main IP Analysis (Local, Gateway, DNS & Public IP)
 [3] Ping & Latency Check
 [4] DNS & TCP Port Quick Check
 [5] Active Wi-Fi Connection Info
 [6] Exit

 MFX@WIFI >
