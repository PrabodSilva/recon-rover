rover_name = "Recon Rover"
ssid = "HomeNetwork"
channel = 6
signal = -47

print(rover_name)
print(ssid)
print(channel)
print(signal)
print(f"{ssid} is on channel {channel} at {signal} dBm")


my_ssid = "Dialog 4G 088"
my_channel = 2
my_percent = 85
my_dbm = (my_percent / 2) - 100

print(f"{my_ssid} is on channel {my_channel} at {my_dbm} dBm")