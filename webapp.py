import subprocess
from flask import Flask


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


app = Flask(__name__)


@app.route("/")
def home():
    scan = parse_netsh(run_scan())

    rows = ""
    for n in scan:
        grade = grade_security(n["security"])
        ssid = n["ssid"] or "(hidden)"
        channel = n.get("channel", "?")
        dbm = n.get("signal_dbm", "?")

        if grade == "F":
            note = "Critical"
        elif grade == "A":
            note = "Strong"
        elif grade == "C":
            note = "Acceptable"
        else:
            note = ""

        rows += f"""<tr>
            <td>{ssid}</td><td>{channel}</td><td>{dbm} dBm</td>
            <td>{n['security']}</td><td><b>{grade}</b> {note}</td>
        </tr>"""

    return f"""
    <html>
    <head>
      <title>Recon Rover</title>
      <style>
        body {{ font-family: sans-serif; margin: 40px; }}
        h1 {{ border-bottom: 3px solid #333; padding-bottom: 8px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th {{ background: #333; color: white; padding: 8px; text-align: left; }}
        td {{ border: 1px solid #ccc; padding: 8px; }}
        tr:nth-child(even) {{ background: #f4f4f4; }}
      </style>
    </head>
    <body>
      <h1>Recon Rover - Wi-Fi Security Scan</h1>
      <p>Found {len(scan)} networks near you.</p>
      <table>
        <tr><th>SSID</th><th>Channel</th><th>Signal</th><th>Security</th><th>Grade</th></tr>
        {rows}
      </table>
      <p style="color:#888; font-size:13px;">
        Observational tool - reads public Wi-Fi information only. Never connects.
      </p>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)