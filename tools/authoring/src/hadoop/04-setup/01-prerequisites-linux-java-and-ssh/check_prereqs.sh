#!/usr/bin/env bash
# check_prereqs.sh: is this Linux / WSL machine ready for Hadoop 3.5?
echo "== Operating system";  grep PRETTY_NAME /etc/os-release | cut -d= -f2
echo "== CPU cores";         nproc
echo "== Memory";            free -h | awk '/Mem:/ {print $2 " total, " $7 " available"}'
echo "== Free disk in HOME"; df -h "$HOME" | awk 'NR==2 {print $4 " free"}'
echo "== Java";              if command -v java >/dev/null; then java -version 2>&1 | head -1; else echo "NOT INSTALLED"; fi
echo "== JAVA_HOME";         echo "${JAVA_HOME:-not set}"
echo "== SSH client";        command -v ssh >/dev/null && echo "installed" || echo "NOT INSTALLED"
echo "== SSH server";        (command -v sshd >/dev/null || [ -x /usr/sbin/sshd ]) && echo "installed" || echo "NOT INSTALLED"
echo "== Passwordless SSH to localhost"
if ssh -o BatchMode=yes -o ConnectTimeout=3 localhost true 2>/dev/null; then echo "OK"; else echo "NOT YET (set up keys in Lesson 4.3)"; fi
