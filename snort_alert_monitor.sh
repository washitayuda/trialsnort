#!/bin/bash
tail -Fn0 /var/log/snort/alert_fast.txt | while read line; do
    /usr/local/bin/snort_telegram.py "$line"
done