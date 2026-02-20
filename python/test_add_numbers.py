#!/usr/bin/env python3
import subprocess
import sys

def run_test(name, args, expected_exit, expected_output=None):
    cmd = ["python3", "python/add_numbers.py"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    passed = result.returncode == expected_exit
    if expected_output is not None:
        passed = passed and expected_output in result.stdout + result.stderr
    
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    if not passed:
        print(f"      Command: {' '.join(cmd)}")
        print(f"      Expected exit: {expected_exit}, got: {result.returncode}")
        print(f"      stdout: {result.stdout.strip()}")
        print(f"      stderr: {result.stderr.strip()}")
    return passed

def main():
    tests = [
        ("Alpha input", ["abc", "123"], 1, "Error"),
        ("Only 1 arg", ["123"], 1, "Usage"),
        ("More than 2 args", ["1", "2", "3"], 1, "Usage"),
        ("Two valid integers", ["5", "7"], 0, "12"),
        ("Two valid floats", ["3.5", "2.5"], 0, "6.0"),
    ]
    
    results = [run_test(name, args, expected_exit, expected_output) 
               for name, args, expected_exit, expected_output in tests]
    
    passed = sum(results)
    total = len(results)
    print(f"\n{passed}/{total} tests passed")
    
    sys.exit(0 if all(results) else 1)

if __name__ == "__main__":
    main()