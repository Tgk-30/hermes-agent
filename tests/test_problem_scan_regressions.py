from __future__ import annotations

import json
import re
import subprocess
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_hindsight_provider_import_is_not_duplicated():
    source = (REPO_ROOT / "plugins" / "memory" / "hindsight" / "__init__.py").read_text()
    assert source.count("from hermes_constants import get_hermes_home") == 1


def test_godmode_fast_prompt_typo_is_fixed_in_doc_and_script():
    doc_source = (
        REPO_ROOT
        / "skills"
        / "red-teaming"
        / "godmode"
        / "references"
        / "jailbreak-templates.md"
    ).read_text()
    script_source = (
        REPO_ROOT
        / "skills"
        / "red-teaming"
        / "godmode"
        / "scripts"
        / "godmode_race.py"
    ).read_text()

    assert "geniuis" not in doc_source.lower()
    assert "geniuis" not in script_source.lower()
    assert "rebel genius" in doc_source
    assert "rebel genius" in script_source


def test_website_sidebar_doc_ids_resolve_to_real_docs():
    sidebars_source = (REPO_ROOT / "website" / "sidebars.ts").read_text()
    refs = {
        ref
        for ref in re.findall(r"['\"]([^'\"]+/[^'\"]*)['\"]", sidebars_source)
        if not ref.startswith("@")
    }
    doc_ids = {
        str(path.relative_to(REPO_ROOT / "website" / "docs").with_suffix("")).replace("\\", "/")
        for path in (REPO_ROOT / "website" / "docs").rglob("*.md")
    }

    missing = sorted(refs - doc_ids)
    assert missing == []


def _run_utils_probe() -> dict[str, str]:
    script = textwrap.dedent(
        """
        import fs from 'node:fs';
        import path from 'node:path';
        import ts from './web/node_modules/typescript/lib/typescript.js';

        const repoRoot = process.argv[1];
        const utilsPath = path.join(repoRoot, 'web', 'src', 'lib', 'utils.ts');
        let source = fs.readFileSync(utilsPath, 'utf8');
        source = source.replace(/^import .*$/gm, '');
        const prefix = `const clsx = (...inputs) => inputs; const twMerge = (value) => value;\n`;
        source = prefix + source;

        const transpiled = ts.transpileModule(source, {
          compilerOptions: {
            module: ts.ModuleKind.ES2020,
            target: ts.ScriptTarget.ES2020,
          },
        }).outputText;

        Date.now = () => 1_700_000_000_000;
        const moduleUrl = 'data:text/javascript;base64,' + Buffer.from(transpiled).toString('base64');
        const mod = await import(moduleUrl);
        console.log(JSON.stringify({
          futureUnix: mod.timeAgo(1_700_000_600),
          futureIso: mod.isoTimeAgo(new Date((1_700_000_000 + 600) * 1000).toISOString()),
          pastUnix: mod.timeAgo(1_699_999_400),
        }));
        """
    )
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script, str(REPO_ROOT)],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_time_helpers_label_future_timestamps_consistently():
    probe = _run_utils_probe()
    assert probe["futureUnix"] == "in 10m"
    assert probe["futureIso"] == "in 10m"
    assert probe["pastUnix"] == "10m ago"


def test_status_and_sessions_pages_do_not_silently_swallow_api_errors():
    status_source = (REPO_ROOT / "web" / "src" / "pages" / "StatusPage.tsx").read_text()
    sessions_source = (REPO_ROOT / "web" / "src" / "pages" / "SessionsPage.tsx").read_text()

    assert ".catch(() => {})" not in status_source
    assert ".catch(() => {})" not in sessions_source
    assert "catch {\n      // ignore" not in sessions_source
