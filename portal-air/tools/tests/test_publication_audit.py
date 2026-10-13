from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "publication_audit.py"
SPEC = importlib.util.spec_from_file_location("publication_audit", MODULE_PATH)
assert SPEC and SPEC.loader
publication_audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publication_audit)


class PublicationAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="Portal Air publication audit ")
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def assignment(name: str, value: str) -> str:
        """Build scanner input without embedding a scanner hit in this test file."""
        return f"{name} = {value}\n"

    def test_safe_example_has_no_findings(self) -> None:
        (self.root / "README.md").write_text("Use environment variables; do not commit values.\n", encoding="utf-8")
        self.assertEqual([], publication_audit.audit(self.root))

    def test_secret_value_is_reported_without_returning_value(self) -> None:
        (self.root / "config.py").write_text(
            self.assignment("api" + "_key", repr("fixture" + "-value-12345")),
            encoding="utf-8",
        )
        findings = publication_audit.audit(self.root)
        self.assertEqual(["P1"], [item["severity"] for item in findings])
        self.assertEqual("credential-assignment", findings[0]["rule"])
        self.assertEqual("config.py", findings[0]["path"])

    def test_exact_coordinate_and_private_key_filename_are_findings(self) -> None:
        (self.root / "id_rsa").write_text("placeholder", encoding="utf-8")
        (self.root / "map.py").write_text(
            self.assignment("lati" + "tude", "48." + "48231"),
            encoding="utf-8",
        )
        findings = publication_audit.audit(self.root)
        self.assertEqual({"P0", "P1"}, {str(item["severity"]) for item in findings})

    def test_examples_with_empty_password_are_not_a_secret_finding(self) -> None:
        (self.root / ".env.example").write_text("POSTGRES_" + "PASSWORD=\n", encoding="utf-8")
        self.assertEqual([], publication_audit.audit(self.root))

    def test_real_environment_file_remains_a_finding(self) -> None:
        (self.root / ".env").write_text("POSTGRES_" + "PASSWORD=\n", encoding="utf-8")
        findings = publication_audit.audit(self.root)
        self.assertEqual(["environment-file"], [item["rule"] for item in findings])

    def test_non_empty_template_value_is_still_content_scanned(self) -> None:
        (self.root / ".env.example").write_text(
            "POSTGRES_" + "PASSWORD=" + "not-a-placeholder-value\n",
            encoding="utf-8",
        )
        findings = publication_audit.audit(self.root)
        self.assertEqual(["credential-assignment"], [item["rule"] for item in findings])

    def test_template_allowlist_only_suppresses_documented_path_rule(self) -> None:
        example = self.root / "portal_air_v1" / "config.example.json"
        example.parent.mkdir()
        protected_path = "/" + "var" + "/" + "lib" + "/portal-air-data/example.db"
        example.write_text(
            '{"database_path": "' + protected_path + '"}\n',
            encoding="utf-8",
        )
        self.assertEqual("protected-runtime-path", publication_audit.audit(self.root)[0]["rule"])
        self.assertEqual([], publication_audit.audit(self.root, allow_safe_templates=True))


if __name__ == "__main__":
    unittest.main()
