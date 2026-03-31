import unittest

from lifting_lug_calculator.core import ALLOWABLE_RULES, calculate_lug_stresses


class CalculateLugStressesTests(unittest.TestCase):
    def setUp(self):
        self.base_params = {
            "fv": 98.1,
            "kd": 1.25,
            "theta_deg": 60,
            "t": 20,
            "t_p": 0,
            "d": 52,
            "dp": 50,
            "r": 75,
            "w": 150,
            "hf": 12,
            "fy": 355,
            "fu": 470,
            "ns": 3,
        }

    def test_returns_expected_metrics_for_valid_input(self):
        results = calculate_lug_stresses(**self.base_params)

        self.assertNotIn("error", results)
        self.assertAlmostEqual(results["t_eff"], 20)
        self.assertAlmostEqual(results["areas"]["net_area"], 1960.0)
        self.assertAlmostEqual(results["areas"]["bearing_area"], 1000.0)
        self.assertAlmostEqual(
            results["metrics"]["tensile"]["allowable"],
            ALLOWABLE_RULES["tensile"]["compute"](355, 470, 3),
        )
        self.assertAlmostEqual(
            results["metrics"]["weld"]["allowable"],
            ALLOWABLE_RULES["weld"]["compute"](355, 470, 3),
        )

    def test_rejects_pin_larger_than_hole(self):
        params = dict(self.base_params, dp=54)

        results = calculate_lug_stresses(**params)

        self.assertEqual(results["error"], "销轴直径 dp 不能大于孔径 d。")

    def test_rejects_invalid_edge_distance(self):
        params = dict(self.base_params, r=26)

        results = calculate_lug_stresses(**params)

        self.assertIn("几何尺寸输入错误", results["error"])

    def test_uses_reinforcement_in_effective_thickness(self):
        params = dict(self.base_params, t_p=10)

        results = calculate_lug_stresses(**params)

        self.assertEqual(results["t_eff"], 40)
        self.assertLess(
            results["metrics"]["tensile"]["value"],
            calculate_lug_stresses(**self.base_params)["metrics"]["tensile"]["value"],
        )


if __name__ == "__main__":
    unittest.main()
