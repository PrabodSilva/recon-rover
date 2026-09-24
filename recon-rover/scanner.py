import subprocess

USE_MOCK = False   # keep False on your Windows laptop to use the real scan


def run_scan():
    if USE_MOCK:
        return MOCK
    result = subprocess.run(
        ["netsh", "wlan", "show", "networks", "mode=bssid"],
        capture_output=True, text=True)
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


def scan():
    """The one function other files call: gives a clean list of networks."""
    return parse_netsh(run_scan())


MOCK = """
SSID 1 : Dialog 4G 088
    Authentication          : WPA2-Personal
    BSSID 1                 : 98:a9:42:7e:bf:f8
         Signal             : 85%
         Channel            : 2
"""


if __name__ == "__main__":
    for n in scan():
        print(n["ssid"], n.get("signal_dbm"), "dBm")