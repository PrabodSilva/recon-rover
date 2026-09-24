def grade_security(security):
    if "Open" in security or "WEP" in security:
        return "F"
    if "WPA3" in security:
        return "A"
    if "WPA2" in security:
        return "C"
    if "WPA" in security:
        return "D"
    return "?"


def analyze(scan):
    """Add a 'grade' to every network."""
    for n in scan:
        n["grade"] = grade_security(n["security"])
    return scan


def find_new_networks(baseline, current):
    known = [n["bssid"] for n in baseline]
    return [n for n in current if n["bssid"] not in known]


def find_evil_twins(scan):
    suspects = []
    for a in scan:
        for b in scan:
            if a["ssid"] == b["ssid"] and a["bssid"] != b["bssid"]:
                if a["security"] != b["security"]:
                    suspects.append((a, b))
    return suspects