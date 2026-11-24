import os, subprocess, sys, unittest


def importPyzwoasi(libraryPath):
    """Import pyzwoasi in a fresh interpreter with PYZWOASI_LIBRARY set; return the result."""
    env = dict(os.environ, PYZWOASI_LIBRARY=libraryPath)
    code = "import pyzwoasi.pyzwoasi as p; print(p.dllPath)"
    return subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)


class TestLibraryOverride(unittest.TestCase):
        def test_overrideLoadsTheGivenLibrary(self):
            # Use the bundled library itself as the "other" copy, so the test needs no SDK download
            default = subprocess.run([sys.executable, "-c", "import pyzwoasi.pyzwoasi as p; print(p.dllPath)"],
                                     env={k: v for k, v in os.environ.items() if k != "PYZWOASI_LIBRARY"},
                                     capture_output=True, text=True)
            self.assertEqual(default.returncode, 0, default.stderr)
            bundled = default.stdout.strip()
            result = importPyzwoasi(bundled)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), bundled)

        def test_missingOverrideFileRaises(self):
            result = importPyzwoasi(os.path.join(os.sep, "no", "such", "libASICamera2.so"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FileNotFoundError", result.stderr)
            self.assertIn("PYZWOASI_LIBRARY", result.stderr)


if __name__ == "__main__":
    unittest.main()
