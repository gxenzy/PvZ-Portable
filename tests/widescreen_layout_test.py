#!/usr/bin/env python3
"""Static regression checks for the optional 16:9 Android layout."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WidescreenLayoutTests(unittest.TestCase):
    def test_widescreen_build_uses_a_1066_by_600_logical_canvas(self):
        constants = (ROOT / "src" / "GameConstants.h").read_text(encoding="utf-8")
        app = (ROOT / "src" / "LawnApp.cpp").read_text(encoding="utf-8")
        selector = (ROOT / "src" / "Lawn" / "Widget" / "GameSelector.cpp").read_text(encoding="utf-8")

        self.assertIn("WIDESCREEN_WIDTH = 1066", constants)
        self.assertIn("WIDESCREEN_PAD = (WIDESCREEN_WIDTH - BOARD_WIDTH) / 2", constants)
        self.assertIn("mWidth = WIDESCREEN_WIDTH", app)
        self.assertIn("gLawnApp->mWidth - theWidth", app)
        self.assertIn("mClip = false", selector)

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

    def test_first_run_import_does_not_start_the_sdl_runtime(self):
        manifest = (ROOT / "android" / "app" / "src" / "main" / "AndroidManifest.xml").read_text(encoding="utf-8")
        launcher = (ROOT / "android" / "app" / "src" / "main" / "java" / "io" / "github" / "wszqkzqk" / "pvzportable" / "LauncherActivity.java").read_text(encoding="utf-8")
        game_activity = (ROOT / "android" / "app" / "src" / "main" / "java" / "io" / "github" / "wszqkzqk" / "pvzportable" / "PvZPortableActivity.java").read_text(encoding="utf-8")

        self.assertIn('android:name=".LauncherActivity"', manifest)
        self.assertIn("ResourceImportActivity.class", launcher)
        self.assertIn("PvZPortableActivity.class", launcher)
        self.assertNotIn("ResourceImportActivity.class", game_activity)

    def test_modal_and_view_lawn_keep_the_game_content_centered(self):
        store = (ROOT / "src" / "Lawn" / "Widget" / "StoreScreen.cpp").read_text(encoding="utf-8")
        chooser = (ROOT / "src" / "Lawn" / "Widget" / "SeedChooserScreen.cpp").read_text(encoding="utf-8")
        cutscene = (ROOT / "src" / "Lawn" / "CutScene.cpp").read_text(encoding="utf-8")

        self.assertIn("Resize(GAME_SCREEN_OFFSET_X, 0, BOARD_WIDTH, BOARD_HEIGHT)", store)
        self.assertIn("mApp->mSeedChooserScreen->Move(GAME_SCREEN_OFFSET_X, SEED_CHOOSER_OFFSET_Y)", cutscene)
        self.assertIn("int aBoardX = BOARD_IMAGE_WIDTH_OFFSET - BOARD_WIDTH", chooser)
        self.assertIn("mBoard->Move(GAME_SCREEN_OFFSET_X - PvzpAnimateCurve", chooser)
        self.assertIn("Move(GAME_SCREEN_OFFSET_X, SEED_CHOOSER_OFFSET_Y)", chooser)

    def test_widescreen_draws_original_textures_across_the_full_canvas(self):
        title = (ROOT / "src" / "Lawn" / "Widget" / "TitleScreen.cpp").read_text(encoding="utf-8")
        selector = (ROOT / "src" / "Lawn" / "Widget" / "GameSelector.cpp").read_text(encoding="utf-8")
        board = (ROOT / "src" / "Lawn" / "Board.cpp").read_text(encoding="utf-8")
        challenge = (ROOT / "src" / "Lawn" / "Widget" / "ChallengeScreen.cpp").read_text(encoding="utf-8")
        award = (ROOT / "src" / "Lawn" / "Widget" / "AwardScreen.cpp").read_text(encoding="utf-8")
        store = (ROOT / "src" / "Lawn" / "Widget" / "StoreScreen.cpp").read_text(encoding="utf-8")
        almanac = (ROOT / "src" / "Lawn" / "Widget" / "AlmanacDialog.cpp").read_text(encoding="utf-8")

        self.assertIn("DrawImage(IMAGE_TITLESCREEN, -GAME_SCREEN_OFFSET_X, 0)", title)
        self.assertIn("aBackdropG.Translate(-GAME_SCREEN_OFFSET_X, 0)", selector)
        self.assertIn("-BOARD_OFFSET - GAME_SCREEN_OFFSET_X", board)
        self.assertIn("FillRect(-GAME_SCREEN_OFFSET_X, 0, GAME_SCREEN_WIDTH, mHeight)", board)
        self.assertIn("IMAGE_CHALLENGE_BACKGROUND, -GAME_SCREEN_OFFSET_X, 0", challenge)
        self.assertIn("IMAGE_AWARDSCREEN_BACK, -GAME_SCREEN_OFFSET_X, 0", award)
        self.assertIn("IMAGE_STORE_BACKGROUND, -GAME_SCREEN_OFFSET_X, 0", store)
        self.assertIn("IMAGE_ALMANAC_INDEXBACK, -GAME_SCREEN_OFFSET_X, 0", almanac)
        self.assertIn("mLastMouseX - mX", almanac)
        self.assertIn("mLastMouseY - mY", almanac)

    def test_widescreen_extends_aquarium_waves_and_fog_without_changing_gameplay_grid(self):
        board = (ROOT / "src" / "Lawn" / "Board.cpp").read_text(encoding="utf-8")

        self.assertIn("IMAGE_WAVESIDE, -GAME_SCREEN_OFFSET_X, 40", board)
        self.assertIn("IMAGE_WAVECENTER, 640, 40", board)
        self.assertIn("IMAGE_WAVESIDE, BOARD_WIDTH + GAME_SCREEN_OFFSET_X, 40", board)
        self.assertIn("float aPosX = x * 80 + mFogOffset + 145", board)

    def test_credits_backgrounds_and_fades_cover_the_widescreen_canvas(self):
        credits = (ROOT / "src" / "Lawn" / "Widget" / "CreditScreen.cpp").read_text(encoding="utf-8")

        self.assertIn("aWideG.Translate(-GAME_SCREEN_OFFSET_X, 0)", credits)
        self.assertIn("aWideG.DrawImage(IMAGE_BACKGROUND1, 0, 0)", credits)
        self.assertIn("FillRect(-GAME_SCREEN_OFFSET_X, 0, GAME_SCREEN_WIDTH, mHeight)", credits)
        self.assertIn("aTransformBackground2.mTransX - BOARD_WIDTH / 2 - GAME_SCREEN_OFFSET_X", credits)


if __name__ == "__main__":
    unittest.main()
