#!/usr/bin/env python3
"""New portfolio helper, NOT part of the original coursework.

Summarize a TSV exported by tshark. No third-party Python libraries needed.
To export from YOUR OWN lab PCAP:
    tshark -r lab.pcap -T fields -E header=y -E separator=/t \
      -e frame.number -e frame.protocols -e ip.src -e ip.dst \
      -e tcp.srcport -e tcp.dstport -e tcp.flags -e arp.opcode > packets.tsv
Usage: python3 tools/packet_summary.py packets.tsv
"""
import csv
import collections
import pathlib
import sys

if len(sys.argv) != 2:
    sys.exit('Usage: python3 tools/packet_summary.py <tshark-export.tsv>')
path = pathlib.Path(sys.argv[1])
counts = collections.Counter()
ports = collections.Counter()
flags = collections.Counter()
with path.open(encoding='utf-8-sig', newline='') as source:
    for row in csv.DictReader(source, delimiter='\t'):
        protocols = (row.get('frame.protocols') or '').lower().split(':')
        for protocol in ('arp', 'icmp', 'tcp'):
            if protocol in protocols:
                counts[protocol] += 1
        if row.get('tcp.dstport'):
            ports[row['tcp.dstport']] += 1
        if row.get('tcp.flags'):
            flags[row['tcp.flags']] += 1
print('Protocols:', dict(sorted(counts.items())))
print('Destination TCP ports:', dict(sorted(ports.items())))
print('TCP flags (hex):', dict(sorted(flags.items())))
