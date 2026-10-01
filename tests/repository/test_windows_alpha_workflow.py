"""Workflow context availability and the actual runner environment handoff."""
import copy
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/windows-alpha.yml"


def check_job_env_contexts(workflow):
    # GitHub's context-availability table for jobs.<job_id>.env. A JSON
    # schema validates shape, but does not enforce this expression scope.
    allowed = {"github", "needs", "strategy", "matrix", "vars", "secrets", "inputs"}
    for job in workflow["jobs"].values():
        for value in job.get("env", {}).values():
            for expression in re.findall(r"\$\{\{(.*?)\}\}", str(value), re.S):
                expression = re.sub(r"'(?:[^']|'')*'", "''", expression)
                roots = set(re.findall(r"(?<![\w.])([A-Za-z_]\w*)\s*(?:\.|\[)", expression))
                if not roots.issubset(allowed):
                    raise ValueError("unavailable job env context: " + ",".join(sorted(roots - allowed)))


class WindowsAlphaWorkflowTests(unittest.TestCase):
    def test_job_environment_does_not_use_runner_context_before_dispatch(self):
        workflow = json.loads(WORKFLOW.read_bytes())
        try:
            check_job_env_contexts(workflow)
        except ValueError as error:
            self.fail(str(error))
        self.assertEqual(workflow["jobs"]["windows-alpha"]["env"]["SOURCE_SHA"], "${{ github.sha }}")
        for expression in ("${{ runner.temp }}", "${{ runner['temp'] }}", "${{ env.ALPHA_ROOT }}", "${{ steps.setup.outputs.root }}"):
            changed = copy.deepcopy(workflow)
            changed["jobs"]["windows-alpha"]["env"]["ALPHA_ROOT"] = expression
            with self.subTest(expression=expression), self.assertRaisesRegex(ValueError, "unavailable job env context"):
                check_job_env_contexts(changed)

    def test_provenance_bootstraps_exact_locked_python_before_verification(self):
        workflow = json.loads(WORKFLOW.read_bytes())
        steps = workflow["jobs"]["provenance"]["steps"]
        setups = [
            (index, step)
            for index, step in enumerate(steps)
            if step.get("uses", "").startswith("actions/setup-python@")
        ]
        self.assertEqual(len(setups), 1, "provenance needs one pinned Python bootstrap")
        setup_index, setup = setups[0]
        self.assertEqual(
            setup,
            {
                "uses": "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97",
                "with": {"python-version": "3.12.10"},
            },
        )
        installs = [
            (index, step)
            for index, step in enumerate(steps)
            if step.get("name") == "Install exact locked verifier dependencies"
        ]
        self.assertEqual(len(installs), 1, "provenance needs one locked dependency install")
        install_index, install = installs[0]
        self.assertEqual(install.get("shell"), "pwsh")
        self.assertEqual(
            install.get("run", "").split(),
            [
                "python", "-m", "pip", "install", "--disable-pip-version-check",
                "--only-binary=:all:", "--require-hashes", "-r",
                "packaging/windows/requirements.lock",
            ],
        )
        verify_index = next(
            index
            for index, step in enumerate(steps)
            if step.get("name") == "Strict machine-readable attestation verification"
        )
        self.assertLess(setup_index, install_index)
        self.assertLess(install_index, verify_index)

    @unittest.skipUnless(os.name == "nt" and shutil.which("pwsh"), "requires Windows PowerShell 7")
    def test_runtime_root_step_exports_exact_path_and_fails_without_runner_inputs(self):
        workflow = json.loads(WORKFLOW.read_bytes())
        steps = workflow["jobs"]["windows-alpha"]["steps"]
        setup = next((step for step in steps if step.get("id") == "alpha-root"), None)
        self.assertIsNotNone(setup, "runner root initialization step missing")
        self.assertLess(steps.index(setup), next(i for i, s in enumerate(steps) if "bootstrap.ps1" in s.get("run", "")))
        with tempfile.TemporaryDirectory(prefix="alpha workflow ") as temporary:
            directory = Path(temporary)
            environment_file = directory / "environment"
            environment_file.write_bytes(b"EXISTING=preserved\n")
            env = dict(os.environ, RUNNER_TEMP=str(directory), GITHUB_ENV=str(environment_file))
            run = lambda values: subprocess.run([shutil.which("pwsh"), "-NoProfile", "-NonInteractive", "-Command", setup["run"]], env=values, capture_output=True)
            result = run(env)
            self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
            self.assertEqual(environment_file.read_bytes(), ("EXISTING=preserved\nALPHA_ROOT=" + str(directory / "tessaveil-alpha") + "\n").encode())
            before = environment_file.read_bytes()
            for changes in ({"RUNNER_TEMP": ""}, {"RUNNER_TEMP": "relative"}, {"RUNNER_TEMP": str(directory) + "\nINJECTED=value"},
                            {"RUNNER_TEMP": str(directory / "absent")}, {"GITHUB_ENV": ""}, {"GITHUB_ENV": "relative"}):
                with self.subTest(changes=changes):
                    self.assertNotEqual(run(dict(env, **changes)).returncode, 0)
                    self.assertEqual(environment_file.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
