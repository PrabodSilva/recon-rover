from storage import load_scan       #you	borrowed	the	function	from	your	other	file.	This	is	why	functions	and separate	files	matter


def find_new_networks(baseline, current):
    known = []
    for n in baseline:
        known.append(n["bssid"])

    new = []
    for n in current:
        if n["bssid"] not in known:
            new.append(n)
    return new


def find_evil_twins(scan):
    suspects = []
    for a in scan:
        for b in scan:
            if a["ssid"] == b["ssid"] and a["bssid"] != b["bssid"]:
                if a["security"] != b["security"]:
                    suspects.append((a, b))
    return suspects


def get_oui(bssid):
    return bssid[:8].upper()


if __name__ == "__main__":
    baseline = load_scan("baseline.json")

    current = baseline + [
        {"ssid": "Dialog 4G 088", "bssid": "de:ad:be:ef:13:37",
         "channel": 1, "security": "Open", "signal_dbm": -52.0},
    ]

    new = find_new_networks(baseline, current)
    print(f"{len(new)} new network(s) since baseline:")
    for n in new:
        print(f"  NEW: {n['ssid']}  ({n['bssid']})  {n['security']}")

    print()
    scan = current
    twins = find_evil_twins(scan)
    for a, b in twins:
        print(f"POSSIBLE EVIL TWIN: '{a['ssid']}'")
        print(f"  real? {b['bssid']} ({b['security']})  maker {get_oui(b['bssid'])}")
        print(f"  fake? {a['bssid']} ({a['security']})  maker {get_oui(a['bssid'])}")
        break