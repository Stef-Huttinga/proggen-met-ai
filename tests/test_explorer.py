import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


class ExplorerTests(unittest.TestCase):
    def test_charts_and_controls(self):
        app = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py").run(timeout=60)
        self.assertFalse(app.exception)
        self.assertEqual(
            [tab.label for tab in app.tabs],
            ["Power plants", "Energy mix", "Relationships", "Scenario"],
        )
        self.assertEqual(len(app.get("plotly_chart")), 8)

        app.radio[0].set_value("Share within country").run(timeout=60)
        self.assertFalse(app.exception)

        phase_out = next(slider for slider in app.slider if slider.label == "Phase-out percentage")
        phase_out.set_value(0).run(timeout=60)
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[-1].value, app.metric[0].value)

        phase_out = next(slider for slider in app.slider if slider.label == "Phase-out percentage")
        phase_out.set_value(100).run(timeout=60)
        self.assertFalse(app.exception)
        self.assertLess(
            float(app.metric[-1].value.split(" t ")[0].replace(",", "")),
            float(app.metric[0].value.split(" t ")[0].replace(",", "")),
        )


if __name__ == "__main__":
    unittest.main()