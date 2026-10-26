# unit-convert

Small Python 3 CLI (stdlib only, no dependencies) that converts values between units of **length**, **mass**, and **temperature**.

## Usage

```sh
python3 convert.py <value> <from_unit> <to_unit>
```

Both units are case-insensitive and must belong to the same category. The result is printed to stdout; nothing else is printed on success.

## Supported units

| Category     | Units            |
|--------------|------------------|
| Length       | `m`, `km`, `mi`, `ft` |
| Mass         | `kg`, `lb`       |
| Temperature  | `c`, `f`, `k`    |

Temperature conversions respect physical limits: a negative Kelvin input, or a result below absolute zero (−273.15 °C), is rejected with an error.

## Examples

```sh
$ python3 convert.py 1 km m
1000

$ python3 convert.py 1 kg lb
2.20462

$ python3 convert.py 100 c f
212

$ python3 convert.py 2 mi ft
10560
```

## Invalid input & exit codes

On success the exit code is `0`. On any error the exit code is `2` and a message is written to stderr:

```sh
$ python3 convert.py abc m km
error: invalid numeric value: 'abc'      # exit code 2

$ python3 convert.py 5 m kg
error: incompatible or unknown units: 'm' -> 'kg'
  length: m, km, mi, ft | mass: kg, lb | temperature: c, f, k
  # exit code 2

$ python3 convert.py -300 c k
error: result below absolute zero        # exit code 2
```

Running the script with fewer than three arguments prints argparse's usage help and exits with code `2` as well.

## Tests

```sh
python3 test_convert.py
```

The test suite exercises the length, mass, and temperature examples above plus the invalid-input cases; it prints `all tests passed` and exits `0` when everything is fine.
