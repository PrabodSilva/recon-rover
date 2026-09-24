import subprocess


def run_scan():
    result = subprocess.run(
        ["netsh", "wlan", "show", "networks", "mode=bssid"],
        capture_output=True,
        text=True
    )
    return result.stdout


def parse_netsh(text):
    networks = []
    ssid = ""
    security = ""

    for line in text.split("\n"):
        line = line.strip()
        if ":" not in line:
            continue

        label, value = line.split(":", 1)
        label = label.strip()
        value = value.strip()

        if label.startswith("SSID") and not label.startswith("BSSID"):
            ssid = value
        elif label == "Authentication":
            security = value
        elif label.startswith("BSSID"):
            networks.append({"ssid": ssid, "security": security, "bssid": value})
        elif label == "Signal":
            percent = int(value.replace("%", "").strip())
            networks[-1]["signal_percent"] = percent
            networks[-1]["signal_dbm"] = (percent / 2) - 100
        elif label == "Channel":
            networks[-1]["channel"] = int(value)

    return networks


def grade_security(security):
    if "Open" in security or "WEP" in security:
        return "F"
    elif "WPA3" in security:
        return "A"
    elif "WPA2" in security:
        return "C"
    elif "WPA" in security:
        return "D"
    return "?"


if __name__ == "__main__":
    text = run_scan()
    scan = parse_netsh(text)

    print(f"Found {len(scan)} access points\n")

    for network in scan:
        g = grade_security(network["security"])
        ssid = network["ssid"] or "(hidden)"
        channel = network.get("channel", "?")
        dbm = network.get("signal_dbm", "?")
        print(f"{ssid:<22} ch{channel:<4} {dbm} dBm   {network['security']:<16} grade {g}")