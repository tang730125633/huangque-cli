import re
import unittest
from pathlib import Path

from hq_cli import __version__


ROOT = Path(__file__).resolve().parents[1]


class InstallerTests(unittest.TestCase):
    def test_installers_pin_the_release_artifact(self):
        shell = (ROOT / "install.sh").read_text(encoding="utf-8")
        powershell = (ROOT / "install.ps1").read_text(encoding="utf-8")
        self.assertIn('version="%s"' % __version__, shell)
        self.assertIn('$Version = "%s"' % __version__, powershell)
        hashes = [
            re.search(r'wheel_sha256="([0-9a-f]{64})"', shell).group(1),
            re.search(r'\$WheelSha256 = "([0-9a-f]{64})"', powershell).group(1),
        ]
        sizes = [
            int(re.search(r'wheel_size="([0-9]+)"', shell).group(1)),
            int(re.search(r'\$WheelSize = ([0-9]+)', powershell).group(1)),
        ]
        self.assertEqual(hashes[0], hashes[1])
        self.assertEqual(sizes[0], sizes[1])
        self.assertGreater(sizes[0], 0)


if __name__ == "__main__":
    unittest.main()
