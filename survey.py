import json


def add_reading(readings, x, y, signal_dbm):
    readings.append({"x": x, "y": y, "signal_dbm": signal_dbm})


if __name__ == "__main__":
    readings = []

    add_reading(readings, 0.5, 0.5, -45)
    add_reading(readings, 4.5, 0.5, -70)
    add_reading(readings, 0.5, 4.5, -60)
    add_reading(readings, 4.5, 4.5, -82)
    add_reading(readings, 2.5, 2.5, -58)
    add_reading(readings, 1.0, 3.0, -52)
    add_reading(readings, 3.5, 1.5, -66)

    with open("survey.json", "w") as f:
        json.dump(readings, f, indent=2)

    print(f"Saved {len(readings)} readings to survey.json")