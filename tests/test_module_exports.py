import unittest

from matplotlib.figure import Figure

from lifting_lug_calculator.core import CalculationInputs, calculate_lug_stresses_from_inputs
from lifting_lug_calculator.reporting import ReportParams, generate_word_report
from lifting_lug_calculator.visualization import draw_lug_diagram


class ModuleSmokeTests(unittest.TestCase):
    def setUp(self):
        self.inputs = CalculationInputs(
            fv=98.1,
            kd=1.25,
            theta_deg=60,
            t=20,
            t_p=0,
            d=52,
            dp=50,
            r=75,
            w=150,
            hf=12,
            fy=355,
            fu=470,
            ns=3,
        )

    def test_typed_core_api_returns_result_object(self):
        result = calculate_lug_stresses_from_inputs(self.inputs)

        self.assertAlmostEqual(result.t_eff, 20)
        self.assertTrue(result.metrics.tensile.passed)

    def test_word_report_returns_readable_bytes(self):
        results = calculate_lug_stresses_from_inputs(self.inputs).to_dict()
        params = ReportParams(
            fv_ton=10,
            fv=98.1,
            kd=1.25,
            theta=60,
            t=20,
            tp=0,
            d=52,
            dp=50,
            r=75,
            h=80,
            w=150,
            hf=12,
            fy=355,
            fu=470,
            ns=3,
        )

        payload = generate_word_report(params, results)

        self.assertGreater(len(payload.getvalue()), 0)

    def test_diagram_returns_matplotlib_figure(self):
        figure = draw_lug_diagram(150, 75, 80, 52, 20, 0, 60)

        self.assertIsInstance(figure, Figure)


if __name__ == "__main__":
    unittest.main()
