import subprocess, sys
def run(*args):
    r = subprocess.run([sys.executable, "convert.py", *args], capture_output=True, text=True)
    return r
assert run("1", "km", "m").stdout.strip() == "1000"
assert abs(float(run("1", "kg", "lb").stdout.strip()) - 2.20462) < 1e-4
assert run("100", "c", "f").stdout.strip() == "212"
assert run("abc", "m", "km").returncode != 0
assert run("1", "m", "kg").returncode != 0
print("all tests passed")
