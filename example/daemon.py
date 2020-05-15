#!/bin/env python3
import systemd_watchdog
import time

wd = systemd_watchdog.watchdog()

if not wd.is_enabled:
    # Then it's probably not running under systemd with watchdog enabled
    raise Exception("Watchdog not enabled")

# Report a status message
wd.status("Starting my service...")
time.sleep(1)

# Report that the program init is complete - "systemctl start" won't return until ready() called
wd.ready()
wd.notify()

timeout_half_sec = int(float(wd.timeout) / 2e6)  # Convert us->s and half that
wd.status("Waiting {} seconds (1/2)".format(timeout_half_sec))
time.sleep(timeout_half_sec)
wd.notify()

wd.status("Waiting {} seconds (2/2)".format(timeout_half_sec))
time.sleep(timeout_half_sec)
wd.notify()

count = 0
while not wd.notify_due:
    count += 1
    wd.status("Waiting for notify_due flag: iteration {}".format(count))
    time.sleep(0.1)  # BUSY LOOPS ARE BAD

# Report an error to the service manager
# wd.notify_error("Blowing up on purpose!")
# The service manager will probably kill the program here

wd.status("Simulating hang")
wd.notify()
time.sleep(120)
