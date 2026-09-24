import json   #Python built in tool for the text document


def save_scan(scan, filename):
    with open(filename, "w") as f:  #means	write	(it	creates	or	overwrites	the	file).	With	no	"w",	open	means read.	The	with	block	closes	the	file	for	you	automatically.
        json.dump(scan, f, indent=2)    # Write	the	list-of-dictionaries	into	the	open	file	f.	indent=2	makes	it	nicely	spaced so	you	can	read	it


def load_scan(filename):
    with open(filename) as f:
        return json.load(f)     #read it back into a real Python list-of-dictionaries


if __name__ == "__main__":
    scan = [
        {"ssid": "Dialog 4G 088", "bssid": "98:a9:42:7e:bf:f8","channel": 2, "security": "WPA2-Personal", "signal_dbm": -57.5},
        {"ssid": "CafeGuest", "bssid": "c8:3a:35:de:ad:01","channel": 11, "security": "Open", "signal_dbm": -72.0},
    ]

    save_scan(scan, "baseline.json")
    print("Saved.")

    loaded = load_scan("baseline.json")
    print(f"Loaded {len(loaded)} networks back")
    print(loaded[0]["ssid"])