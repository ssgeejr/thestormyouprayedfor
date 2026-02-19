#!/usr/bin/env python3
"""Tests for add_numbers.py"""

import os
import subprocess
import sys


def run_script(args):
    """Run add_numbers.py with given arguments and return (exit_code, output, error)."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "add_numbers.py")
    cmd = [sys.executable, script_path] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def test_alpha_input():
    """Test that alphabetic input is rejected."""
    code, out, err = run_script(["abc", "5"])
    assert code == 1, f"Expected exit code 1, got {code}"
    assert "not a valid number" in err.lower(), f"Expected error about invalid number, got: {err}"
    print("✓ Alpha input rejected")


def test_single_arg():
    """Test that only 1 argument is rejected."""
    code, out, err = run_script(["5"])
    assert code == 1, f"Expected exit code 1, got {code}"
    assert "Usage" in err or "not a valid number" in err.lower(), f"Expected usage or error, got: {err}"
    print("✓ Single argument rejected")


def test_three_args():
    """Test that more than 2 arguments is rejected."""
    code, out, err = run_script(["1", "2", "3"])
    assert code == 1, f"Expected exit code 1, got {code}"
    assert "Usage" in err, f"Expected usage message, got: {err}"
    print("✓ Three arguments rejected")


def test_two_valid_numbers():
    """Test that two valid numbers produce correct sum."""
    code, out, err = run_script(["3", "4"])
    assert code == 0, f"Expected exit code 0, got {code}"
    assert out == "7.0", f"Expected '7.0', got '{out}'"
    print("✓ Two valid numbers: 3 + 4 = 7.0")


def test_negative_numbers():
    """Test with negative numbers."""
    code, out, err = run_script(["-5", "10"])
    assert code == 0, f"Expected exit code 0, got {code}"
    assert out == "5.0", f"Expected '5.0', got '{out}'"
    print("✓ Negative numbers: -5 + 10 = 5.0")


def test_float_numbers():
    """Test with floating point numbers."""
    code, out, err = run_script(["2.5", "3.5"])
    assert code == 0, f"Expected exit code 0, got {code}"
    assert out == "6.0", f"Expected '6.0', got '{out}'"
    print("✓ Float numbers: 2.5 + 3.5 = 6.0")


def main():
    tests = [
        test_alpha_input,
        test_single_arg,
        test_three_args,
        test_two_valid_numbers,
        test_negative_numbers,
        test_float_numbers,
    ]
    
    failed = []
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed.append((test.__name__, str(e)))
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed.append((test.__name__, str(e)))
    
    print()
    if failed:
        print(f"FAILED: {len(failed)} test(s) failed")
        for name, msg in failed:
            print(f"  - {name}: {msg}")
        sys.exit(1)
    else:
        print("SUCCESS: All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()