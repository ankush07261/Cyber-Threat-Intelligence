import os
import csv
import json
import time
import sys
import subprocess

# Force UTF-8 encoding to avoid Unicode errors in Windows CMD
sys.stdout.reconfigure(encoding='utf-8')

CSV_FILE = "capture_data.csv"
JSON_FILE = "capture_data.json"
TEMP_CSV = "temp_capture.csv"

def get_wifi_interface():
    """Find the correct Wi-Fi interface using tshark."""
    try:
        output = subprocess.check_output(["tshark", "-D"], universal_newlines=True)
        for line in output.splitlines():
            if "Wi-Fi" in line or "WLAN" in line:
                return line.split(".")[0].strip()  # Extract interface number
    except subprocess.CalledProcessError:
        print("❌ Error detecting Wi-Fi interface.")
        return None

def initialize_files():
    """Ensure CSV and JSON files exist with proper headers."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "source_ip", "destination_ip", "protocol", "packet_size"])

    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w") as file:
            json.dump([], file, indent=4)

def capture_packets(interface, capture_duration=1):
    """Capture network packets using tshark and save them to a temporary CSV file."""
    if not interface:
        print("⚠ No Wi-Fi interface found.")
        return

    command = f'tshark -i {interface} -a duration:{capture_duration} -T fields ' \
              f'-e frame.time_epoch -e ip.src -e ip.dst -e ip.proto -e frame.len ' \
              f'-E header=n -E separator=, -E quote=n > {TEMP_CSV}'
    
    print(f"📡 Capturing packets for {capture_duration} seconds on interface {interface}...")
    os.system(command)

def process_and_save_data():
    """Read captured data, append it to CSV and JSON files."""
    new_data = []
    
    if not os.path.exists(TEMP_CSV):
        print("⚠ No packets captured.")
        return

    with open(TEMP_CSV, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if not rows:
        print("⚠ No valid data in capture.")
        return

    # Append to CSV
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            if len(row) == 5 and row[0] != "frame.time_epoch":  # Ignore header-like entries
                writer.writerow(row)
                new_data.append({
                    "timestamp": row[0],
                    "source_ip": row[1],
                    "destination_ip": row[2],
                    "protocol": row[3],
                    "packet_size": row[4]
                })

    # Update JSON
    if new_data:
        with open(JSON_FILE, "r") as file:
            existing_data = json.load(file)

        existing_data.extend(new_data)

        with open(JSON_FILE, "w") as file:
            json.dump(existing_data, file, indent=4)

        print(f"✅ Updated {CSV_FILE} and {JSON_FILE} with new data.")
    else:
        print("⚠ No valid packets to save.")

def main(interval=1):
    """Main loop to continuously capture and save packets."""
    initialize_files()
    wifi_interface = get_wifi_interface()

    if not wifi_interface:
        print("❌ No Wi-Fi interface detected. Exiting.")
        return

    while True:
        capture_packets(interface=wifi_interface, capture_duration=interval)
        process_and_save_data()
        time.sleep(interval)  # Wait before next capture

if __name__ == "__main__":
    main(interval=1)  # Capture every 1 second
