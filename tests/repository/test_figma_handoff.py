"""Fail-closed contract for the Windows v1 Figma handoff."""

from copy import deepcopy
import json
from pathlib import Path
import re
import unittest
from urllib.parse import parse_qsl, urlsplit


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "reports/windows-v1/figma-handoff.md"
AUTHORIZED_KEY = "VCQcLCScpQja1WVXjWYROq"
AUTHORIZED_NAME = "Tessaveil — Product Design"
AUTHORIZED_PAGE = "0:1"
CANONICAL_FILE_URL = f"https://www.figma.com/design/{AUTHORIZED_KEY}"
EXCLUDED_KEY = "JRmYeYALLwsII1wjFxoFRV"
EXCLUDED_NAME = "Classic Create Concepts"
REQUIRED_COVERAGE = {
    "foundations_and_components",
    "start_create_open_unlock",
    "profile_search_exact_status_unavailable",
    "custom_dictionary_lifecycle",
    "sheet_10_36_protection_verify",
    "spin_and_repeat_warning",
    "backup_restore_original_password",
    "rotation_and_old_copy_warning",
    "dirty_save_discard_cancel",
    "privacy_cover_and_locked",
    "wrong_password_damaged_access_denied_oversize",
    "scaling_and_accessibility",
    "sheet_create_rename_delete",
    "settings_locale_theme_timeout",
    "stable_actionable_controller_errors",
}
EXPECTED_ERROR_KEYS = {
    "invalid-header", "unsupported-version", "kdf-out-of-bounds",
    "unsupported-kdf", "truncated", "too-large", "authentication",
    "invalid-password", "password-policy", "access-denied",
    "insufficient-space", "io", "already-exists", "invalid-path",
    "unsupported-filesystem", "locked", "unsaved-changes",
    "invalid-payload", "temporary-remains",
}
REQUIRED_COMPONENTS = {
    "App/Header", "Tab/Navigation", "Profile/Card", "Sheet/Protection",
    "Error/Card", "Button/Primary", "Button/Secondary", "Button/Danger",
    "Field/Text", "Field/Secret", "Field/Select", "Badge/Status",
    "Note/Security", "Table/Cell", "Dialog/Shell", "Privacy/Cover",
}
EXPECTED_LINK_NODE_IDS = {
    "foundations": "3:59",
    "components": "13:85",
    "screens": {
        "start_create_open_unlock": "5:2",
        "profile_search_exact_status_unavailable": "5:36",
        "custom_dictionary_lifecycle": "5:65",
        "sheet_10_36_protection_verify": "5:103",
        "spin_and_repeat_warning": "5:144",
        "backup_restore_original_password": "6:54",
        "rotation_and_old_copy_warning": "6:79",
        "dirty_save_discard_cancel": "6:90",
        "privacy_cover_and_locked": "6:108",
        "wrong_password_damaged_access_denied_oversize": "6:125",
        "scaling_and_accessibility": "6:153",
        "sheet_create_rename_delete": "14:87",
        "settings_locale_theme_timeout": "14:129",
        "stable_actionable_controller_errors": "15:119",
    },
}
EXPECTED_COMPONENT_NODES = {
    "App/Header": "13:87", "Tab/Navigation": "13:91",
    "Profile/Card": "13:93", "Sheet/Protection": "13:98",
    "Error/Card": "13:102", "Button/Primary": "4:5",
    "Button/Secondary": "4:7", "Button/Danger": "4:9",
    "Field/Text": "4:11", "Field/Secret": "4:14",
    "Field/Select": "4:17", "Badge/Status": "4:20",
    "Note/Security": "4:22", "Table/Cell": "4:25",
    "Dialog/Shell": "4:27", "Privacy/Cover": "4:30",
}
EXPECTED_ERROR_NODES = {
    "invalid-header": "15:126", "unsupported-version": "15:130",
    "kdf-out-of-bounds": "15:134", "unsupported-kdf": "15:138",
    "truncated": "15:150", "too-large": "15:154",
    "authentication": "15:158", "invalid-password": "15:162",
    "password-policy": "15:174", "access-denied": "15:178",
    "insufficient-space": "15:182", "io": "15:186",
    "already-exists": "15:198", "invalid-path": "15:202",
    "unsupported-filesystem": "15:206", "locked": "15:210",
    "unsaved-changes": "15:222", "invalid-payload": "15:226",
    "temporary-remains": "15:230",
}
EXPECTED_STATE_NODES = {
    "sheet_create": "14:105", "sheet_rename": "14:113",
    "sheet_delete": "14:121", "settings_locale": "14:137",
    "settings_theme": "14:145", "settings_timeout": "14:153",
}


def node_id_from_link(link: str) -> str | None:
    if not isinstance(link, str):
        return None
    parsed = urlsplit(link)
    if (parsed.scheme != "https" or parsed.netloc != "www.figma.com" or
            parsed.path != f"/design/{AUTHORIZED_KEY}" or parsed.fragment):
        return None
    query = parse_qsl(parsed.query, keep_blank_values=True)
    if len(query) != 1 or query[0][0] != "node-id":
        return None
    found = re.fullmatch(r"(\d+)-(\d+)", query[0][1])
    return f"{found.group(1)}:{found.group(2)}" if found else None


def extract_contract(text: str) -> dict:
    blocks = re.findall(r"```json\s*\n(.*?)\n```", text, flags=re.DOTALL)
    if len(blocks) != 1:
        raise ValueError("expected exactly one JSON contract block")
    return json.loads(blocks[0])


def validate_contract(contract: dict) -> tuple[str, ...]:
    errors = []
    disposition = contract.get("disposition")
    if disposition not in {"pass", "blocked"}:
        errors.append("disposition must be exactly pass or blocked")

    target = contract.get("authorized_target", {})
    if target.get("file_key") != AUTHORIZED_KEY:
        errors.append("authorized target file key mismatch")
    if target.get("name") != AUTHORIZED_NAME:
        errors.append("authorized target name mismatch")
    if target.get("url") != CANONICAL_FILE_URL:
        errors.append("authorized target URL mismatch")
    if target.get("page_node_id") != AUTHORIZED_PAGE:
        errors.append("authorized page mismatch")
    serialized_target = json.dumps(target, ensure_ascii=False)
    if EXCLUDED_KEY in serialized_target or EXCLUDED_NAME in serialized_target:
        errors.append("unrelated Figma evidence cannot be an authorized target")

    coverage = contract.get("coverage", {})
    if set(coverage) != REQUIRED_COVERAGE:
        errors.append("coverage keys do not match the reviewed Task 6 scope")
    if not coverage or any(value is not True for value in coverage.values()):
        errors.append("every coverage item must be explicitly true")

    node_links = contract.get("node_links", {})
    screen_links = node_links.get("screens", {})
    if set(screen_links) != REQUIRED_COVERAGE - {"foundations_and_components"}:
        errors.append("every screen coverage item must have a node link")
    all_links = [node_links.get("foundations"), node_links.get("components"),
                 *screen_links.values()]
    node_ids = []
    for link in all_links:
        if not isinstance(link, str):
            errors.append("node links must point into the authorized file")
            break
        node_id = node_id_from_link(link)
        if node_id is None or node_id == "999:999":
            errors.append("node links must use reviewed, non-placeholder node IDs")
            break
        node_ids.append(node_id)
    if len(node_ids) != len(set(node_ids)):
        errors.append("coverage node mappings must be unique")
    actual_link_ids = {
        "foundations": node_id_from_link(node_links.get("foundations", "")),
        "components": node_id_from_link(node_links.get("components", "")),
        "screens": {key: node_id_from_link(value) for key, value in screen_links.items()},
    }
    if actual_link_ids != EXPECTED_LINK_NODE_IDS:
        errors.append("node links do not match the exact reviewed live-node inventory")

    component_nodes = contract.get("component_nodes", {})
    if set(component_nodes) != REQUIRED_COMPONENTS:
        errors.append("component node inventory mismatch")
    if len(component_nodes.values()) != len(set(component_nodes.values())):
        errors.append("component node IDs must be unique")
    if any(not re.fullmatch(r"\d+:\d+", value or "") for value in component_nodes.values()):
        errors.append("component node IDs must be concrete Figma IDs")
    if component_nodes != EXPECTED_COMPONENT_NODES:
        errors.append("component nodes do not match reviewed live evidence")

    error_nodes = contract.get("error_nodes", {})
    if set(error_nodes) != EXPECTED_ERROR_KEYS:
        errors.append("all 19 stable controller error keys require exact nodes")
    if len(error_nodes.values()) != len(set(error_nodes.values())):
        errors.append("controller error node IDs must be unique")
    if any(not re.fullmatch(r"\d+:\d+", value or "") for value in error_nodes.values()):
        errors.append("controller error nodes must be concrete Figma IDs")
    if error_nodes != EXPECTED_ERROR_NODES:
        errors.append("controller error nodes do not match reviewed live evidence")

    state_nodes = contract.get("state_nodes", {})
    if state_nodes != EXPECTED_STATE_NODES:
        errors.append("sheet and settings state nodes do not match reviewed evidence")

    audit = contract.get("audit")
    if not isinstance(audit, dict):
        errors.append("audit object is mandatory")
    else:
        if audit.get("screen_count") != 15:
            errors.append("audit requires exactly 15 reviewed 1280x720 boards")
        if audit.get("screen_size") != "1280x720":
            errors.append("audit screen size mismatch")
        if audit.get("component_count") != 16:
            errors.append("audit component count does not match reviewed evidence")
        if audit.get("instance_count") != 108 or audit.get("text_node_count") != 361:
            errors.append("audit editable-node counts do not match reviewed evidence")
        if audit.get("image_fill_count") != 0 or audit.get("all_nodes_within_screen_bounds") is not True:
            errors.append("audit editability or bounds evidence failed")
        if audit.get("stable_error_key_count") != 19:
            errors.append("audit must bind all stable controller error keys")
        usage = audit.get("component_instance_use", {})
        if set(usage) != REQUIRED_COMPONENTS or any(value < 1 for value in usage.values()):
            errors.append("every required component must have a live instance")
        if usage.get("Dialog/Shell", 0) < 3 or usage.get("Error/Card") != 19:
            errors.append("dialog and error component instance evidence mismatch")
        if audit.get("variable_count") != 47 or audit.get("all_scopes_count") != 0:
            errors.append("variable-scope audit does not match reviewed evidence")
        if audit.get("primitive_hidden_count") != 23:
            errors.append("primitive scope audit does not match reviewed evidence")

    excluded = contract.get("excluded_evidence")
    if not isinstance(excluded, list) or len(excluded) != 1:
        errors.append("exactly one excluded unrelated Figma evidence record is required")
    elif (excluded[0].get("file_key"), excluded[0].get("name")) != (EXCLUDED_KEY, EXCLUDED_NAME):
        errors.append("excluded Renderis evidence mismatch")

    fonts = contract.get("font_validation", {})
    if fonts.get("production") != ["Segoe UI", "Consolas"]:
        errors.append("production font contract mismatch")
    if fonts.get("preview") != ["Inter", "Roboto Mono"]:
        errors.append("preview font contract mismatch")

    blocker = contract.get("blocker")
    if disposition == "blocked":
        if not isinstance(blocker, dict):
            errors.append("blocked disposition requires a blocker object")
        else:
            if blocker.get("category") != "exact-production-fonts-unavailable":
                errors.append("blocked disposition requires the exact-font blocker category")
            for field in ("reason", "owner_action", "rerun"):
                if not isinstance(blocker.get(field), str) or not blocker[field].strip():
                    errors.append(f"blocked disposition requires blocker.{field}")
        if fonts.get("status") != "blocked":
            errors.append("blocked disposition requires blocked font status")
    elif disposition == "pass":
        if blocker is not None:
            errors.append("pass disposition cannot carry a blocker")
        if fonts.get("status") != "pass":
            errors.append("pass disposition requires passing exact-font validation")

    impact = contract.get("impact", {})
    if impact.get("code") != "unaffected" or impact.get("release") != "unaffected":
        errors.append("Figma handoff must not be promoted to a code or release defect")
    if impact.get("handoff_gate") != disposition:
        errors.append("handoff gate must match disposition")
    return tuple(errors)


class FigmaHandoffTests(unittest.TestCase):
    def read_contract(self) -> dict:
        self.assertTrue(REPORT.is_file(), "missing reports/windows-v1/figma-handoff.md")
        return extract_contract(REPORT.read_text(encoding="utf-8"))

    def test_committed_handoff_contract_is_valid(self):
        contract = self.read_contract()
        self.assertEqual(validate_contract(contract), ())

    def test_disposition_is_not_ambiguous_or_omitted(self):
        contract = self.read_contract()
        for value in (None, "partial", "pass-or-blocked", "PASS"):
            with self.subTest(value=value):
                candidate = deepcopy(contract)
                if value is None:
                    candidate.pop("disposition", None)
                else:
                    candidate["disposition"] = value
                self.assertTrue(validate_contract(candidate))

    def test_blocked_requires_reason_owner_action_and_rerun(self):
        contract = self.read_contract()
        candidate = deepcopy(contract)
        candidate["disposition"] = "blocked"
        for field in ("reason", "owner_action", "rerun"):
            with self.subTest(field=field):
                broken = deepcopy(candidate)
                broken.setdefault("blocker", {}).pop(field, None)
                self.assertTrue(validate_contract(broken))

    def test_unrelated_file_cannot_be_authorized_target(self):
        contract = self.read_contract()
        for field, value in (("file_key", EXCLUDED_KEY), ("name", EXCLUDED_NAME)):
            with self.subTest(field=field):
                candidate = deepcopy(contract)
                candidate["authorized_target"][field] = value
                self.assertTrue(validate_contract(candidate))

    def test_fake_duplicate_and_placeholder_node_links_fail_closed(self):
        contract = self.read_contract()
        fake = "https://www.figma.com/design/VCQcLCScpQja1WVXjWYROq?node-id=999-999"
        for mutation in ("all_fake", "duplicate"):
            with self.subTest(mutation=mutation):
                candidate = deepcopy(contract)
                if mutation == "all_fake":
                    candidate["node_links"]["foundations"] = fake
                    candidate["node_links"]["components"] = fake
                    candidate["node_links"]["screens"] = {
                        key: fake for key in candidate["node_links"]["screens"]
                    }
                else:
                    first = next(iter(candidate["node_links"]["screens"].values()))
                    candidate["node_links"]["screens"] = {
                        key: first for key in candidate["node_links"]["screens"]
                    }
                self.assertTrue(validate_contract(candidate))

    def test_missing_audit_or_excluded_evidence_fails_closed(self):
        contract = self.read_contract()
        for field in ("audit", "excluded_evidence"):
            with self.subTest(field=field):
                candidate = deepcopy(contract)
                candidate.pop(field, None)
                self.assertTrue(validate_contract(candidate))

    def test_wrong_authorized_page_or_key_fails_closed(self):
        contract = self.read_contract()
        for field, value in (("page_node_id", "9:9"), ("file_key", EXCLUDED_KEY)):
            with self.subTest(field=field):
                candidate = deepcopy(contract)
                candidate["authorized_target"][field] = value
                self.assertTrue(validate_contract(candidate))

    def test_authorized_target_rejects_noncanonical_url_with_retained_key(self):
        contract = self.read_contract()
        attacks = (
            f"https://evil.example/design/{AUTHORIZED_KEY}",
            f"https://figma.com.evil/design/{AUTHORIZED_KEY}",
            f"http://www.figma.com/design/{AUTHORIZED_KEY}",
            f"https://www.figma.com/file/{AUTHORIZED_KEY}",
            f"https://user@www.figma.com/design/{AUTHORIZED_KEY}",
            f"https://www.figma.com/design/{AUTHORIZED_KEY}#other",
        )
        for url in attacks:
            with self.subTest(url=url):
                candidate = deepcopy(contract)
                candidate["authorized_target"]["url"] = url
                self.assertTrue(validate_contract(candidate))

    def test_node_links_reject_foreign_or_malformed_urls_with_valid_ids(self):
        contract = self.read_contract()
        original = contract["node_links"]["foundations"]
        node_query = original.split("?", 1)[1]
        attacks = (
            f"https://evil.example/design/{AUTHORIZED_KEY}?{node_query}",
            f"https://figma.com.evil/design/{AUTHORIZED_KEY}?{node_query}",
            f"http://www.figma.com/design/{AUTHORIZED_KEY}?{node_query}",
            f"https://www.figma.com/file/{AUTHORIZED_KEY}?{node_query}",
            f"https://user@www.figma.com/design/{AUTHORIZED_KEY}?{node_query}",
            f"https://www.figma.com/design/{AUTHORIZED_KEY}?{node_query}#other",
        )
        for url in attacks:
            with self.subTest(url=url):
                candidate = deepcopy(contract)
                candidate["node_links"]["foundations"] = url
                self.assertTrue(validate_contract(candidate))

    def test_blocked_may_retain_authorized_file_and_completed_coverage(self):
        contract = self.read_contract()
        self.assertEqual(contract["disposition"], "blocked")
        self.assertEqual(contract["authorized_target"]["file_key"], AUTHORIZED_KEY)
        self.assertTrue(all(contract["coverage"].values()))


if __name__ == "__main__":
    unittest.main()
