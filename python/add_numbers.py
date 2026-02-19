#!/usr/bin/env python3
"""Add two numbers with input validation."""

import sys


def main():
    # Check argument count
    if len(sys.argv) != 3:
        print("Usage: python add_numbers.py <num1> <num2>", file=sys.stderr)
        sys.exit(1)
    
    num1_str = sys.argv[1]
    num2_str = sys.argv[2]
    
    # Validate first argument
    try:
        num1 = float(num1_str)
    except ValueError:
        print(f"Error: '{num1_str}' is not a valid number", file=sys.stderr)
        sys.exit(1)
    
    # Validate second argument
    try:
        num2 = float(num2_str)
    except ValueError:
        print(f"Error: '{num2_str}' is not a valid number", file=sys.stderr)
        sys.exit(1)
    
    # Calculate and print sum
    result = num1 + num2
    print(result)


if __name__ == "__main__":
    main()