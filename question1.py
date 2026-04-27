import sys

try:
    if len(sys.argv) != 3:
        raise ValueError

    total_load = float(sys.argv[1])
    num_supports = float(sys.argv[2])

    if num_supports == 0:
        print("Error: Cannot divide by zero! Supports must be greater than zero.")
    else:
        result = total_load / num_supports
        print(f"Load per support point: {result:.2f} N")

except ValueError:
    print("Error: Invalid input! Enter numeric values only.")
