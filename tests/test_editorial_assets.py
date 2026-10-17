"""Guard against decorative assets causing layout shifts or unbounded downloads."""

import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from scripts import check_build


class EditorialAssetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.site = Path(self.temporary.name)
        for name in ("structure", "signal"):
            for width in (480, 960, 1440):
                path = self.site / f"assets/editorial/{name}-{width}.webp"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"small fixture")
        for name in ("manrope-latin", "newsreader-latin", "newsreader-italic-latin"):
            path = self.site / f"assets/fonts/{name}.woff2"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"small fixture")
        self.home = "".join(
            '<img src="/assets/editorial/{name}-960.webp" width="1440" height="960" alt="Editorial artwork" '
            'srcset="/assets/editorial/{name}-480.webp 480w, /assets/editorial/{name}-960.webp 960w, /assets/editorial/{name}-1440.webp 1440w" {loading}>'.format(
                name=name, loading='fetchpriority="high"' if name == "structure" else 'loading="lazy"'
            )
            for name in ("structure", "signal")
        )

    def audit(self, home: str) -> None:
        with patch.object(check_build, "SITE", self.site):
            check_build.audit_editorial_assets(home)

    def test_responsive_assets_within_budget_pass(self) -> None:
        self.audit(self.home)

    def test_missing_intrinsic_dimensions_are_rejected(self) -> None:
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            self.audit(self.home.replace('width="1440"', ""))

    def test_missing_responsive_variant_is_rejected(self) -> None:
        (self.site / "assets/editorial/structure-480.webp").unlink()
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            self.audit(self.home)

    def test_oversized_font_is_rejected(self) -> None:
        (self.site / "assets/fonts/manrope-latin.woff2").write_bytes(b"x" * 100_001)
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            self.audit(self.home)

    def test_lazy_hero_is_rejected(self) -> None:
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            self.audit(self.home.replace('fetchpriority="high"', 'loading="lazy"'))


if __name__ == "__main__":
    unittest.main()
