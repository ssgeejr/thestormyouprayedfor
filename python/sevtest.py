#!/usr/bin/env python3
"""
sevtest.py - System health check report
Checks user login activity (last 7 days) and CPU usage (last hour)
"""

import subprocess
import shutil
from datetime import datetime, timedelta
from pathlib import Path


def get_last_login_users(days: int = 7) -> list[dict]:
    """Get users who logged in within the specified number of days."""
    cutoff = datetime.now() - timedelta(days=days)
    cutoff_str = cutoff.strftime("%Y-%m-%d %H:%M:%S")
    
    # Use last command with time filter
    try:
        result = subprocess.run(
            ["last", "-s", cutoff_str],
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.strip().split("\n")[2:]  # Skip header and blank line
        
        users = []
        for line in lines:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 5:
                users.append({
                    "user": parts[0],
                    "tty": parts[1],
                    "login_time": " ".join(parts[2:5]),
                    "duration": parts[-1] if parts[-1] != "still" else " ".join(parts[-2:])
                })
        return users
    except subprocess.CalledProcessError as e:
        return [{"error": f"last command failed: {e.stderr}"}]


def get_cpu_usage() -> dict:
    """Get CPU usage statistics."""
    try:
        # Get CPU info from /proc/stat
        with open("/proc/stat", "r") as f:
            cpu_line = f.readline()
        
        parts = cpu_line.split()
        if parts[0] == "cpu":
            user = int(parts[1])
            nice = int(parts[2])
            system = int(parts[3])
            idle = int(parts[4])
            iowait = int(parts[5]) if len(parts) > 5 else 0
            irq = int(parts[6]) if len(parts) > 6 else 0
            softirq = int(parts[7]) if len(parts) > 7 else 0
            
            total = user + nice + system + idle + iowait + irq + softirq
            active = total - idle
            usage = (active / total * 100) if total > 0 else 0
            
            return {
                "user_pct": round(user / total * 100, 1) if total > 0 else 0,
                "system_pct": round(system / total * 100, 1) if total > 0 else 0,
                "idle_pct": round(idle / total * 100, 1) if total > 0 else 0,
                "iowait_pct": round(iowait / total * 100, 1) if total > 0 else 0,
                "total_usage_pct": round(usage, 1)
            }
    except (IOError, ZeroDivisionError) as e:
        return {"error": str(e)}
    
    return {"error": "Failed to parse CPU stats"}


def get_uptime() -> str:
    """Get system uptime."""
    try:
        result = subprocess.run(
            ["uptime", "-p"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "Unknown"


def generate_report() -> str:
    """Generate formatted report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = []
    report.append("=" * 60)
    report.append("SYSTEM HEALTH CHECK REPORT")
    report.append(f"Generated: {timestamp}")
    report.append("=" * 60)
    report.append("")
    
    # Uptime section
    report.append("📦 SYSTEM UPTIME")
    report.append("-" * 40)
    report.append(f"  {get_uptime()}")
    report.append("")
    
    # CPU Usage section
    cpu = get_cpu_usage()
    report.append("⚡ CPU USAGE (Last Hour)")
    report.append("-" * 40)
    if "error" in cpu:
        report.append(f"  ERROR: {cpu['error']}")
    else:
        report.append(f"  Total Usage:  {cpu['total_usage_pct']}%")
        report.append(f"  User Mode:    {cpu['user_pct']}%")
        report.append(f"  System Mode:  {cpu['system_pct']}%")
        report.append(f"  Idle:         {cpu['idle_pct']}%")
        report.append(f"  I/O Wait:     {cpu['iowait_pct']}%")
    report.append("")
    
    # Login Activity section
    users = get_last_login_users(7)
    report.append("👤 USERS LOGGED IN (Last 7 Days)")
    report.append("-" * 40)
    if users:
        for user in users:
            if "error" in user:
                report.append(f"  ERROR: {user['error']}")
            else:
                report.append(f"  {user['user']:15} | {user['tty']:10} | {user['login_time']}")
    else:
        report.append("  No login activity found in the last 7 days.")
    report.append("")
    
    report.append("=" * 60)
    report.append("END OF REPORT")
    report.append("=" * 60)
    
    return "\n".join(report)


def save_report(filepath: str = "sevtest_report.txt"):
    """Save report to file."""
    report = generate_report()
    with open(filepath, "w") as f:
        f.write(report)
    return filepath


if __name__ == "__main__":
    report = generate_report()
    print(report)
    
    # Save to file
    save_path = save_report("sevtest_report.txt")
    print(f"\n✅ Report saved to: {save_path}")