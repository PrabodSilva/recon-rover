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


def make_report(scan):
    lines = []
    lines.append("RECON ROVER - WIFI SECURITY AUDIT")
    lines.append("=" * 40)
    lines.append(f"Networks found: {len(scan)}")

    counts = {}
    for n in scan:
        g = grade_security(n["security"])
        counts[g] = counts.get(g, 0) + 1
    lines.append(f"Grades: {counts}")
    lines.append(f"Critical (grade F): {counts.get('F', 0)}")

    lines.append("")
    lines.append("FINDINGS")
    lines.append("-" * 40)
    for n in scan:
        g = grade_security(n["security"])
        ssid = n["ssid"] or "(hidden)"
        lines.append(f"[{g}] {ssid}  ch{n.get('channel','?')}  {n['security']}")
        if g == "F":
            lines.append("     ! Critical: no effective encryption")
        ch = n.get("channel", 99)
        if ch not in (1, 6, 11) and ch <= 13:
            lines.append(f"     - Channel {ch} overlaps; recommend 1, 6 or 11")

    return "\n".join(lines)


if __name__ == "__main__":
    scan = [
        {"ssid": "Dialog 4G 088", "channel": 2,  "security": "WPA2-Personal"},
        {"ssid": "CafeGuest",     "channel": 11, "security": "Open"},
    ]
    report = make_report(scan)
    print(report)

    with open("audit_report.txt", "w") as f:
        f.write(report)
    print("\nSaved to audit_report.txt")