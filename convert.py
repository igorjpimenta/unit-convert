#!/usr/bin/env python3
"""unit-convert: convert length, mass, temperature from the command line (stdlib only)."""
import argparse
import sys

LENGTH_TO_M = {"m": 1.0, "km": 1000.0, "mi": 1609.344, "ft": 0.3048}
MASS_TO_KG = {"kg": 1.0, "lb": 0.45359237}
TEMP_UNITS = ("c", "f", "k")

def convert_length(value, from_u, to_u):
    return value * LENGTH_TO_M[from_u] / LENGTH_TO_M[to_u]

def convert_mass(value, from_u, to_u):
    return value * MASS_TO_KG[from_u] / MASS_TO_KG[to_u]

def to_celsius(value, from_u):
    if from_u == "c":
        return value
    if from_u == "f":
        return (value - 32.0) * 5.0 / 9.0
    return value - 273.15  # k

def from_celsius(value, to_u):
    if to_u == "c":
        return value
    if to_u == "f":
        return value * 9.0 / 5.0 + 32.0
    return value + 273.15  # k

def convert_temp(value, from_u, to_u):
    c = to_celsius(value, from_u)
    if to_u == "k" and (c + 273.15) < 0:
        raise ValueError("result below absolute zero")
    if from_u == "k" and value < 0:
        raise ValueError("kelvin cannot be negative")
    return from_celsius(c, to_u)

def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Convert values between units.")
    p.add_argument("value", help="numeric value to convert")
    p.add_argument("from_unit", help="source unit: m, km, mi, ft, kg, lb, c, f, k")
    p.add_argument("to_unit", help="target unit (must match category)")
    return p.parse_args(argv)

def main(argv=None):
    args = parse_args(argv)
    try:
        value = float(args.value)
    except ValueError:
        print(f"error: invalid numeric value: {args.value!r}", file=sys.stderr)
        return 2
    f = args.from_unit.lower()
    t = args.to_unit.lower()
    try:
        if f in LENGTH_TO_M and t in LENGTH_TO_M:
            result = convert_length(value, f, t)
        elif f in MASS_TO_KG and t in MASS_TO_KG:
            result = convert_mass(value, f, t)
        elif f in TEMP_UNITS and t in TEMP_UNITS:
            result = convert_temp(value, f, t)
        else:
            print(f"error: incompatible or unknown units: {args.from_unit!r} -> {args.to_unit!r}", file=sys.stderr)
            print("  length: m, km, mi, ft | mass: kg, lb | temperature: c, f, k", file=sys.stderr)
            return 2
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(f"{result:g}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
