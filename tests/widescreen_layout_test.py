#!/usr/bin/env python3
"""Static regression checks for the optional 16:9 Android layout."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WidescreenLayoutTests(unittest.TestCase):
    def test_widescreen_build_uses_a_1066_by_600_logical_canvas(self):
        constants = (ROOT / "src" / "GameConstants.h").read_text(encoding="utf-8")
        app = (ROOT / "src" / "LawnApp.cpp").read_text(encoding="utf-8")

        self.assertIn("WIDESCREEN_WIDTH = 1066", constants)
        self.assertIn("WIDESCREEN_PAD = (WIDESCREEN_WIDTH - BOARD_WIDTH) / 2", constants)
        self.assertIn("mWidth = WIDESCREEN_WIDTH", app)

    def test_viewport_uses_the_logical_canvas_aspect_ratio(self):
        viewport = (ROOT / "src" / "SexyAppFramework" / "graphics" / "GLInterface.cpp").read_text(encoding="utf-8")

        self.assertIn("const int logicalWidth = mApp->mWidth", viewport)
        self.assertIn("const int logicalHeight = mApp->mHeight", viewport)
        self.assertIn("width * logicalHeight", viewport)
        self.assertIn("height * logicalWidth", viewport)

    def test_android_workflow_enables_the_optional_widescreen_build(self):
        workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

        self.assertIn("-DPVZ_WIDESCREEN=ON", workflow)
        self.assertIn('branches: [ "main", "codex/widescreen-android" ]', workflow)
        self.assertIn("if: github.ref_name != 'codex/widescreen-android'", workflow)


if __name__ == "__main__":
    unittest.main()
