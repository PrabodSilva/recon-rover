from analyzer import grade_security


def make_report(scan):
    lines = ["RECON ROVER - WIFI SECURITY AUDIT", "=" * 40,
             f"Networks found: {len(scan)}"]

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