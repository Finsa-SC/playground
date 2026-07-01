import subprocess
import re

total_icmp = 20
max_delay = 100.0

res = subprocess.Popen(
    ["ping", "-c", f"{total_icmp}", "google.com"],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

while True:
    row = res.stdout.readline() #Get new line

    if not row.strip() and res.poll() is not None: #Skip loop if process return status code or empty line
        break

    if row:
        pattern = r'time=([\d\.]*)'
        match = re.search(pattern, row)
        if match:
            time = float(match.group(1))

            if time >= max_delay:
                print(f"Jittering detected! {time} ms")