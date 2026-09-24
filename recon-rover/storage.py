import json


def save_scan(scan, filename):
    with open(filename, "w") as f:
        json.dump(scan, f, indent=2)


def load_scan(filename):
    with open(filename) as f:
        return json.load(f)