from flask import Flask, jsonify
import scanner
import analyzer

app = Flask(__name__)


@app.route("/api/scan")
def api_scan():
    return jsonify(analyzer.analyze(scanner.scan()))


@app.route("/")
def home():
    return PAGE


PAGE = """<!DOCTYPE html>
<html>
<head>
  <title>Recon Rover</title>
  <style>
    body { font-family: sans-serif; margin: 40px; background:#111; color:#eee; }
    h1 { border-bottom: 3px solid #0f766e; padding-bottom: 8px; }
    table { border-collapse: collapse; width: 100%; }
    th { background:#0f766e; color:#fff; padding:8px; text-align:left; }
    td { border:1px solid #444; padding:8px; }
    .F { color:#f87171; font-weight:bold; }
    .A { color:#34d399; font-weight:bold; }
  </style>
</head>
<body>
  <h1>Recon Rover - Live Wi-Fi Security</h1>
  <p id="count">scanning...</p>
  <table id="tbl"></table>

  <script>
    function refresh() {
      fetch("/api/scan").then(r => r.json()).then(nets => {
        document.getElementById("count").textContent =
            "Found " + nets.length + " networks";
        let rows = "<tr><th>SSID</th><th>Channel</th><th>Signal</th>" +
                   "<th>Security</th><th>Grade</th></tr>";
        for (const n of nets) {
          rows += "<tr><td>" + (n.ssid || "(hidden)") + "</td>" +
                  "<td>" + (n.channel || "?") + "</td>" +
                  "<td>" + (n.signal_dbm || "?") + " dBm</td>" +
                  "<td>" + n.security + "</td>" +
                  "<td class='" + n.grade + "'>" + n.grade + "</td></tr>";
        }
        document.getElementById("tbl").innerHTML = rows;
      });
    }
    refresh();
    setInterval(refresh, 3000);
  </script>
</body>
</html>"""


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)