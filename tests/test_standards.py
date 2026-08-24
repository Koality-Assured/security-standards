"""Unit tests verifying security standards structure."""

import unittest
from pathlib import Path
from tools.validator import validate_standard_file


class TestSecurityStandards(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]
        self.standards_dir = self.root / "standards"

    def test_standards_directory_exists(self):
        self.assertTrue(self.standards_dir.exists())

    def test_standards_have_valid_frontmatter(self):
        standards = [p for p in self.standards_dir.glob("*.md") if p.name != "README.md"]
        for std in standards:
            errs = validate_standard_file(std)
            self.assertEqual(errs, [], f"Standard {std.name} has validation errors: {errs}")


if __name__ == "__main__":
    unittest.main()
