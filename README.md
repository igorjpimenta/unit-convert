# unit-convert

Small Python 3 CLI (stdlib only) that converts length, mass, and temperature.

## Usage

```sh
python3 convert.py <value> <from_unit> <to_unit>
```

Units (case-insensitive):

- length: `m`, `km`, `mi`, `ft`
- mass: `kg`, `lb`
- temperature: `c`, `f`, `k`

## Examples

```sh
python3 convert.py 1 km m      # 1000
python3 convert.py 1 kg lb     # 2.20462
python3 convert.py 100 c f     # 212
```

Invalid input exits non-zero with an error message.

## Test

```sh
python3 test_convert.py
```
