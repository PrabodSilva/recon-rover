# Recon Rover

A wireless security auditing tool that scans nearby Wi-Fi networks, grades
their security, detects new and suspicious access points, and produces a
security report and coverage heatmap.

## What it does

- Scans nearby Wi-Fi networks and reads their public information
- Grades each network's security (Open/WEP = critical, up to WPA3 = strong)
- Detects new networks that appear since a saved baseline (rogue detection)
- Flags possible "evil-twin" networks (same name, different hardware)
- Generates a written security audit report
- Draws a signal-strength heatmap of the surveyed area
- Shows everything on a live web dashboard that re-scans automatically

## Why

Wireless site surveys are usually done by hand and rarely repeated, so a rogue
access point can sit unnoticed for months. This tool automates the survey and
makes it repeatable.

## How it works

The tool reads the network information that every access point broadcasts
publicly (beacon frames). It never connects to, logs into, or reads traffic
from any network. See ETHICS below.

## Tech

Python, Flask, matplotlib. Built and tested on Windows using the built-in
`netsh` Wi-Fi scan. A Raspberry Pi rover version is planned so it can survey
a site by driving itself.

## Running it

    pip install flask matplotlib scipy
    python webapp.py

Then open http://127.0.0.1:5000

## Ethics and scope

This tool is observational: it only reads publicly broadcast network
information and never connects to any network. It was tested only on my own
home network. Any network names shown in screenshots are my own or redacted.

## Limitations

- Windows reports signal as a percentage, converted to dBm approximately.
- `netsh` returns cached scan results; Windows refreshes on its own schedule,
  so a new network can take up to a minute to appear.
- Position for the heatmap is entered by hand (the rover version will measure it).
- Built-in laptop adapters do a normal active scan, not monitor-mode capture.

## What's next

- Raspberry Pi rover so the survey drives itself
- Bluetooth/BLE scanning
- Scheduled patrols with alerts on new devices