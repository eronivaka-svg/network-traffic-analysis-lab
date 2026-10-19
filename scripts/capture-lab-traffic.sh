#!/usr/bin/env bash
# Newly written portfolio helper. Not a copy of an original course file.
# Run only on the authorized disposable Labtainer 'box1' virtual interface.
set -euo pipefail
if [[ "${RUN_ONLY_INSIDE_LABTAINERS:-}" != "YES" ]]; then
  echo 'Only run in the authorized two-host Labtainer lab: set RUN_ONLY_INSIDE_LABTAINERS=YES' >&2
  exit 2
fi
ip addr show dev eth0
arp -a || true
# Capture ~20 packets. On box2, run 'ping -c 2 172.0.0.2' and 'ssh 172.0.0.2'.
# Use Ctrl+C to stop earlier if needed.
sudo tcpdump -vv -n -e -i eth0 -c 20 '(arp or icmp or (tcp and port 22))'
