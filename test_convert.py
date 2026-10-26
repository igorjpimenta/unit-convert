"""Full test suite for convert.py (stdlib only, unittest). Run: python3 test_convert.py"""
import subprocess
import sys
import unittest

CONVERT = "convert.py"


def run(*args):
    return subprocess.run(
        [sys.executable, CONVERT, *args],
        capture_output=True, text=True,
    )


def converts(args):
    r = run(*args)
    assert r.returncode == 0, f"{args}: rc={r.returncode} stderr={r.stderr!r}"
    return float(r.stdout.strip())


def rejects(args):
    r = run(*args)
    assert r.returncode != 0, f"{args}: expected failure, got {r.stdout!r}"
    assert r.returncode == 2, f"{args}: expected exit 2, got {r.returncode}"
    return r


class TestLength(unittest.TestCase):
    def test_km_to_m(self):
        self.assertEqual(converts(["1", "km", "m"]), 1000)

    def test_m_to_km(self):
        self.assertAlmostEqual(converts(["1", "m", "km"]), 0.001)

    def test_mi_to_m(self):
        self.assertAlmostEqual(converts(["1", "mi", "m"]), 1609.344, places=2)  # %g: 6 sig figs

    def test_mi_to_km(self):
        self.assertAlmostEqual(converts(["1", "mi", "km"]), 1.609344, places=5)  # %g: 6 sig figs

    def test_ft_to_m(self):
        self.assertAlmostEqual(converts(["1", "ft", "m"]), 0.3048)

    def test_m_to_ft(self):
        self.assertAlmostEqual(converts(["1", "m", "ft"]), 1 / 0.3048, places=4)  # %g: 6 sig figs

    def test_mi_to_ft(self):
        self.assertEqual(converts(["2", "mi", "ft"]), 10560)

    def test_km_to_mi(self):
        self.assertAlmostEqual(converts(["1", "km", "mi"]), 1000 / 1609.344, places=6)  # %g: 6 sig figs

    def test_same_unit(self):
        self.assertEqual(converts(["1", "m", "m"]), 1)

    def test_case_insensitive(self):
        self.assertEqual(converts(["1", "KM", "M"]), 1000)


class TestMass(unittest.TestCase):
    def test_kg_to_lb(self):
        self.assertAlmostEqual(converts(["1", "kg", "lb"]), 1 / 0.45359237, places=4)

    def test_lb_to_kg(self):
        self.assertAlmostEqual(converts(["1", "lb", "kg"]), 0.45359237, places=6)  # %g: 6 sig figs

    def test_same_unit(self):
        self.assertEqual(converts(["5", "kg", "kg"]), 5)


class TestTemperature(unittest.TestCase):
    def test_c_to_f(self):
        self.assertEqual(converts(["100", "c", "f"]), 212)

    def test_f_to_c(self):
        self.assertEqual(converts(["32", "f", "c"]), 0)

    def test_c_to_k(self):
        self.assertAlmostEqual(converts(["0", "c", "k"]), 273.15)

    def test_k_to_c(self):
        self.assertAlmostEqual(converts(["273.15", "k", "c"]), 0)

    def test_f_to_k(self):
        self.assertAlmostEqual(converts(["32", "f", "k"]), 273.15)

    def test_k_to_f(self):
        self.assertAlmostEqual(converts(["273.15", "k", "f"]), 32)

    def test_zero_k_to_c(self):
        self.assertAlmostEqual(converts(["0", "k", "c"]), -273.15)

    def test_absolute_zero_boundary_c_k(self):
        self.assertAlmostEqual(converts(["-273.15", "c", "k"]), 0)

    def test_absolute_zero_boundary_f_c(self):
        self.assertAlmostEqual(converts(["-459.67", "f", "c"]), -273.15, places=2)

    def test_absolute_zero_boundary_f_k(self):
        self.assertAlmostEqual(converts(["-459.67", "f", "k"]), 0, places=6)

    def test_case_insensitive(self):
        self.assertEqual(converts(["100", "C", "F"]), 212)


class TestAbsoluteZeroGuards(unittest.TestCase):
    def test_neg_kelvin_to_c(self):
        rejects(["-1", "k", "c"])

    def test_neg_kelvin_to_k(self):
        rejects(["-1", "k", "k"])

    def test_neg_kelvin_to_f(self):
        rejects(["-5", "k", "f"])

    def test_below_zero_c_to_k(self):
        rejects(["-300", "c", "k"])

    def test_below_zero_c_to_f(self):
        # regression: used to return -508 with rc 0
        rejects(["-300", "c", "f"])

    def test_below_zero_c_to_c(self):
        # regression: used to return -300 with rc 0
        rejects(["-300", "c", "c"])

    def test_below_zero_f_to_c(self):
        # regression: used to return -295.556 with rc 0
        rejects(["-500", "f", "c"])

    def test_below_zero_f_to_f(self):
        # regression: used to return -500 with rc 0
        rejects(["-500", "f", "f"])

    def test_below_zero_f_to_k(self):
        rejects(["-500", "f", "k"])


class TestInvalidInput(unittest.TestCase):
    def test_non_numeric(self):
        r = rejects(["abc", "m", "km"])
        self.assertIn("invalid numeric value", r.stderr)

    def test_incompatible_units(self):
        r = rejects(["1", "m", "kg"])
        self.assertIn("incompatible or unknown units", r.stderr)

    def test_unknown_units(self):
        r = rejects(["1", "foo", "bar"])
        self.assertIn("incompatible or unknown units", r.stderr)

    def test_mass_to_unknown(self):
        rejects(["1", "kg", "g"])

    def test_missing_args(self):
        r = subprocess.run(
            [sys.executable, CONVERT, "1", "m"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(r.returncode, 2)

    def test_error_goes_to_stderr(self):
        r = run("abc", "m", "km")
        self.assertEqual(r.stdout.strip(), "")
        self.assertNotEqual(r.stderr.strip(), "")

    def test_success_exit_zero_and_clean_stderr(self):
        r = run("1", "km", "m")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stderr.strip(), "")
        self.assertEqual(r.stdout.strip(), "1000")


if __name__ == "__main__":
    unittest.main(verbosity=2)
