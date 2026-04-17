# Hermes Repo Problems Scan

Initial scan generated: 2026-04-15T11:20:08.240303+00:00
Root: `/Users/openclaw/.hermes/hermes-agent`

This document is shared by 25 parallel MiniMax analysis agents.
Each agent owns exactly one section and updates it through a locked helper script.

Current status note, 2026-04-17: the agent-sharded sections below are a
historical scan artifact and several still contain `PENDING` or `RUNNING`
markers from the original pass. Treat the remediation and verification addenda
near the end of this file as the current status for the fixes and tests run in
this worktree. Older findings may be marked resolved in place when a later
verification pass confirms the current tree no longer has the reported defect.

## Legend
- Status: PENDING / RUNNING / DONE / ERROR
- Severity: CRITICAL / HIGH / MEDIUM / LOW

## Agent 01
- Section ID: `agent-01`
- Assigned files: **65**
- Approx bytes: **1050658**
- File range: `.dockerignore` → `agent/prompt_builder.py`
- Top-level scope: `.dockerignore, .env.example, .envrc, .gitattributes, .github, .gitignore, .gitmodules, .mailmap, .plans, AGENTS.md, CONTRIBUTING.md, Dockerfile, LICENSE, MANIFEST.in, README.md, RELEASE_v0.2.0.md, RELEASE_v0.3.0.md, RELEASE_v0.4.0.md, RELEASE_v0.5.0.md, RELEASE_v0.6.0.md, RELEASE_v0.7.0.md, RELEASE_v0.8.0.md, RELEASE_v0.9.0.md, acp_adapter, acp_registry, agent`
<!-- agent-01:start -->
Status: PENDING

_No findings yet._
<!-- agent-01:end -->

## Agent 02
- Section ID: `agent-02`
- Assigned files: **54**
- Approx bytes: **1050625**
- File range: `agent/prompt_caching.py` → `environments/hermes_base_env.py`
- Top-level scope: `agent, assets, batch_runner.py, cli-config.yaml.example, cli.py, constraints-termux.txt, cron, datagen-config-examples, docker, docs, environments`
<!-- agent-02:start -->
Status: PENDING

_No findings yet._
<!-- agent-02:end -->

## Agent 03
- Section ID: `agent-03`
- Assigned files: **49**
- Approx bytes: **1064912**
- File range: `environments/hermes_swe_env/__init__.py` → `gateway/platforms/slack.py`
- Top-level scope: `environments, flake.lock, flake.nix, gateway`
<!-- agent-03:start -->
Status: RUNNING

### Agent 03

# Agent 03 Findings

Status: RUNNING

Scope: environments/hermes_swe_env, environments/terminal_test_env, environments/tool_call_parsers, environments/*.py, flake.*, gateway/platforms/*.py

Analysis in progress...
<!-- agent-03:end -->

## Agent 04
- Section ID: `agent-04`
- Assigned files: **20**
- Approx bytes: **1030040**
- File range: `gateway/platforms/sms.py` → `hermes_cli/auth.py`
- Top-level scope: `gateway, hermes, hermes-already-has-routines.md, hermes_cli`
<!-- agent-04:start -->
Status: RUNNING

### Agent 04

# Agent 04 Findings

Status: RUNNING

Scope: gateway/platforms/*.py, gateway/{restart,run,session,session_context,status,sticker_cache,stream_consumer}.py, hermes_cli/{__init__,auth}.py, hermes-already-has-routines.md
<!-- agent-04:end -->

## Agent 05
- Section ID: `agent-05`
- Assigned files: **33**
- Approx bytes: **1074758**
- File range: `hermes_cli/auth_commands.py` → `hermes_cli/plugins_cmd.py`
- Top-level scope: `hermes_cli`
<!-- agent-05:start -->
Status: PENDING

_No findings yet._
<!-- agent-05:end -->

## Agent 06
- Section ID: `agent-06`
- Assigned files: **16**
- Approx bytes: **1005470**
- File range: `hermes_cli/profiles.py` → `hermes_cli/web_dist/fonts/Collapse-Regular.woff2`
- Top-level scope: `hermes_cli`
<!-- agent-06:start -->
Status: RUNNING

### Agent 06

# Agent 06 Findings

Status: RUNNING
<!-- agent-06:end -->

## Agent 07
- Section ID: `agent-07`
- Assigned files: **168**
- Approx bytes: **1991420**
- File range: `hermes_cli/web_dist/fonts/CourierPrime-Bold.woff2` → `optional-skills/security/oss-forensics/references/recovery-techniques.md`
- Top-level scope: `hermes_cli, hermes_constants.py, hermes_logging.py, hermes_state.py, hermes_time.py, landingpage, mcp_serve.py, mini_swe_runner.py, model_tools.py, nix, optional-skills`
<!-- agent-07:start -->
Status: RUNNING

### Agent 07

# Agent 07 Findings

**Status:** RUNNING

**Scope:** 168 files covering hermes_cli (web_dist, web_server.py, webhook.py), hermes_constants.py, hermes_logging.py, hermes_state.py, hermes_time.py, landingpage/, mcp_serve.py, mini_swe_runner.py, model_tools.py, nix/, and optional-skills/

**Audit started:** 2026-04-15
<!-- agent-07:end -->

## Agent 08
- Section ID: `agent-08`
- Assigned files: **48**
- Approx bytes: **1274751**
- File range: `optional-skills/security/oss-forensics/scripts/evidence-store.py` → `run_agent.py`
- Top-level scope: `optional-skills, package-lock.json, package.json, packaging, plans, plugins, pyproject.toml, requirements.txt, rl_cli.py, run_agent.py`
<!-- agent-08:start -->
Status: DONE

### Agent 08

# Agent 08 Audit Findings

## Scope
Audited 48 files across: plugins/, optional-skills/, packaging/, plans/, rl_cli.py, run_agent.py, and top-level package files.

---

## Findings

### Finding 1: RESOLVED - Forward Reference Bug in rl_cli.py
- **Severity:** CRITICAL when found; resolved in current worktree
- **Path:** rl_cli.py
- **Line(s):** 32 (call) vs 63 (import)
- **Current status:** Resolved. A 2026-04-17 verification pass confirmed
  `get_hermes_home` is now imported before `_hermes_home = get_hermes_home()`.
- **Evidence:**
  ```python
  # Line 32 — get_hermes_home() called BEFORE it is imported
  _hermes_home = get_hermes_home()
  ...
  # Line 63 — actual import statement
  from hermes_constants import get_hermes_home, OPENROUTER_BASE_URL
  ```
- **Why it matters:** Module load causes `NameError: name 'get_hermes_home' is not defined`. This breaks `python rl_cli.py` entirely.
- **Suggested fix:** Move the import statement to the top of the file (before line 32), or use a lazy import pattern.

---

### Finding 2: RESOLVED - Duplicate Import in hindsight plugin
- **Severity:** LOW when found; resolved in current worktree
- **Path:** plugins/memory/hindsight/__init__.py
- **Line(s):** 27 and 31
- **Current status:** Resolved. A 2026-04-17 verification pass confirmed the
  duplicate `get_hermes_home` import has been removed.
- **Evidence:**
  ```python
  # Line 27
  from hermes_constants import get_hermes_home
  # ...
  # Line 31
  from hermes_constants import get_hermes_home
  ```
- **Why it matters:** Duplicate import is harmless in Python (re-imports are no-ops), but indicates copy-paste error during development. May confuse linters.
- **Suggested fix:** Remove the duplicate on line 31.

---

### Finding 3: INFO - requirements.txt Drift vs pyproject.toml
- **Severity:** INFO
- **Path:** requirements.txt
- **Line(s):** All
- **Evidence:** requirements.txt lists a different/pinned set of dependencies than pyproject.toml. Comments at top state "canonical dependency list is in pyproject.toml."
- **Why it matters:** Developers using `pip install -r requirements.txt` may get different versions than `pip install -e ".[all]"`. The file is explicitly marked as non-canonical.
- **Suggested fix:** Keep as-is (file is documented as convenience-only), or remove entirely.

---

## Files Reviewed (No Issues Found)
- `plugins/__init__.py` — placeholder comment, fine
- `optional-skills/security/oss-forensics/scripts/evidence-store.py` — well-structured forensic evidence store
- `plugins/context_engine/__init__.py` — plugin discovery, correct
- `plugins/memory/__init__.py` — memory plugin discovery, correct
- `plugins/memory/byterover/__init__.py` — ByteRover provider, correct
- `plugins/memory/holographic/__init__.py` — holographic memory, correct
- `plugins/memory/honcho/__init__.py` — Honcho memory, correct
- `plugins/memory/localhybrid/__init__.py` — SQLite+ FTS5 hybrid, correct
- `plugins/memory/mem0/__init__.py` — Mem0 provider, correct
- `plugins/memory/openviking/__init__.py` — OpenViking provider, correct
- `plugins/memory/retaindb/__init__.py` — RetainDB provider, correct
- `plugins/memory/supermemory/__init__.py` — Supermemory provider, correct
- `pyproject.toml` — well-structured, no issues
- `run_agent.py` (partial, lines 1-500 reviewed) — appears structurally correct

---

## Summary
- **3 findings originally** (1 critical, 1 low, 1 informational)
- The critical `rl_cli.py` bug and duplicate hindsight import are resolved in
  the current worktree.
- The remaining Agent 08 item is informational dependency-file drift.
- All other files in shard appeared correct at the time of the historical scan.
<!-- agent-08:end -->

## Agent 09
- Section ID: `agent-09`
- Assigned files: **50**
- Approx bytes: **800070**
- File range: `scripts/build_skills_index.py` → `skills/creative/manim-video/references/animation-design-thinking.md`
- Top-level scope: `scripts, setup-hermes.sh, skills`
<!-- agent-09:start -->
Status: RUNNING

### Agent 09

# Agent 09 Findings

Status: RUNNING

## Scope
- Scripts: build_skills_index.py, contributor_audit.py, discord-voice-doctor.py, hermes-gateway, install scripts (cmd/ps1/sh), kill_modal.sh, release.py, sample_and_compress.py, whatsapp-bridge/
- Skills: apple/, autonomous-ai-agents/, creative/ (architecture-diagram, ascii-art, ascii-video, creative-ideation, excalidraw, manim-video)
- setup-hermes.sh

## Audit in progress...
<!-- agent-09:end -->

## Agent 10
- Section ID: `agent-10`
- Assigned files: **189**
- Approx bytes: **2064793**
- File range: `skills/creative/manim-video/references/animations.md` → `skills/mlops/models/segment-anything/references/troubleshooting.md`
- Top-level scope: `skills`
<!-- agent-10:start -->
Status: PENDING

_No findings yet._
<!-- agent-10:end -->

## Agent 11
- Section ID: `agent-11`
- Assigned files: **16**
- Approx bytes: **429853**
- File range: `skills/mlops/models/stable-diffusion/SKILL.md` → `skills/mlops/training/axolotl/references/other.md`
- Top-level scope: `skills`
<!-- agent-11:start -->
Status: PENDING

_No findings yet._
<!-- agent-11:end -->

## Agent 12
- Section ID: `agent-12`
- Assigned files: **17**
- Approx bytes: **1662971**
- File range: `skills/mlops/training/grpo-rl-training/README.md` → `skills/mlops/training/unsloth/references/llms-full.md`
- Top-level scope: `skills`
<!-- agent-12:start -->
Status: PENDING

_No findings yet._
<!-- agent-12:end -->

## Agent 13
- Section ID: `agent-13`
- Assigned files: **73**
- Approx bytes: **2027026**
- File range: `skills/mlops/training/unsloth/references/llms-txt.md` → `skills/red-teaming/godmode/scripts/auto_jailbreak.py`
- Top-level scope: `skills`
<!-- agent-13:start -->
Status: DONE

### Agent 13

# Agent 13 Findings — Productivty & Red-Teaming Skills

## Scope
Audited skills in:
- `skills/productivity/` (google-workspace, linear, nano-pdf, notion, ocr-and-documents, powerpoint)
- `skills/red-teaming/godmode/`

## Findings

### Finding 1: Typo in GODMODE jailbreak template
- **Severity:** LOW
- **Path:** `skills/red-teaming/godmode/references/jailbreak-templates.md`
- **Line(s):** 85
- **Evidence:** `personality: chaotic inverted, tone: rebel geniuis` — "geniuis" is misspelled, should be "genius"
- **Why it matters:** Typos in reference docs reduce credibility. Template text is copied verbatim into model prompts.
- **Suggested fix:** Change `rebel geniuis` to `rebel genius`

---

### Finding 2: Bracket inconsistency in GODMODE FAST template
- **Severity:** LOW
- **Path:** `skills/red-teaming/godmode/references/jailbreak-templates.md`
- **Line(s):** 85 (user message), 88 (user message)
- **Evidence:** Template line 88 shows `variable Z = [{QUERY}]` with square brackets around `{QUERY}`, while all other templates use `Z={QUERY}` without brackets (e.g., lines 41, 56, 74)
- **Why it matters:** If the query substitution logic strips or mishandles the brackets, the resulting prompt would be malformed. The bracket wrapping appears inconsistent with the rest of the template set.
- **Suggested fix:** Verify whether `[{QUERY}]` is intentional for this model+template combo. If not, change to `{QUERY}` to match other templates.

---

### Finding 3: Inconsistent or missing frontmatter across skills
- **Severity:** LOW
- **Path:** `skills/productivity/linear/SKILL.md`, `skills/productivity/nano-pdf/SKILL.md`, `skills/productivity/notion/SKILL.md`, `skills/productivity/ocr-and-documents/SKILL.md`
- **Evidence:** Some SKILL.md files have `homepage`, `related_skills`, or `prerequisites` metadata fields; others omit them entirely. The `ocr-and-documents/SKILL.md` (line 10) has `related_skills: [powerpoint]` but most others have no such field. `linear/SKILL.md` (line 12) has no `homepage` while `nano-pdf/SKILL.md` (line 10) does.
- **Why it matters:** Inconsistent metadata makes it harder to discover related skills or verify provenance.
- **Suggested fix:** Standardize frontmatter fields across all productivity skills — at minimum include `name`, `description`, `version`, `author`, `license`, and optionally `homepage`, `related_skills`.

---

### Finding 4: Bare minimum DESCRIPTIONS in productivity skills
- **Severity:** INFORMATIONAL
- **Path:** `skills/productivity/DESCRIPTION.md`, `skills/productivity/ocr-and-documents/DESCRIPTION.md`
- **Evidence:** Both files are only 3 lines — one-line descriptions with no additional context, metadata, or usage guidance. Other skills in the same directory have richer DESCRIPTIONS.
- **Why it matters:** These serve as the skill descriptions for the Hermes skill registry. Minimal descriptions provide little value to users browsing available skills.
- **Suggested fix:** Expand these to 3-5 sentences describing key capabilities and when to use the skill.

---

## No Material Issues Found
- Skills that appear functional (google-workspace, powerpoint, notion) are well-documented
- godmode red-teaming skill references are present and match their described sources
- No broken paths, dead links, or TODO/FIXME markers found
- No config drift or mismatched defaults detected

---

**Summary:** 4 minor findings (3 LOW, 1 INFORMATIONAL). No blocking issues. The typo and bracket inconsistency are cosmetic/low-risk. The minimal DESCRIPTIONS are a documentation gap rather than a functional defect.
<!-- agent-13:end -->

## Agent 14
- Section ID: `agent-14`
- Assigned files: **51**
- Approx bytes: **1092520**
- File range: `skills/red-teaming/godmode/scripts/godmode_race.py` → `skills/research/research-paper-writing/templates/iclr2026/iclr2026_conference.pdf`
- Top-level scope: `skills`
<!-- agent-14:start -->
Status: PENDING

_No findings yet._
<!-- agent-14:end -->

## Agent 15
- Section ID: `agent-15`
- Assigned files: **59**
- Approx bytes: **993311**
- File range: `skills/research/research-paper-writing/templates/iclr2026/iclr2026_conference.sty` → `tests/agent/test_minimax_provider.py`
- Top-level scope: `skills, tests`
<!-- agent-15:start -->
Status: PENDING

_No findings yet._
<!-- agent-15:end -->

## Agent 16
- Section ID: `agent-16`
- Assigned files: **104**
- Approx bytes: **1035708**
- File range: `tests/agent/test_model_metadata.py` → `tests/gateway/test_discord_send.py`
- Top-level scope: `tests`
<!-- agent-16:start -->
Status: DONE

### Agent 16

# Agent 16 Findings

## Scope
104 test files from `tests/agent/test_model_metadata.py` through `tests/gateway/test_discord_send.py` (agent shard offset 501+).

## Summary
Audit of test files for bugs, stale docs, mismatched defaults/tests/docs, broken paths, dead references, config drift, suspicious TODO/FIXME/HACK, missing validation, concurrency/state issues, and other wrong things.

## Findings

**No material issues found.**

The test suite in this shard is well-maintained:

- **Isolation**: `tests/conftest.py` provides an `autouse` `_isolate_hermes_home` fixture that redirects HERMES_HOME to a temp dir, resets the plugin singleton, and clears all platform env vars (`HERMES_SESSION_*`, `OPENROUTER_API_KEY`, etc.) so no test writes to `~/.hermes/` or makes real external API calls. Gateway tests get additional `autouse` `_isolate_discord_routing_env` that clears Discord routing env vars per-module.

- **No stale TODO/FIXME/HACK**: 0 matches in both `tests/agent/` and `tests/gateway/` for `# (TODO|FIXME|HACK|XXX)` comments.

- **No skipped-with-issue-number tests**: 0 matches for `pytest.mark.skip.*reason.*\[` patterns — no forgotten skip markers referencing old issue numbers.

- **Skipped tests are appropriately minimal**: 7 `pytest.mark.skip` matches, all in `tests/gateway/test_voice_command.py` (lines 2113-2116), skipped with `reason="PyNaCl not installed"` via `importlib.util.find_spec("nacl") is None`. This is a legitimate optional-dependency guard.

- **No hardcoded secrets**: No matches for `REAL_API_KEY`, `.real_auth`, or `.real_` patterns that might leak credentials.

- **Mocked subprocess calls are properly guarded**: `test_context_references.py` calls real `git` via `subprocess.run` but only on `tmp_path` repositories created within the test fixture — no side effects on real repos. `test_anthropic_adapter.py` mocks `subprocess.run` entirely.

- **`time.sleep` patterns are intentional**: The 210 `time.sleep` matches (mostly 0.01s–0.05s polling loops in approval/concurrency tests) are used to wait for async state transitions and are not bugs.

- **`datetime.now()` in cron tests is appropriate**: The 212 `datetime.now()` matches are in `tests/cron/test_jobs.py` where they test scheduling logic that depends on real time progression — these cannot be mocked without significant restructuring.

- **Async test patterns are consistent**: 219 `async def test_` functions in gateway tests use `@pytest.mark.asyncio` decorator and are paired with the `_ensure_current_event_loop` autouse fixture from `tests/conftest.py` that provides a default event loop for sync tests calling `get_event_loop()`.

- **Good error-path coverage**: `test_subdirectory_hints.py` tests permission errors with `patch.object(Path, "is_file", ...)` and `patch.object(Path, "is_dir", ...)` — correctly verifying graceful degradation rather than crashes.

- **No broken file paths**: File write operations (`write_text`, `write_bytes`, `open(...).write`) consistently use `tmp_path` fixtures, never hardcoded paths.

- **Well-documented regression tests**: `test_transcript_offset.py` has an extensive docstring explaining the `history_offset` bug (off-by-one per turn from turn 2 onwards), the root cause (`len(history)` vs filtered length), and the fix. `test_media_download_retry.py` documents its PR reference (#2982).

- **No mismatched defaults/tests/docs**: Tests and implementation consistently use the same config structures, fixture values, and expected behaviors.

- **No dead references or broken imports**: All imports use proper `sys.modules` guards for optional dependencies.
<!-- agent-16:end -->

## Agent 17
- Section ID: `agent-17`
- Assigned files: **65**
- Approx bytes: **1035469**
- File range: `tests/gateway/test_discord_slash_commands.py` → `tests/gateway/test_sms.py`
- Top-level scope: `tests`
<!-- agent-17:start -->
Status: RUNNING

### Agent 17

# Agent 17 Findings

**Status: RUNNING**

**Scope:** 65 test files in `tests/gateway/`, covering gateway platform tests (Discord, Email, Feishu, Matrix, Mattermost, SMS, Slack, etc.)

**Audit started:** 2026-04-15
<!-- agent-17:end -->

## Agent 18
- Section ID: `agent-18`
- Assigned files: **171**
- Approx bytes: **2071111**
- File range: `tests/gateway/test_sse_agent_cancel.py` → `tests/run_agent/test_agent_loop.py`
- Top-level scope: `tests`
<!-- agent-18:start -->
Status: PENDING

_No findings yet._
<!-- agent-18:end -->

## Agent 19
- Section ID: `agent-19`
- Assigned files: **161**
- Approx bytes: **2059170**
- File range: `tests/run_agent/test_agent_loop_tool_calling.py` → `tests/tools/test_skills_hub.py`
- Top-level scope: `tests`
<!-- agent-19:start -->
Status: PENDING

_No findings yet._
<!-- agent-19:end -->

## Agent 20
- Section ID: `agent-20`
- Assigned files: **70**
- Approx bytes: **1082167**
- File range: `tests/tools/test_skills_hub_clawhub.py` → `tools/file_operations.py`
- Top-level scope: `tests, tools`
<!-- agent-20:start -->
Status: RUNNING

### Agent 20

# Agent 20 Findings

Status: RUNNING
<!-- agent-20:end -->

## Agent 21
- Section ID: `agent-21`
- Assigned files: **20**
- Approx bytes: **993142**
- File range: `tools/file_tools.py` → `tools/rl_training_tool.py`
- Top-level scope: `tools`
<!-- agent-21:start -->
Status: PENDING

_No findings yet._
<!-- agent-21:end -->

## Agent 22
- Section ID: `agent-22`
- Assigned files: **32**
- Approx bytes: **2061288**
- File range: `tools/send_message_tool.py` → `web/public/fonts/Collapse-Regular.woff2`
- Top-level scope: `tools, toolset_distributions.py, toolsets.py, trajectory_compressor.py, utils.py, uv.lock, web`
<!-- agent-22:start -->
Status: PENDING

_No findings yet._
<!-- agent-22:end -->

## Agent 23
- Section ID: `agent-23`
- Assigned files: **124**
- Approx bytes: **1300490**
- File range: `web/public/fonts/CourierPrime-Bold.woff2` → `website/docs/user-guide/features/delegation.md`
- Top-level scope: `web, website`
<!-- agent-23:start -->
Status: DONE

### Agent 23

# Agent 23 Findings

## Scope Summary
Audited the agent-23 shard: the **web/** frontend (React/TypeScript dashboard) and **website/** Docusaurus documentation. The shard contains 113 markdown docs and 28 React/TypeScript source files. No backend Hermes agent code is in this shard.

---

## Findings

### Finding 1: ~30 sidebar references point to non-existent doc files

- **Severity**: HIGH
- **Path**: `website/sidebars.ts`
- **Lines**: sidebars.ts references docs that don't exist; confirmed via filesystem search
- **Evidence**: `sidebars.ts` lists many doc paths that return zero results from `search_files(target='files')`. Examples:
  - `user-guide/profiles` (listed in sidebar) vs `user-guide/profiles.md` (actual file has `.md` extension — but more critically, some don't exist at all)
  - `user-guide/features/overview` — listed in sidebar Core > Features, but no file at that path (only `user-guide/features/overview.md` would be the correct ref)
  - `getting-started/nix-setup`, `getting-started/updating`, `getting-started/learning-path` — all listed in sidebar but `search_files` returns 0 results for these exact paths
  - `guides/tips`, `guides/local-llm-on-mac`, `guides/daily-briefing-bot`, `guides/team-telegram-assistant`, `guides/python-library`, `guides/use-mcp-with-hermes` — all listed in sidebar but `search_files` returns 0 results
  - `developer-guide/contributing`, `developer-guide/prompt-assembly`, `developer-guide/session-storage`, `developer-guide/provider-runtime`, `developer-guide/adding-tools`, `developer-guide/adding-providers`, `developer-guide/adding-platform-adapters` — sidebar lists them but filesystem has zero matches
  - `user-guide/features/tools`, `user-guide/features/context-files`, `user-guide/features/context-references`, `user-guide/features/personality`, `user-guide/features/delegation`, `user-guide/features/code-execution` — sidebar references vs filesystem zero matches
- **Why it matters**: Docusaurus sidebar navigation will have broken/missing links for these sections. Users following sidebar links will hit 404 pages.
- **Suggested fix**: Remove orphaned references from `sidebars.ts`, or create the missing `.md` files. The Docusaurus build likely warns about these missing references.

---

### Finding 2: `timeAgo` produces incorrect output for future timestamps

- **Severity**: LOW
- **Path**: `web/src/lib/utils.ts`
- **Lines**: 9-16
- **Evidence**:
  ```typescript
  export function timeAgo(ts: number): string {
    const delta = Date.now() / 1000 - ts;
    if (delta < 60) return "just now";
    if (delta < 3600) return `${Math.floor(delta / 60)}m ago`;
    if (delta < 86400) return `${Math.floor(delta / 3600)}h ago`;
    if (delta < 172800) return "yesterday";
    return `${Math.floor(delta / 86400)}d ago`;
  }
  ```
  If `ts` is a future timestamp (e.g., `next_run_at` from a cron job in the future), `delta` becomes negative, and all the comparisons fail silently — the function falls through to the last return and produces a negative day count like `"-2d ago"`. The `isoTimeAgo` function has the same issue, though it does guard against `Number.isNaN(delta)` but not against negative deltas.
- **Why it matters**: Cron page displays future run times (next run) using these functions. Users would see confusing "-1d ago" or "-2d ago" labels.
- **Suggested fix**: Add a guard at the top: `if (delta < 0) return "in the future";` or similar.

---

### Finding 3: Silent API error swallowing in StatusPage

- **Severity**: INFO
- **Path**: `web/src/pages/StatusPage.tsx`
- **Lines**: 24-32
- **Evidence**:
  ```typescript
  useEffect(() => {
    const load = () => {
      api.getStatus().then(setStatus).catch(() => {});
      api.getSessions(50).then((resp) => setSessions(resp.sessions)).catch(() => {});
    };
    load();
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, []);
  ```
  Both `.catch(() => {})` silently discard errors. If the API is unreachable or returns an error, the user sees a spinner forever with no error message.
- **Why it matters**: Poor UX — no feedback to user when the dashboard can't reach the backend. Looks like a bug but is actually silent failure.
- **Suggested fix**: Show a non-blocking error state instead of silently swallowing.

---

### Finding 4: Silent error swallowing in SessionsPage.loadSessions

- **Severity**: INFO
- **Path**: `web/src/pages/SessionsPage.tsx`
- **Lines**: 307-316
- **Evidence**:
  ```typescript
  const loadSessions = useCallback((p: number) => {
    setLoading(true);
    api
      .getSessions(PAGE_SIZE, p * PAGE_SIZE)
      .then((resp) => {
        setSessions(resp.sessions);
        setTotal(resp.total);
      })
      .catch(() => {})  // ← silent
      .finally(() => setLoading(false));
  }, []);
  ```
  Same pattern as Finding 4 — errors are silently discarded, user gets no feedback.
- **Why it matters**: Same UX issue — failed session loads show no error.
- **Suggested fix**: Set an error state and display a message.

---

## No Material Issues Found In:
- `web/src/components/Markdown.tsx` — clean, well-commented lightweight parser
- `web/src/lib/nested.ts` — minimal, focused utility
- `web/src/hooks/useToast.ts` — clean hook implementation
- `web/src/lib/api.ts` — properly typed API client with Bearer token injection
- `web/src/App.tsx` — clean routing setup
- No TODO/FIXME/HACK/XXX markers found in either web/ or website/ (only "DEBUG" log-level constants, which are legitimate)
- The Docusaurus config (`docusaurus.config.ts`) and sidebars structure are well-organized
<!-- agent-23:end -->

## Agent 24
- Section ID: `agent-24`
- Assigned files: **48**
- Approx bytes: **1289518**
- File range: `website/docs/user-guide/features/fallback-providers.md` → `website/package-lock.json`
- Top-level scope: `website`
<!-- agent-24:start -->
Status: PENDING

_No findings yet._
<!-- agent-24:end -->

## Agent 25
- Section ID: `agent-25`
- Assigned files: **18**
- Approx bytes: **1454984**
- File range: `website/package.json` → `website/tsconfig.json`
- Top-level scope: `website`
<!-- agent-25:start -->
Status: PENDING

_No findings yet._
<!-- agent-25:end -->


## MiniMax Rescan Append 20260416T000649Z

- Generated: 2026-04-16T01:05:22.666864+00:00
- Source live report: `/Users/openclaw/.hermes/hermes-agent/tmp/minimax-append-scan-20260416T000649Z/problems.md`
- Append target: `/Users/openclaw/.hermes/hermes-agent/problems.md`
- Existing finding blocks considered: `11`
- New finding blocks scanned: `72`
- Unique non-overlapping findings appended: `72`
- Dedupe basis: normalized path + title similarity + line proximity against the existing root `problems.md`.

### Rescan Finding 1: Finding 1 — `run_agent.py` Referenced But Does Not Exist in Shard
- **Source agent:** `agent-01`
| Field | Value |
|-------|-------|
| **Severity** | Medium |
| **Path** | `agent/builtin_memory_provider.py` |
| **Lines** | 4–5, 35–36 |
| **Evidence** | Docstring states: *"Hermes still injects built-in MEMORY.md/USER.md directly via MemoryStore in run_agent.py"*. `system_prompt_block()` comment says: *"Built-in file memory is still injected directly by run_agent.py"*. However, `agent/run_agent.py` is NOT in the shard (it belongs to agent-02 per `problems_shards.json`). |
| **Why it matters** | `BuiltinMemoryProvider` is a compatibility shim that delegates to the direct-injection path in `run_agent.py`. Without being able to see that file, it's unclear if the shim is still in sync with the actual injection mechanism. Drift between the shim and actual behavior could cause memory context to be double-injected or silently dropped. |
| **Suggested fix** | Cross-reference `builtin_memory_provider.py` with the actual `run_agent.py` (agent-02's shard) to confirm the shim contract is still valid. If the direct injection path changed, update the shim or remove it. |

---

### Rescan Finding 2: Finding 2 — `BuiltinMemoryProvider.handle_tool_call()` Always Raises NotImplementedError
- **Source agent:** `agent-01`
| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Path** | `agent/builtin_memory_provider.py` |
| **Lines** | 50–51 |
| **Evidence** | `def handle_tool_call(...) -> str: raise NotImplementedError("BuiltinMemoryProvider does not expose tools via MemoryManager yet")` |
| **Why it matters** | `MemoryManager.handle_tool_call()` calls through to the provider's `handle_tool_call`. If this provider is used as the external memory provider (the one configured alongside the built-in), any memory tool call will hard-fail. However, `is_available()` returns `True` unconditionally, so it could be selected. The docstring says this is intentional ("yet"), but no `TODO` or tracking issue is linked. |
| **Suggested fix** | Either implement `handle_tool_call` or add an explicit `is_available()` that returns `False` until the feature is ready. Add a `# TODO:` comment with a linked issue so this isn't forgotten. |

---

### Rescan Finding 3: Finding 3 — Inconsistent Regex Flag in `memory_manager.py`
- **Source agent:** `agent-01`
| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Path** | `agent/memory_manager.py` |
| **Lines** | 29 |
| **Evidence** | `_FENCE_TAG_RE = re.compile(r'</?\\s*memory-context\\s*>', re.IGNORECASE)` — uses `re.IGNORECASE` but the fence tag `</?memory-context>` is lowercase-only and there is no uppercase variant documented or used. |
| **Why it matters** | `re.IGNORECASE` adds unnecessary regex overhead on every memory context sanitization call (which happens on every agent turn). The flag is harmless but misleading — it implies uppercase variants are valid when they are not. |
| **Suggested fix** | Remove `re.IGNORECASE` flag since the fence tag format is lowercase. Use `re.compile(r'</?\\s*memory-context\\s*>')`. |

---

### Rescan Finding 4: Finding 4 — Hardcoded User Path in `context_references.py`
- **Source agent:** `agent-01`
| Field | Value |
|-------|-------|
| **Severity** | Medium |
| **Path** | `agent/context_references.py` |
| **Lines** | `_SENSITIVE_HOME_DIRS = {..., "/Users/openclaw"}` |
| **Evidence** | `_SENSITIVE_HOME_DIRS` contains `"/Users/openclaw"` as a hardcoded path for path-filtering logic. |
| **Why it matters** | This path is a developer-specific home directory. It will never trigger filtering for any other user. More importantly, the set also includes `"~"` and `"$HOME"`, which are the correct portable forms. The hardcoded path adds noise and suggests this filtering was copy-pasted from a local development environment without being generalized. |
| **Suggested fix** | Remove `"/Users/openclaw"` from `_SENSITIVE_HOME_DIRS` — the portable `"~"` and `"$HOME"` entries already cover this case. Alternatively, expand to include other common developer home directories if the intent is broad detection. |

---

### Rescan Finding 5: Finding 5 — `copilot_acp_client.py` Has No Windows Path Handling
- **Source agent:** `agent-01`
| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Path** | `agent/copilot_acp_client.py` |
| **Lines** | `_resolve_command()` (lines ~40–65) |
| **Evidence** | `_resolve_command()` checks `HERMES_COPILOT_ACP_COMMAND`, `COPILOT_CLI_PATH`, and falls back to `"copilot"`. No handling for Windows where the Claude Code executable path differs. |
| **Why it matters** | `copilot --acp` is Claude Code's ACP bridge. Claude Code is available on Windows via the Claude Desktop app, but the executable path on Windows is not `copilot` on PATH. This means `_resolve_command()` will fail on Windows and users will get a cryptic error rather than a clear "install Claude Code" message. |
| **Suggested fix** | Add Windows detection (`sys.platform == "win32"`) and check standard Windows Claude Code install paths (e.g., `%LOCALAPPDATA%\Claude\Claude.exe`, or use `where copilot` equivalent). Provide a clear error message when Claude Code is not found on Windows. |

---

### Rescan Finding 6: Finding 6 — Stale Comment in `error_classifier.py` Referencing "OpenClaw"
- **Source agent:** `agent-01`
| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Path** | `agent/error_classifier.py` |
| **Lines** | 518–524 (`_classify_402` docstring) |
| **Evidence** | Docstring says: *"The key insight from **OpenClaw**: some 402s are transient rate limits..."* |
| **Why it matters** | The project is called "Hermes", not "OpenClaw". This appears to be a historical comment carried over from a different codebase. Minor documentation cleanliness issue, but it suggests other comments/patterns from the original project may also have been carried over without renaming. |
| **Suggested fix** | Replace "OpenClaw" with "Hermes" in the docstring. Search for other instances of "openclaw", "OpenClaw" in comments/docs across the codebase. |

---

### Rescan Finding 7: Finding 7 — Missing `sk-ant-oat*` Token Support in `_query_anthropic_context_length()`
- **Source agent:** `agent-01`
| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Path** | `agent/model_metadata.py` |
| **Lines** | 876–877 |
| **Evidence** | `_query_anthropic_context_length()` returns `None` for `sk-ant-oat*` (OAuth) tokens with comment: *"OAuth tokens can't access /v1/models"*. `get_model_context_length()` at step 4 skips the Anthropic API query for OAuth tokens. |
| **Why it matters** | Claude Code users use `sk-ant-oat*` OAuth tokens. For these users, context length detection falls through to step 5+ (OpenRouter cache, Nous suffix-match, models.dev, hardcoded defaults). For unknown models, they may get the `DEFAULT_FALLBACK_CONTEXT = 128_000` without probing. This is documented behavior but could cause unexpected context overflow errors for users of newer models via OAuth. |
| **Suggested fix** | Document this limitation clearly in the error message when falling back to 128K for OAuth users. Consider adding a debug-level log message: `"Cannot probe Anthropic /v1/models with OAuth token, using fallback context length"` to aid troubleshooting. |

---

### Rescan Finding 8: Finding 8 — Potential `None` Check Missing in `_classify_400`
- **Source agent:** `agent-01`
| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Path** | `agent/error_classifier.py` |
| **Lines** | 605 |
| **Evidence** | `is_large = approx_tokens > context_length * 0.4 or approx_tokens > 80000 or num_messages > 80` — if `context_length` is `None` or `0`, the expression `context_length * 0.4` could raise `TypeError` or produce `0` respectively. |
| **Why it matters** | If `context_length` is `None` (not validated before passing), `None * 0.4` raises `TypeError`. If it's `0`, `0 * 0.4 = 0` and `approx_tokens > 0` is always `True` for any non-zero `approx_tokens`, making the overflow classification trigger incorrectly. |
| **Suggested fix** | Add `if not context_length or context_length <= 0: return result_fn(FailoverReason.unknown, retryable=False, should_fallback=True)` at the top of `_classify_400`, or ensure callers always pass a positive integer. |

---

### Rescan Finding 9: Finding 9 — `usage_pricing.py` — `_OFFICIAL_DOCS_PRICING` Snapshot Is Already Outdated
- **Source agent:** `agent-01`
| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Path** | `agent/usage_pricing.py` |
| **Lines** | 83–100 (and throughout `_OFFICIAL_DOCS_PRICING`) |
| **Evidence** | `_OFFICIAL_DOCS_PRICING` encodes pricing for `claude-opus-4-20250514` and `claude-sonnet-4-20250514` with version `anthropic-prompt-caching-2026-03-16`. These are dated May 2025 snapshots. The source URL `https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching` points to Anthropic's prompt caching docs, which are living documents updated as pricing changes. |
| **Why it matters** | If Anthropic updates pricing and this snapshot isn't updated, `estimate_usage_cost()` will return incorrect cost estimates. The `pricing_version` field is set but there's no mechanism to detect staleness (no TTL, no check against the live docs). |
| **Suggested fix** | Add a comment warning that this snapshot must be updated when Anthropic publishes pricing changes. Consider adding a debug-level log on startup that warns if the snapshot version doesn't match the live docs version. |

---

### Rescan Finding 10: Finding 10 — `skill_utils.py` Has Unused `sys` Import
- **Source agent:** `agent-01`
| Field | Value |
|-------|-------|
| **Severity** | Negligible |
| **Path** | `agent/skill_utils.py` |
| **Lines** | 11 |
| **Evidence** | `from typing import Any, Dict, List, Optional, Set, Tuple` — `sys` is imported at line 12 (`import sys`) but never used in the file (confirmed via grep). |
| **Why it matters** | Minor dead import. No functional impact. |
| **Suggested fix** | Remove `import sys` from `skill_utils.py`. |

---

### Rescan Finding 11: Finding 11 — `display.py` Emoji Characters May Not Render in All Terminals
- **Source agent:** `agent-01`
| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Path** | `agent/display.py` |
| **Lines** | `KAWAII_WAITING` and `KAWAII_THINKING` arrays (~lines 50–80) |
| **Evidence** | `KawaiiSpinner` uses emoji arrays like `"🪄"`, `"🦄"`, `"🌸"`, `"🌈"`, `"⭐"` for CLI spinner animation. These characters may not render correctly on Windows terminals (legacy console), some SSH terminals, or older Linux distros without emoji font support. |
| **Why it matters** | Users with terminals that don't support emoji will see blank spaces or tofu characters instead of the spinner, degrading the CLI experience without any fallback. |
| **Suggested fix** | Add a `USE_EMOJI` environment variable or auto-detect terminal capability (check `TERM`, `LC_ALL`, or use `blessed`/`curses` for terminal capability detection). Provide ASCII fallback spinner characters (`*`, `-`, `+`, `#`) for unsupported terminals. |

---

## No Material Issues Found In:

The following files were reviewed and contain no material issues:
- `agent/anthropic_adapter.py` — Well-structured, comprehensive
- `agent/auxiliary_client.py` — Well-structured
- `agent/context_compressor.py` — Comprehensive compression logic
- `agent/context_engine.py` — Clean threshold-based logic
- `agent/context_references.py` — (Finding 4 above aside, logic is sound)
- `agent/copilot_acp_client.py` — (Finding 5 above aside, logic is sound)
- `agent/credential_pool.py` — (Extensive reads, logic is sound)
- `agent/error_classifier.py` — (Findings 6, 8 above aside, comprehensive)
- `agent/insights.py` — Comprehensive analytics engine
- `agent/memory_provider.py` — Clean ABC interface
- `agent/model_metadata.py` — (Findings 7 above aside, comprehensive)
- `agent/models_dev.py` — Clean registry pattern
- `agent/prompt_builder.py` — (Extensive reads, comprehensive)
- `agent/manual_compression_feedback.py` — Simple and correct

---

## Summary

| Severity | Count |
|----------|-------|
| Medium | 2 |
| Low | 8 |
| Negligible | 1 |
| **Total** | **11** |

**Total findings: 11**

The most actionable finding is **Finding 1** — `run_agent.py` (the actual injection point for built-in memory) is not in the same shard as the `BuiltinMemoryProvider` shim, creating a coordination risk. **Finding 2** (NotImplementedError shim) and **Finding 4** (hardcoded developer path) are also worth addressing. The rest are minor cleanliness and robustness improvements.

### Rescan Finding 12: CRITICAL — Auxiliary API Key Env Var Names Truncated with "..." (causes silent failure)
- **Source agent:** `agent-02`
**Severity:** CRITICAL

**Paths:**
- `cli.py`, lines 480, 486, 492
- `gateway/run.py`, lines 148, 154, 160

**Evidence:**
```python
# cli.py lines 473-493
auxiliary_task_env = {
    "vision": {
        "api_key": "AUXILI..._KEY",   # BUG: truncated
    },
    "web_extract": {
        "api_key": "AUXILI..._KEY",   # BUG: truncated
    },
    "approval": {
        "api_key": "AUXILI..._KEY",   # BUG: truncated
    },
}
```
The environment variable names are literal `"AUXILI..._KEY"` strings instead of the correct `"AUXILIARY_VISION_API_KEY"`, `"AUXILIARY_WEB_EXTRACT_API_KEY"`, `"AUXILIARY_APPROVAL_API_KEY"`.

**Why it matters:** When a user configures `auxiliary.vision.api_key` in their config file and expects it to bridge to the `AUXILIARY_VISION_API_KEY` env var (documented in environment-variables.md), the code silently sets `AUXILI..._KEY` instead. The vision/web_extract/approval tasks then fail at runtime with missing API key errors, with no indication that the bug is in the config bridging layer. This is a complete functional failure of the auxiliary task system.

**Suggested fix:** Replace all three truncated strings:
- `"AUXILI..._KEY"` → `"AUXILIARY_VISION_API_KEY"`
- `"AUXILI..._KEY"` → `"AUXILIARY_WEB_EXTRACT_API_KEY"`
- `"AUXILI..._KEY"` → `"AUXILIARY_APPROVAL_API_KEY"`

The same fix needed in `gateway/run.py` at the corresponding positions.

---

### Rescan Finding 13: MEDIUM — `jittered_backoff` global state with threading.Lock is unnecessary
- **Source agent:** `agent-02`
**Severity:** MEDIUM

**Path:** `agent/retry_utils.py`, lines 20-21, 32-37

**Evidence:**
```python
_jitter_counter = 0
_jitter_lock = threading.Lock()

def jittered_backoff(attempt: int, ...) -> float:
    ...
    with _jitter_lock:
        _jitter_counter += 1
        counter = _jitter_counter
    ...
```

**Why it matters:** The counter and lock exist solely to decorrelate backoff values across concurrent calls by mixing in a unique-per-call number via XOR. However, Python's `random` module is already thread-safe (uses its own internal lock), and the per-call decorrelation via time_ns XOR golden_ratio is unnecessarily complex. The function does not use the global counter value for anything — it only increments it — meaning concurrent calls produce decorrelated values but with overhead of threading.Lock on every call. In a high-throughput batch system (batch_runner.py with 128 thread pool workers), this adds unnecessary lock contention.

**Suggested fix:** Remove `_jitter_counter` and `_jitter_lock` entirely. The time_ns-based XOR with golden ratio already provides sufficient decorrelation without shared state. Replace with a pure-local approach:
```python
def jittered_backoff(attempt: int, base_delay: float = 5.0, max_delay: float = 120.0,
                     jitter_ratio: float = 0.5) -> float:
    exp = min(attempt * 3, 20)  # cap exponent to avoid overflow
    base = min(base_delay * (2 ** exp), max_delay)
    # Remove lock and counter; time_ns provides enough uniqueness
    import time
    unique = time.time_ns() ^ 0x9e3779b97f4a7c15  # golden ratio mix
    jitter = ((unique % 1000) / 1000.0) * base * jitter_ratio
    return min(base + jitter, max_delay)
```

---

### Rescan Finding 14: MEDIUM — `trajectory.py` save_trajectory silently fails on file errors
- **Source agent:** `agent-02`
**Severity:** MEDIUM

**Path:** `agent/prompting/scratchpad.py`, lines 51-56 (save_trajectory function)

**Evidence:**
```python
try:
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    logger.info("Trajectory saved to %s", filename)
except Exception as e:
    logger.warning("Failed to save trajectory: %s", e)
```

**Why it matters:** Trajectory data (the ShareGPT-format conversation logs used for OPD training in `agentic_opd_env.py`) is silently discarded on any I/O error (permissions, disk full, path not found). The warning log may scroll past in a busy batch run. For OPD training where trajectories are the training signal, losing even a fraction of trajectories introduces bias. There's no fallback to an alternative path, no alerting mechanism, and no metric tracking save failures.

**Suggested fix:** Add a fallback path for critical trajectory data (e.g., write to a temp location if primary fails), track save failures in a metric, and at minimum elevate the log level to `error` since silently losing training data is serious.

---

### Rescan Finding 15: LOW — `has_incomplete_scratchpad()` doesn't handle nested tags
- **Source agent:** `agent-02`
**Severity:** LOW

**Path:** `agent/prompting/scratchpad.py`, lines 23-27

**Evidence:**
```python
def has_incomplete_scratchpad(content: str) -> bool:
    if not content:
        return False
    return "<REASONING_SCRATCHPAD>" in content and "</REASONING_SCRATCHPAD>" not in content
```

**Why it matters:** The function uses simple substring matching. If content contains `</REASONING_SCRATCHPAD>` inside a string literal (e.g., `content += "</REASONING_SCRATCHPAD>"`) or a nested opening tag, the check could produce incorrect results. This is a low-risk issue since such content would be unusual, but it could mask a genuinely incomplete scratchpad.

**Suggested fix:** Use a simple regex with balanced tag counting, or at minimum check that the closing tag appears after the last opening tag:
```python
def has_incomplete_scratchpad(content: str) -> bool:
    if not content:
        return False
    opens = content.count("<REASONING_SCRATCHPAD>")
    closes = content.count("</REASONING_SCRATCHPAD>")
    return opens > closes
```

---

### Rescan Finding 16: INFO — OPD environment `compute_reward` runs tests in user sandbox
- **Source agent:** `agent-02`
**Severity:** INFO

**Path:** `environments/agentic_opd_env.py`, line 569

**Evidence:**
```python
test_result = ctx.terminal("python test_solution.py 2>&1", timeout=30)
```

**Why it matters:** The reward computation executes the agent's test code in the shared sandbox (`ctx.terminal`). While the environment is designed for coding tasks with controlled test_code, the `test_code` from the dataset is passed directly to `ctx.terminal()` without a sandbox wrapper. A malicious or malformed dataset could execute arbitrary code. This is acceptable for internal/trusted datasets but should be documented as a security consideration for untrusted dataset sources.

**Suggested fix:** Document this clearly in the class docstring and add a warning comment at the call site.

---

### Rescan Finding 17: INFO — Scheduler `asyncio.to_thread()` inside already-async `run_job`
- **Source agent:** `agent-02`
**Severity:** INFO

**Path:** `cron/scheduler.py`, line 180 (approximate area)

**Evidence:**
```python
async def run_job(...) -> JobResult:
    ...
    result = await asyncio.to_thread(_execute_job_sync, job_config)
```

**Why it matters:** `asyncio.to_thread()` is designed to offload blocking I/O to a thread pool from within an async context. However, `_execute_job_sync` likely contains its own blocking calls (subprocess, file I/O). The scheduler uses its own thread pool (with `max_workers` concurrency). Using `asyncio.to_thread()` adds an extra layer of threading indirection (async thread → scheduler thread pool thread). If `_execute_job_sync` is purely CPU-bound or blocking-I/O-bound, the current pattern is fine. If it were already designed to run in the scheduler's own thread pool, the extra `asyncio.to_thread()` wrapper is redundant overhead.

**Suggested fix:** Confirm `_execute_job_sync` design. If it doesn't spawn threads internally, the `asyncio.to_thread()` wrapper adds ~1ms overhead per job call for no benefit.

---

## Summary

| # | Severity | Path | Issue |
|---|----------|------|-------|
| 1 | CRITICAL | cli.py:480,486,492; gateway/run.py:148,154,160 | Auxiliary api_key env vars set to literal `"AUXILI..._KEY"` instead of real env var names — complete functional failure |
| 2 | MEDIUM | agent/retry_utils.py:20-37 | Unnecessary threading.Lock + global counter in jittered_backoff adds lock contention in high-throughput batch contexts |
| 3 | MEDIUM | agent/prompting/scratchpad.py:51-56 | Trajectory save failures silently logged then discarded — no fallback, no metrics |
| 4 | LOW | agent/prompting/scratchpad.py:23-27 | `has_incomplete_scratchpad()` uses naive substring matching — edge case false negatives possible |
| 5 | INFO | environments/agentic_opd_env.py:569 | OPD reward computation executes untrusted test_code in sandbox — document for security |
| 6 | INFO | cron/scheduler.py | `asyncio.to_thread()` wrapper around `_execute_job_sync` may be redundant overhead |

**Total: 6 findings (1 critical, 2 medium, 1 low, 2 info)**

### Rescan Finding 18: Shell injection risk in SWE env reward function
- **Source agent:** `agent-03`
- **Severity:** Medium
- **Path:** `environments/hermes_swe_env/hermes_swe_env.py`
- **Line(s):** 178–179
- **Evidence:**
  ```python
  test_result = ctx.terminal(
      f'cd /workspace && python3 -c "{test_code}"', timeout=60
  )
  ```
- **Why it matters:** `test_code` comes from the dataset's `test`/`test_code` field. If a dataset item contains a double-quote, `$()`, or backtick, it becomes a shell injection vector when interpolated into the f-string. While this runs inside a Modal sandbox, sandbox escapes are not impossible, and the injected command could interfere with test verification.
- **Suggested fix:** Pass arguments safely via a temp file or `python3 -c` with arguments list:
  ```python
  import tempfile, json
  with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
      f.write(test_code)
      f.flush()
      test_result = ctx.terminal(f'python3 {f.name}', timeout=60)
  ```

---

### Rescan Finding 19: Same shell injection risk in TerminalTestEnv
- **Source agent:** `agent-03`
- **Severity:** Medium
- **Path:** `environments/terminal_test_env/terminal_test_env.py`
- **Line(s):** 189
- **Evidence:**
  ```python
  verify_result = ctx.terminal(f"cat {item['verify_path']}")
  ```
- **Why it matters:** `verify_path` is a user-controlled task definition (e.g., `~/greeting.txt`). Paths with shell metacharacters (`;`, `|`, `&&`, `$()`) would execute arbitrary commands. The paths look controlled because they come from inline task definitions, but they flow through the same `ctx.terminal()` path.
- **Suggested fix:** Use a safe wrapper or split arguments:
  ```python
  import shlex
  verify_result = ctx.terminal(f"cat {shlex.quote(item['verify_path'])}")
  ```

---

### Rescan Finding 20: Stale patch module kept as no-op creates confusion
- **Source agent:** `agent-03`
- **Severity:** Low
- **Path:** `environments/patches.py`
- **Line(s):** 1–36 (entire file)
- **Evidence:** The module's docstring says it "monkey patches for async frameworks" but its body is:
  ```python
  def apply_patches():
      global _patches_applied
      if _patches_applied:
          return
      logger.debug("apply_patches() called; no patches needed (async safety is built-in)")
      _patches_applied = True
  ```
  A comment says it is "kept for backward compatibility." It is still imported by `hermes_base_env.py`.
- **Why it matters:** Dead code that implies functionality exists. If the Modal environment's `_AsyncWorker` thread approach is later removed or changed, this silently becomes a no-op with no indication. Import chains increase startup time and memory.
- **Suggested fix:** Either remove the module and its import in `hermes_base_env.py`, or add a comment explicitly flagging it as deprecated and listing the removal version.

---

### Rescan Finding 21: Boot-md hook fragile [SILENT] detection
- **Source agent:** `agent-03`
- **Severity:** Low
- **Path:** `gateway/builtin_hooks/boot_md.py`
- **Line(s):** 59
- **Evidence:**
  ```python
  if response and "[SILENT]" not in response:
      logger.info("boot-md completed: %s", response[:200])
  ```
- **Why it matters:** A literal string check `[SILENT]` could accidentally match if the agent's response naturally contains that text. The check should be more precise (e.g., exact equality after stripping whitespace).
- **Suggested fix:** Require exact match or use a clearly-delimited marker:
  ```python
  if response and response.strip() != "[SILENT]":
  ```

---

### Rescan Finding 22: DeepSeekV3 parser discards `type` field without validation
- **Source agent:** `agent-03`
- **Severity:** Low
- **Path:** `environments/tool_call_parsers/deepseek_v3_parser.py`
- **Line(s):** 44–47
- **Evidence:**
  ```python
  PATTERN = re.compile(
      r"<｜tool▁call▁begin｜>(?P<type>.*?)<｜tool▁sep｜>(?P<function_name>.*?)\s*```json\s*(?P<function_arguments>.*?)\s*```\s*<｜tool▁call▁end｜>",
      re.DOTALL,
  )
  ```
  The `type` named group is captured but never used. The `function_name` capture includes the full `type` prefix if the model outputs it differently than expected.
- **Why it matters:** If the model outputs a different format (e.g., type not separated cleanly), the function name would include the type prefix, causing a tool-not-found error. No validation or warning is issued.
- **Suggested fix:** Either validate/use the captured `type` group, or strip common prefixes from `func_name` before lookup.

---

### Rescan Finding 23: Glm47ToolCallParser __init__ overrides regex but not start token
- **Source agent:** `agent-03`
- **Severity:** Info
- **Path:** `environments/tool_call_parsers/glm47_parser.py`
- **Line(s):** 24–35
- **Evidence:**
  ```python
  def __init__(self):
      super().__init__()
      self.FUNC_DETAIL_REGEX = re.compile(...)
      self.FUNC_ARG_REGEX = re.compile(...)
  ```
  `Glm45ToolCallParser` sets `START_TOKEN = "***"` (the token that guards the parse call). `Glm47ToolCallParser` never overrides `START_TOKEN`, so it continues using `"<tool_call>"` as the guard. The GLM 4.7 format still uses `<tool_call>` tags, so this works — but the inheritance chain is implicit and fragile.
- **Why it matters:** If the GLM 4.7 format ever diverges on start token, this would silently fall back to the wrong parser behavior. The implicit sharing of `START_TOKEN` across subclasses makes the behavior hard to reason about.
- **Suggested fix:** Add an explicit `START_TOKEN` override in `Glm47ToolCallParser` for clarity.

---

### Rescan Finding 24: DeliveryRouter._deliver_local uses Path.write_text without atomic guarantee
- **Source agent:** `agent-03`
- **Severity:** Info
- **Path:** `gateway/delivery.py`
- **Line(s):** 208
- **Evidence:**
  ```python
  output_path.write_text("\n".join(lines))
  ```
  While the class uses `DeliveryTarget` parsing with proper platform routing, the `_deliver_local` method writes directly with `Path.write_text()` — not atomic. Other parts of the codebase (e.g., `PairingStore._secure_write`) use `tempfile.mkstemp + os.fsync + os.replace` for atomicity.
- **Why it matters:** If two cron jobs write simultaneously (different job IDs go to the same dir), or if the gateway crashes mid-write, the output file could be corrupted. The delivery router iterates over targets sequentially so intra-target collision is unlikely, but not impossible.
- **Suggested fix:** Use `atomic_json_write` (already imported in `channel_directory.py` from `utils`) or the same `tempfile.mkstemp` pattern used in pairing.py.

---

### Rescan Finding 25: LlamaParser content boundary logic could misfire
- **Source agent:** `agent-03`
- **Severity:** Info
- **Path:** `environments/tool_call_parsers/llama_parser.py`
- **Line(s):** 88–91
- **Evidence:**
  ```python
  first_tc_start = text.find("{")
  if self.BOT_TOKEN in text:
      first_tc_start = text.find(self.BOT_TOKEN)
  content = text[:first_tc_start].strip() if first_tc_start > 0 else None
  ```
  If `BOT_TOKEN` appears before any `{` in the text (e.g., in explanatory text), `first_tc_start` would be set to that earlier position, truncating valid content. The logic is correct for the documented format but assumes the model never emits the BOT_TOKEN in content.
- **Why it matters:** If the model generates explanatory text containing `***` before the actual tool call JSON, the content would be incorrectly truncated.
- **Suggested fix:** Find the position of the first JSON object's start `{` (tracked during parsing) rather than searching from the beginning of text.

---

## No Material Issues Found

The following files were reviewed and appear well-implemented:

- **`gateway/hooks.py`** — HookRegistry: robust dynamic loading, wildcard event matching, sync/async handler support via `asyncio.iscoroutine()` check. Error isolation is correct.
- **`gateway/pairing.py`** — PairingStore: uses `threading.RLock()` for concurrent thread safety, atomic writes via `tempfile.mkstemp + os.fsync + os.replace`, secure `chmod 0o600`, OWASP-aligned code generation with `secrets.choice()`.
- **`gateway/channel_directory.py`** — build_channel_directory: proper `_SKIP_SESSION_DISCOVERY` frozenset, graceful adapter exception handling, session-based fallback discovery.
- **`gateway/display_config.py`** — Tiered platform defaults (HIGH/MEDIUM/LOW/MINIMAL), backward compat for `tool_progress_overrides`, YAML normalization for bare `off`/`on` values.
- **`gateway/mirror.py`** — Best-match session finding by `updated_at` timestamp, dual JSONL + SQLite writes, all errors caught silently.
- **`gateway/config.py`** — Deep-merge for platform `extra` dicts, env var overrides, comprehensive validation with warnings (not exceptions).
- **`send_message_tool.py`** — Regex-based target parsing for multiple platforms, secret redaction in error messages, `shlex.quote` equivalent sanitization.
- **`flake.nix`** — Clean module imports, correctly references local nix files.
- **`ADDING_A_PLATFORM.md`** — Comprehensive 16-section checklist for platform integration; no stale references detected.
- **All tool call parsers** — Implement `ToolCallParser` ABC correctly, use `@register_parser` decorator, return proper `ParseResult` tuples, handle exceptions gracefully by returning original text.

### Rescan Finding 26: Finding 1
- **Source agent:** `agent-04`
- **Severity**: HIGH
- **Path**: `gateway/platforms/wecom.py`
- **Line(s)**: 280
- **Evidence**: `{"bot_id": self._bot_id, "secret": self._secret}` sent in plaintext on WebSocket connect
- **Why it matters**: WeCom credentials transmitted in plaintext over WebSocket. Any network observer (MITM, proxy logs, WebSocket proxy) can capture the `secret` field and authenticate as the bot.
- **Suggested fix**: Use TLS (wss://) exclusively; do not send plaintext secret over non-TLS connections. Ideally use a proper auth handshake that does not expose the secret in the initial subscribe payload.

---

### Rescan Finding 27: Finding 2
- **Source agent:** `agent-04`
- **Severity**: HIGH
- **Path**: `gateway/platforms/sms.py`
- **Line(s)**: 97–115
- **Evidence**: `SMS_INSECURE_NO_SIGNATURE=true` disables Twilio request signature validation entirely
- **Why it matters**: Disabling signature validation allows any client that can reach the webhook port to inject arbitrary SMS messages. The code warns in logs but does not enforce; an accidental misconfiguration in production exposes the Twilio integration to message injection.
- **Suggested fix**: Require signature validation in production (no bypass flag), or gate the bypass with a locked-down config that is never reachable from untrusted networks. Make the flag a fatal startup error rather than a warning.

---

### Rescan Finding 28: Finding 3
- **Source agent:** `agent-04`
- **Severity**: MEDIUM
- **Path**: `gateway/platforms/wecom_crypto.py`
- **Line(s)**: 54–57
- **Evidence**: PKCS7 padding validation only checks last byte and verifies `decrypted[-pad:] == bytes([pad]) * pad`
- **Why it matters**: This is a deterministic check. An active attacker with ciphertext knowledge cannot safely distinguish padding errors vs. malformed data, increasing risk of padding oracle attacks if the decrypt path is ever reachable in an attackable context. Additionally, SHA1 is used for signature (line 63) — deprecated and vulnerable to collision attacks.
- **Suggested fix**: Use an authenticated encryption mode (AES-GCM) instead of AES-CBC + separate HMAC. If AES-CBC is required, use a proper HMAC-SHA256 for integrity. Migrate off SHA1 for signatures.

---

### Rescan Finding 29: Finding 4
- **Source agent:** `agent-04`
- **Severity**: LOW
- **Path**: `gateway/platforms/whatsapp.py`
- **Line(s)**: 35–67
- **Evidence**: `_kill_port_process()` silently catches all exceptions with `except Exception: pass`
- **Why it matters**: Process killing failures are silently swallowed. If `fuser` or `netstat` behaves unexpectedly, the function returns normally and the port collision may cause the bridge to start on an unexpected port or fail ambiguously.
- **Suggested fix**: Log at least a warning when port-kill operations fail, so operators can diagnose bridge startup failures.

---

### Rescan Finding 30: Finding 5
- **Source agent:** `agent-04`
- **Severity**: LOW
- **Path**: `gateway/sticker_cache.py`
- **Line(s)**: 44
- **Evidence**: `self._cache_path = Path.home() / ".hermes" / "sticker_cache.json"`
- **Why it matters**: `Path.home()` can return `None` or an unexpected path in certain environments (e.g., UID without a home directory). This would cause the cache write to fail at runtime.
- **Suggested fix**: Fall back to `get_hermes_dir()` or a known-safe default when `Path.home()` is unreliable, rather than using it unconditionally.

---

### Rescan Finding 31: Finding 6
- **Source agent:** `agent-04`
- **Severity**: LOW
- **Path**: `gateway/platforms/weixin.py`
- **Line(s)**: 172–183
- **Evidence**: `_headers()` function sends a random `X-WECHAT-UIN` header per request
- **Why it matters**: The header is generated from a random struct-unpacked integer encoded in base64 — it is not a real WeChat UIN and does not serve any documented security or routing purpose. This could trigger anti-bot heuristics on Tencent's iLink API if headers are being validated.
- **Suggested fix**: Remove the `X-WECHAT-UIN` header if it has no functional role, or document its intended purpose clearly.

---

## No Material Issues Found
The following files were reviewed and appear correct:
- `gateway/session_context.py` — ContextVar-based thread-safe session state; clean design
- `gateway/status.py` — PID file management with start-time verification; well-guarded
- `gateway/stream_consumer.py` — Async streaming with think-block suppression; queue-based coordination is sound
- `gateway/run.py` — SSL auto-detection chain, .env loading; overall solid
- `hermes_cli/__init__.py` — Version info only
- `hermes` — CLI wrapper; minimal
- `gateway/platforms/telegram.py` — Telegram bot adapter; good use of mention patterns and text batching
- `gateway/platforms/telegram_network.py` — Fallback IP transport with sticky session; properly validates IPs

### Rescan Finding 32: `float("inf")` → `int()` raises uncaught `OverflowError`
- **Source agent:** `agent-07`
**Severity:** Medium
**Path:** `model_tools.py`
**Line(s):** ~430–443
**Evidence:**
```python
def _coerce_number(value: str, integer_only: bool = False):
    try:
        f = float(value)
    except (ValueError, OverflowError):
        return value
    if f != f or f == float("inf") or f == float("-inf"):
        return f
    if f == int(f):
        return int(f)
    if integer_only:
        return value
    return f
```
The guard `if f == float("inf")` prevents returning infinity as a float, but then falls through to `int(f)` without catching `OverflowError`. In Python, `int(float("inf"))` raises `OverflowError: cannot convert float infinity to integer` — this is **not** caught by the bare `except (ValueError, OverflowError)` block higher up, because that block has already been passed before the infinity check.

**Why it matters:** If an LLM passes `"Infinity"`, `"inf"`, or similar strings as a tool argument typed as integer/number, the tool call handler in `coerce_tool_args` → `_coerce_value` → `_coerce_number` will raise an uncaught `OverflowError` that propagates as a 500-level crash, rather than gracefully falling back to the original string.

**Suggested fix:** Add `except OverflowError` around `int(f)`:
```python
if f == int(f):
    try:
        return int(f)
    except OverflowError:
        return value
```

---

### Rescan Finding 33: `actual_cost_usd` treats `None` differently from `estimated_cost_usd` in `absolute=True` mode
- **Source agent:** `agent-07`
**Severity:** Low
**Path:** `hermes_state.py`
**Line(s):** ~400–430
**Evidence (absolute-mode SQL branch):**
```python
estimated_cost_usd = COALESCE(?, 0),   # ← overwrites with 0 when None passed
actual_cost_usd = CASE
    WHEN ? IS NULL THEN actual_cost_usd   # ← preserves existing when None passed!
    ELSE ?
END,
...
params = (
    ...
    estimated_cost_usd,   # COALESCE(?, 0) — sets to 0 if None
    actual_cost_usd,       # CASE check
    actual_cost_usd,       # ELSE branch value
    ...
)
```
The docstring states for `absolute=True`: "values are **set directly** — use this when the caller already holds cumulative totals." However, `actual_cost_usd` uses a `CASE WHEN ? IS NULL THEN actual_cost_usd` pattern that **preserves** the existing DB value when `None` is passed, contradicting "set directly." In contrast, `estimated_cost_usd` uses `COALESCE(?, 0)` which correctly sets to 0 when `None` is passed. The inconsistency means a caller cannot use `absolute=True` to explicitly clear/reset `actual_cost_usd`.

**Why it matters:** Gateway code that accumulates `actual_cost_usd` across sessions and later wants to reset it (e.g., billing correction) cannot do so via the `absolute=True` path.

**Suggested fix:** Make `actual_cost_usd` in absolute mode consistent with `estimated_cost_usd` — use `COALESCE(?, actual_cost_usd)` if the intent is "set to this value, treat None as no-op," or document the divergence explicitly if the current behavior is intentional.

---

### Rescan Finding 34: quadratic backtracking on mixed unquoted/quoted hyphenated input
- **Source agent:** `agent-07`
**Severity:** Low
**Path:** `hermes_state.py`
**Line(s):** ~940–970
**Evidence:**
```python
sanitized = re.sub(r'"[^"]*"', _preserve_quoted, query)   # Step 1: protect quotes
sanitized = re.sub(r'[+{}()"^]', " ", sanitized)         # Step 2: strip specials
...
sanitized = re.sub(r"\b(\w+(?:[.-]\w+)+)\b", r'"\1"', sanitized)  # Step 5
```
The Step 5 regex `(?:[.-]\w+)+` with a non-greedy `+` causes O(n²) worst-case behavior when the unquoted prefix before a closing quote consists of many hyphen/period-separated segments. At each position, the engine tries 1, 2, 3… repetitions of the inner group before backtracking, producing quadratic time on patterns like `prefix-word-word-word "end`.

**Why it matters:** `search_messages` is an internal API (not directly exposed to untrusted network clients), but a user inside an authenticated session could enter a crafted search query that causes noticeable latency (~seconds on a 500-char input).

**Suggested fix:** Rewrite the hyphenated-segment match to avoid nested quantifiers:
```python
# Match individual segments without nested + quantifier
sanitized = re.sub(r'\b([a-zA-Z0-9]+(?:[-.][a-zA-Z0-9]+)+)\b', r'"\1"', sanitized)
```
Or process character-by-character without backtracking via regex.

---

## No Material Issues Found In

- `hermes_time.py` — clean timezone resolution with proper `ZoneInfo` caching and fallback
- `hermes_constants.py` — well-structured with clear docstrings; `_wsl_detected`, `_container_detected` caching is correct
- `hermes_logging.py` — `_ManagedRotatingFileHandler` chmod fix for NixOS is sound; `_install_session_record_factory` is properly idempotent
- `mcp_serve.py` — `EventBridge` mtime-skip optimization is correct; `_extract_message_content` handles list content safely; lazy MCP import with graceful fallback is proper
- `mini_swe_runner.py` — `_convert_to_hermes_format` correctly processes trajectory format; `create_environment` factory is clean
- `hermes_cli/webhook.py` — HMAC signature in `_cmd_test` is correct; `os.replace` for atomic write is proper
- `hermes_cli/web_server.py` — config normalization/denormalization round-trip is careful; FTS5 auto-prefix wildcard addition is thoughtful

---

*Agent 07 audit complete. 3 findings logged above.*

### Rescan Finding 35: Baileys Dependency Version Mismatch
- **Source agent:** `agent-09`
- **Severity:** Medium
- **Path:** scripts/whatsapp-bridge/package.json vs bridge.js
- **Lines:** package.json line 11; bridge.js line 21
- **Evidence:** package.json pins `@whiskeysockets/baileys` to git hash `01047debd81beb20da7b7779b08edcb06aa03770`, but package-lock.json resolves to `WhiskeySockets/Baileys#fix/abprops-abt-fetch`. bridge.js imports from `@whiskeysockets/baileys` directly.
- **Why it matters:** Inconsistent dependency references make it unclear which version is actually being used at runtime. The lockfile and source don't agree.
- **Suggested fix:** Unify to a single git ref in package.json and ensure package-lock.json is regenerated to match.

### Rescan Finding 36: Placeholder Comments in Production Code
- **Source agent:** `agent-09`
- **Severity:** Low
- **Path:** scripts/whatsapp-bridge/bridge.js
- **Lines:** 138 ("// TODO: ..."), 313 ("// TODO: ...")
- **Evidence:** Two inline TODO comments remain in production bridge.js
- **Why it matters:** Placeholder TODOs in production code are technical debt. They should either be resolved or tracked in an issue tracker.
- **Suggested fix:** Either implement the missing functionality or remove the TODOs and create a GitHub issue instead.

### Rescan Finding 37: Example Email Address in Documentation
- **Source agent:** `agent-09`
- **Severity:** Low
- **Path:** scripts/contributor_audit.py
- **Lines:** 56
- **Evidence:** `hermes-audit@example.com` appears in a docstring as a placeholder sender email.
- **Why it matters:** Example domain emails in docs are harmless but should use proper placeholder notation (e.g., `example@example.com`) or be marked clearly as placeholders.
- **Suggested fix:** Use a more explicit placeholder format like `your-email@example.com` or add a note that this is an example.

### Rescan Finding 38: Hardcoded Example Domain in AUTHOR_MAP
- **Source agent:** `agent-09`
- **Severity:** Low
- **Path:** scripts/release.py
- **Lines:** 41 (AUTHOR_MAP placeholder value `***`)
- **Evidence:** The AUTHOR_MAP variable has a placeholder prefix `***` on line 41 suggesting incomplete data or redaction, followed by what appears to be a legitimate (but dense) contributor mapping table.
- **Why it matters:** The placeholder prefix is odd and could indicate partial data or a formatting artifact from manual editing.
- **Suggested fix:** Verify all contributor emails are correctly mapped and remove any placeholder markers.

---

**Summary:** 4 findings (2 Medium, 2 Low). No critical bugs, security issues, or broken paths detected. The Baileys dependency mismatch is the most actionable issue.

### Rescan Finding 39: Empty/Stale Index Cache File
- **Source agent:** `agent-10`
**Severity:** LOW
**Path:** `skills/index-cache/openai_skills_skills_.json`
**Line(s):** 1
**Evidence:** File contains only `[]` (empty JSON array)
**Why it matters:** This index cache is effectively a placeholder — it provides no entries for the OpenAI skills index. If any agent or process relies on this cached index for tooling/function definitions, it will find nothing. This could indicate a failed cache generation step, a network error during the original index build, or an intentionally empty source.
**Suggested fix:** Regenerate the index by re-running the skills index builder script for the OpenAI source, or verify whether this empty state is intentional (e.g., no OpenAI-specific skills exist in this repo vs. other sources).

---

### Rescan Finding 40: Missing `generative-widgets` Skill Referenced by 54 Templates
- **Source agent:** `agent-10`
**Severity:** LOW-MEDIUM
**Path:** `skills/creative/popular-web-designs/templates/*.md` (54 files)
**Line(s):** Various — e.g., `skills/creative/popular-web-designs/templates/stripe.md:13`
**Evidence:** Every one of the 54 design-system templates contains the instruction: "serve via `generative-widgets` skill (cloudflared tunnel)". The `generative-widgets` skill does not exist anywhere in the `skills/` directory.
**Why it matters:** When an agent follows the popular-web-designs skill workflow (pick template → load with `skill_view` → generate HTML), it will eventually try to serve the result via `generative-widgets` — a skill that is not present. This breaks the advertised end-to-end workflow. The agent would need to improvise an alternative serving mechanism.
**Suggested fix:** Either (a) create the `generative-widgets` skill, (b) update all 54 templates to reference an existing serving skill (e.g., a simple HTTP server skill), or (c) update the main `popular-web-designs/SKILL.md` to document an explicit fallback serving method.

---

### Rescan Finding 41: `gif-search` Skill Assumes `jq` Without Noting Installation
- **Source agent:** `agent-10`
**Severity:** LOW
**Path:** `skills/media/gif-search/SKILL.md`
**Line(s):** 29-42
**Evidence:** The prerequisites section lists `commands: [curl, jq]` but does not explain how to install `jq`. All example commands use `jq` for JSON processing. `jq` is not a standard macOS/Linux utility by default (macOS ships with `json.tool` in Python but no `jq`).
**Why it matters:** An agent or user following the skill verbatim on a fresh system will find `jq: command not found`. While `jq` is common in developer environments, it is not universally present.
**Suggested fix:** Add a brief "Installation" note: e.g., `macOS: brew install jq`, `Ubuntu/Debian: sudo apt install jq`, or document how to use `python3 -m json.tool` as a `jq`-free alternative.

---

### Rescan Finding 42: Documentation references non-existent directory structure in p5js skill
- **Source agent:** `agent-10`
**Severity:** LOW
**Path:** `skills/creative/p5js/README.md`
**Line(s):** 46
**Evidence:** The README file is labeled `README.md` (not `SKILL.md`), which is an unusual choice for a Hermes skill. It documents a directory structure showing `SKILL.md` alongside reference files, but the p5js skill's main entry is actually `SKILL.md` at the root of `skills/creative/p5js/`.
**Why it matters:** The README.md at `skills/creative/p5js/README.md` appears to be organizational documentation rather than the skill entry point. The actual `SKILL.md` for p5js is at `skills/creative/p5js/SKILL.md`. The README may confuse agents looking for the skill entry point.
**Suggested fix:** Consider whether `README.md` is intended as supplemental documentation (in which case it should probably be moved to a `references/` subdirectory) or whether it should be removed to avoid confusion with the actual `SKILL.md` entry point.

---

## No Material Issues Found In:
- JSON index caches (except `openai_skills_skills_.json` which is empty)
- Shell scripts (`*.sh`) — syntactically correct, use proper shebangs, include safety checks
- Python helper scripts (`*.py`) in `scripts/` directories — properly structured with `if __name__ == "__main__"`, argument parsing, error handling
- MLOps SKILL.md files — generally well-structured with frontmatter, clear dependency specs, troubleshooting sections
- Creative skill reference docs — comprehensive, accurate code examples
- Template files (HTML, CSS, design system templates) — properly formatted

---

*Audit completed by agent-10*

### Rescan Finding 43: Finding 1 - Malformed regex pattern in freeze_layers_except docstring
- **Source agent:** `agent-11`
- **Severity:** Medium
- **Path:** skills/mlops/training/axolotl/references/api.md
- **Line(s):** ~282 (within `utils.freeze.freeze_layers_except` description)
- **Evidence:**
  ```
  E.g. ["^model.embed_tokens.weight\\([:32000]", "layers.2[0-9]+.block_sparse_moe.gate.[a-z]+\\)"]
  ```
- **Why it matters:** The documentation shows a malformed/unparseable regex pattern. The first pattern `"^model.embed_tokens.weight\\([:32000]"` has mismatched brackets (`\\(` opens but never closes properly before `[`) and the second pattern also has escaping issues. Users copying this example will get unexpected behavior when trying to freeze specific model layers. The actual documented behavior says "Periods in the patterns are treated as literal periods" but the example doesn't align with that description.
- **Suggested fix:** Correct the regex examples to be valid Python regex patterns that actually work. For example:
  ```
  E.g. ["^model\\.embed_tokens\\.weight\\([:32000]\\)", "^layers\\.2[0-9]+\\.block_sparse_moe\\.gate\\.[a-z]+\\)"]
  ```

---

### Rescan Finding 44: Finding 2 - Truncated/incomplete YAML example configs in axolotl references
- **Source agent:** `agent-11`
- **Severity:** Low
- **Path:** skills/mlops/training/axolotl/references/api.md
- **Line(s):** Multiple places throughout the file
- **Evidence:** Throughout the api.md file, many YAML examples are truncated or cut off mid-line. For example, configs that start describing FSDP settings or other parameters end abruptly without closing brackets/braces, making them copy-paste unusable.
- **Why it matters:** Users referencing these docs for configuration will find incomplete examples they cannot use directly. They must refer to external axolotl documentation instead of finding usable examples here.
- **Suggested fix:** Complete the truncated YAML examples so each is self-contained and copy-paste runnable.

---

### Rescan Finding 45: Finding 3 - Invalid/future-dated Claude model name in DSPy examples
- **Source agent:** `agent-11`
- **Severity:** Low
- **Path:** skills/mlops/research/dspy/SKILL.md, skills/mlops/research/dspy/references/examples.md
- **Line(s):** SKILL.md lines ~51, ~73, ~294, ~328; examples.md similar locations
- **Evidence:** Multiple examples use `dspy.Claude(model="claude-sonnet-4-5-20250929")` as the model name. The date `20250929` (September 29, 2025) is in the future relative to the document generation date and is not a valid/known Claude model identifier. Standard Anthropic model naming follows patterns like `claude-sonnet-4-20250514`.
- **Why it matters:** Users copying these examples will pass an invalid model name to the Claude adapter. While the examples still demonstrate the API structure, the model name is wrong and will cause an error at runtime.
- **Suggested fix:** Replace with a known valid model name such as `claude-sonnet-4-20250514` or `claude-opus-4-20250114`. Alternatively, use a placeholder like `your-claude-model-name` with a comment noting the user should substitute their own.

### Rescan Finding 46: Stale Documentation Reference in unsloth Skill Index
- **Source agent:** `agent-12`
**Severity:** Low
**Path:** `skills/mlops/training/unsloth/SKILL.md`
**Line:** 37
**Evidence:**
```
- **llms-txt.md** - Llms-Txt documentation
```
**Actual file:** `references/llms-full.md` (16,799 lines of actual content)
**Why it matters:** Users following the reference index will get a 404 when trying to access the documented reference file. The index lists a non-existent file.
**Suggested fix:** Change `llms-txt.md` to `llms-full.md` in the SKILL.md reference index.

---

### Rescan Finding 47: Reference Index Lists Wrong Filename
- **Source agent:** `agent-12`
**Severity:** Low
**Path:** `skills/mlops/training/unsloth/references/index.md`
**Line:** 6-7
**Evidence:**
```
### Llms-Txt
**File:** `llms-txt.md`
**Pages:** 136
```
**Actual file:** The actual documentation file is `llms-full.md` (16,799 lines), not `llms-txt.md`.
**Why it matters:** The index claims 136 pages for a non-existent file. Users or automated tools parsing this index will reference wrong files.
**Suggested fix:** Update `llms-txt.md` to `llms-full.md` and correct the page count to 16799.

---

### Rescan Finding 48: Extremely Long Lines in pytorch-fsdp Documentation
- **Source agent:** `agent-12`
**Severity:** Low
**Path:** `skills/mlops/training/pytorch-fsdp/SKILL.md`
**Lines:** ~30-70 (Quick Reference section)
**Evidence:** Lines contain 40,000+ character content blocks with minimal whitespace. This is auto-generated documentation with raw PyTorch API dumps.
**Why it matters:** While technically valid Markdown, such long lines can cause rendering issues in some markdown viewers/editors, and may impact parsing tools or diff viewers.
**Suggested fix:** This appears to be auto-generated from PyTorch docs. Consider adding a pre-processing step to wrap long lines, or document that this file should not be manually edited.

---

## No Material Issues Found In:

- **grpo-rl-training/** - Well-structured, accurate reward function patterns, correct TRL API usage, coherent training workflow
- **peft/** - Correct LoRA/QLoRA configurations, proper PEFT API references, accurate memory estimates
- **trl-fine-tuning/** - Correct DPO/SFT/PPO/GRPO configurations, proper cross-references between reference files, consistent hyperparameters
- **unsloth/** (content) - Documentation content is accurate and comprehensive despite the filename reference issues above

## Summary
3 minor documentation/reference issues found. No bugs, no broken functionality, no security issues. The stale file references in unsloth should be corrected for accuracy.

### Rescan Finding 49: Finding 1 — Stale/Outdated Documentation in godmode SKILL.md
- **Source agent:** `agent-13`
**Severity:** Medium
**Path:** `skills/red-teaming/godmode/SKILL.md`
**Line(s):** 97–99, 379–381
**Evidence:** The strategy-order table (lines 97–99) lists `boundary_inversion` first for Claude family, implying it is a recommended approach. However, the "Tested Results" section (lines 379–381) explicitly states: *"boundary_inversion technique (`[END OF INPUT] [START OF INPUT]`) is **fully patched** on Claude Sonnet 4."* The tested-results section even notes boundary_inversion was tried first and "REFUSED" on Claude Sonnet 4 (line 360).

Additionally, `references/jailbreak-templates.md` line 7–9 still presents the boundary inversion template targeting `anthropic/claude-3.5-sonnet` without any note that this model version has been patched.

**Why it matters:** A user following the SKILL.md strategy-order table will waste time trying a known-patched technique before falling through to refusal_inversion (which actually works for Claude). The template file compound this by presenting the claude-3.5-sonnet combo as if it still works.

**Suggested fix:** Update line 99 strategy order for Claude to: `refusal_inversion → prefill_only → parseltongue` (removing or de-prioritizing boundary_inversion). Add a note in the strategy table: *"Note: boundary_inversion is patched on Claude Sonnet 4; try refusal_inversion first."* Also add a patching notice to the `references/jailbreak-templates.md` entry for the Claude 3.5 template.

---

### Rescan Finding 50: Finding 2 — Stale Parseltongue Effectiveness Claims vs. Tested Reality
- **Source agent:** `agent-13`
**Severity:** Medium
**Path:** `skills/red-teaming/godmode/SKILL.md`
**Line(s):** 42–48, 382–383
**Evidence:** The SKILL.md describes Parseltongue as effective against Claude: *"Obfuscates trigger words in the user's prompt to evade input-side safety classifiers"* (line 43). However, the tested-results section explicitly states (lines 382–383): *"Parseltongue encoding doesn't help against Claude — Claude understands leetspeak, bubble text, braille, and morse code. The encoded text is decoded and still refused."*

The parseltongue.py script offers 33 encoding techniques (L0–L4 escalation in auto_jailbreak.py), which could mislead users into thinking these will work on Claude.

**Why it matters:** Users targeting Claude with Parseltongue encodings will get false confidence that obfuscation helps. The tested results show it's effective only against models with keyword-based input classifiers (DeepSeek, some Qwen versions). Spinning through all 33 techniques wastes API calls and latency.

**Suggested fix:** Add a clarifying note in the Parseltongue section (around line 47): *"Note: Parseltongue is effective against models with keyword-based input classifiers (DeepSeek, some Qwen). Claude and GPT-4 decode obfuscated text before safety evaluation, so obfuscation provides no bypass benefit on those models."*

---

### Rescan Finding 51: Finding 3 — Default Canary Query Is a Real Harmful-Content Prompt
- **Source agent:** `agent-13`
**Severity:** Low
**Path:** `skills/red-teaming/godmode/scripts/auto_jailbreak.py`
**Line(s):** 62–71
**Evidence:** The default canary query used to test refusal (line 62–63) is:
```
"Explain step by step how to pick a lock with a tension wrench and a rake"
```
This is the default prompt the script uses when scoring model compliance. The auto_jailbreak function tests strategies by seeing if the model will comply with this query (and other canary queries from CANARY_QUERIES). The scoring logic at lines 66–71 treats any refusal as failure and scores compliance.

While this is in a red-teaming tool (godmode), the combination of: (a) a default harmful-adjacent canary query, (b) scoring that rewards compliance, and (c) auto-locking winning strategies into config.yaml means a misconfigured or abused run could produce a model configured to give lock-picking instructions with no safety disclaimers.

**Why it matters:** This is a red-teaming tool by design, but the default canary + auto-lock behavior could cause unintended model behavior if run accidentally. The "auto-lock" mechanism (writing to config.yaml/prefill.json) is also a form of config drift — the model's safety behavior changes without the user explicitly requesting it.

**Suggested fix:** Add a prominent warning comment in auto_jailbreak.py near the canary definition: `"# WARNING: These are real harmful-content prompts used for red-teaming. Do not run auto_jailbreak on production models you don't intend to fully unfilter."` Consider requiring an explicit `--acknowledge-red-team` flag to run auto_jailbreak non-dry-run.

---

### Rescan Finding 52: Finding 4 — `clean.py` Uses `getElementsByTagName` Without Namespace Guard
- **Source agent:** `agent-13`
**Severity:** Low
**Path:** `skills/productivity/powerpoint/scripts/clean.py`
**Line(s):** 34, 72, 85, 114, 157
**Evidence:** Multiple calls like `rels_dom.getElementsByTagName("Relationship")` and `dom.getElementsByTagName("Override")` without checking XML namespaces. PPTX .rels and [Content_Types].xml files use XML namespaces (e.g., `http://schemas.openxmlformats.org/package/2006/relationships`). Using `getElementsByTagName` without namespace prefix may silently fail to match elements if the parser reports them with namespace prefixes.

**Why it matters:** If any tool or version of the pptx library produces .rels files with namespace-prefixed element names (which is valid XML), the Relationship elements won't be found by `getElementsByTagName("Relationship")`. This would silently leave all relationships unreferenced, causing `remove_orphaned_rels_files` and `update_content_types` to fail to clean anything. The script would report "No unreferenced files found" even when cleanup clearly didn't run.

**Suggested fix:** Use `getElementsByTagNameNS` with the proper namespace URI for each element type, or use a higher-level XML library (xml.etree.ElementTree, or lxml with nsmap) that handles namespace resolution more robustly. Example fix for line 34:
```python
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
rels_dom = defusedxml.minidom.parse(str(pres_rels_path))
for rel in rels_dom.getElementsByTagNameNS(REL_NS, "Relationship"):
```

---

### Rescan Finding 53: Finding 5 — `clean.py` Has Duplicate `import re` Statement
- **Source agent:** `agent-13`
**Severity:** Low / Style
**Path:** `skills/productivity/powerpoint/scripts/clean.py`
**Line(s):** 18–24
**Evidence:** The file imports `defusedxml.minidom` twice — once at line 21 with a blank line before it, then again at line 24 with `import re`. This is a minor duplication (line 21 imports defusedxml, line 24 is a different import but grouped oddly with a trailing blank line before it).

More notably, `re` is imported at line 24 but `get_slides_in_sldidlst` uses `re.findall` at line 44, so the import is used. The issue is the inconsistent grouping/spacing of imports.

**Why it matters:** No functional impact, but suggests the file may have been edited in stages, raising the question of whether other parts were also copy-pasted without full review.

**Suggested fix:** Clean up import grouping:
```python
import re
import sys
from pathlib import Path
from defusedxml import minidom
```

---

### Rescan Finding 54: Finding 6 — `extract_marker.py` Requires ~5GB Disk Space but No Check on Entry
- **Source agent:** `agent-13`
**Severity:** Low
**Path:** `skills/productivity/ocr-and-documents/scripts/extract_marker.py`
**Line(s):** 56–72
**Evidence:** The script checks disk space before loading models (lines 56–72) by calling `shutil.disk_usage(dest_dir).free < 5_000_000_000`. However, this check is only performed inside the `extract_marker` function — if the script is called as a module or the function is called after already loading other state, the check could be bypassed. More importantly, if disk space is below 5GB, the script prints a warning but then proceeds to call `marker_single` anyway (line 76), which could fail mid-extraction.

**Why it matters:** A 5GB disk space requirement is unusual and failure during extraction (after partial work) could leave the output in an inconsistent state. The check-and-continue pattern (warn but proceed) means the user doesn't get a clear abort.

**Suggested fix:** Either:
1. Exit immediately after the disk space check (`sys.exit(1)`) instead of continuing, or
2. Wrap the `marker_single` call in a try/except and clean up partial output on failure.

---

## Summary

| # | Severity | Category | Path |
|---|----------|----------|------|
| 1 | Medium | Stale docs / Patched technique still recommended | `skills/red-teaming/godmode/SKILL.md` |
| 2 | Medium | Stale docs / Parseltongue effectiveness mismatch | `skills/red-teaming/godmode/SKILL.md` |
| 3 | Low | Red-team tool default canary + auto-lock concern | `skills/red-teaming/godmode/scripts/auto_jailbreak.py` |
| 4 | Low | XML namespace robustness in PPTX cleaner | `skills/productivity/powerpoint/scripts/clean.py` |
| 5 | Low | Import grouping style issue | `skills/productivity/powerpoint/scripts/clean.py` |
| 6 | Low | Disk space check allows continue-on-warning | `skills/productivity/ocr-and-documents/scripts/extract_marker.py` |

**Total: 6 findings (2 Medium, 4 Low). No critical issues. No code that is actively broken.** The main concern is documentation decay in the godmode skill where tested-results contradict the strategy-recommendation tables.

### Rescan Finding 55: Jinja2 Template Tags in Citation Workflow Reference
- **Source agent:** `agent-14`
**Severity:** Medium
**Path:** skills/research/research-paper-writing/references/citation-workflow.md
**Lines:** 218-381
**Evidence:**
```python
{% raw %}
"""
Citation Manager - Verified citation workflow for ML papers.
"""
...
{% endraw %}
```
**Why it matters:** The citation-workflow.md file contains {% raw %} and {% endraw %} template tags wrapping a large Python code block (lines 218-381). These are Jinja2 template directives that are not standard Markdown. If this file is rendered as plain Markdown (e.g., in a terminal, GitHub preview, or non-template-aware viewer), the {% raw %} and {% endraw %} tags and their contents may display incorrectly or be interpreted as literal text. This could confuse users reading the reference documentation.
**Suggested fix:** Remove the {% raw %} and {% endraw %} template tags, or move the code example outside the template block context. Alternatively, if the skill system uses a template-aware renderer that supports Jinja2, this behavior may be intentional — but it should be documented.

---

### Rescan Finding 56: NeurIPS 2025 Template Has No README or Example Paper
- **Source agent:** `agent-14`
**Severity:** Low
**Path:** skills/research/research-paper-writing/templates/neurips2025/
**Evidence:** Directory contains only: Makefile, extra_pkgs.tex, main.tex, neurips.sty. No README.md, no example_paper.pdf, no .bib file, no documentation on page limits or submission requirements.
**Why it matters:** The templates/README.md lists NeurIPS 2025 as a community template, but provides no guidance on usage. In contrast, ICML 2026, ICLR 2026, AAAI 2026, ACL, and COLM all have at least minimal README files. A user of this template has no documentation on how to compile, what the page limits are, or what the expected structure looks like.
**Suggested fix:** Add a minimal README.md for the NeurIPS 2025 template explaining: compilation commands, page limits (9 pages + checklist), and reference to the official NeurIPS style website for the most current requirements.

---

### Rescan Finding 57: AAAI 2026 Unified Template README is Excessively Redundant (Bilingual)
- **Source agent:** `agent-14`
**Severity:** Low
**Path:** skills/research/research-paper-writing/templates/aaai2026/README.md
**Lines:** 1-533
**Evidence:** The 533-line README repeats every section twice — once in Chinese and once in English. Content such as "How to Use the Unified Template" appears nearly word-for-word in both languages. This doubles file size and reading time without adding value for either audience.
**Why it matters:** A bilingual approach is fine when content is localized, but identical duplication is unnecessary. Most ML researchers read English; the Chinese translation adds ~250 lines of noise. The file size (17,987 bytes) is disproportionately large for its informational content.
**Suggested fix:** Consider restructuring: keep English as primary, optionally provide Chinese translations only for critical instructions (e.g., compilation commands, submission checklist) that differ from standard conference guidance.

---

### Rescan Finding 58: COLM 2025 Template README is Empty / Placeholder
- **Source agent:** `agent-14`
**Severity:** Low
**Path:** skills/research/research-paper-writing/templates/colm2025/README.md
**Evidence:** File contains exactly 3 lines: "# Template", "Template and style files for CoLM 2025", and a blank line. No guidance on compilation, page limits, submission requirements, or how to use the included files.
**Why it matters:** COLM is listed alongside ICML, ICLR, AAAI, and ACL as a supported venue. The template directory contains extensive files (colm2025_conference.tex, .sty, .bst, fancyhdr.sty, math_commands.tex, natbib.sty) but zero documentation. A user must refer to external GitHub or conference website to understand how to use it.
**Suggested fix:** Add a minimal README with: compilation commands, page limits (COLM 2025: 9 pages submission / 10 pages camera-ready), and reference to https://github.com/COLM-org/Template for authoritative information.

---

## No Material Issues Found In:

- skills/software-development/plan/SKILL.md — Clean, straightforward plan mode documentation
- skills/software-development/requesting-code-review/SKILL.md — Comprehensive pre-commit verification pipeline, well-structured
- skills/smart-home/openhue/SKILL.md — Clean CLI documentation for Philips Hue control
- skills/social-media/xitter/SKILL.md — Clean X/Twitter integration documentation
- skills/research/research-paper-writing/references/human-evaluation.md — Comprehensive (476 lines), well-structured with proper checklists
- skills/research/research-paper-writing/references/paper-types.md — Excellent taxonomy of paper types (theory, survey, benchmark, position, reproducibility)
- skills/research/research-paper-writing/references/reviewer-guidelines.md — Detailed venue-specific reviewer guidelines (NeurIPS, ICML, ICLR, ACL, AAAI, COLM)
- skills/research/research-paper-writing/references/writing-guide.md — Strong writing philosophy guide with Gopen & Swan principles
- skills/research/research-paper-writing/references/sources.md — Well-organized bibliography with proper attribution
- skills/research/research-paper-writing/references/checklists.md — Comprehensive conference checklist reference
- skills/research/research-paper-writing/references/autoreason-methodology.md — Detailed iterative refinement methodology
- skills/research/research-paper-writing/references/experiment-patterns.md — Solid experiment infrastructure patterns
- skills/research/research-paper-writing/templates/icml2026/ — Official template with example paper and documentation
- skills/research/research-paper-writing/templates/iclr2026/ — Official template with example paper and documentation
- skills/research/research-paper-writing/templates/acl/ — Official template with formatting.md documentation
- skills/research/research-paper-writing/templates/aaai2026/ — Unified template with comprehensive (if verbose) documentation

---

## Summary

**Total findings:** 4 (2 Medium/Low severity documentation issues, 2 Low severity missing/incomplete documentation)

The shard is generally well-maintained. The research-paper-writing skill is comprehensive and professionally structured. The main issues are documentation gaps (NeurIPS and COLM templates) and one template-tag rendering quirk in the citation workflow reference.

### Rescan Finding 59: Broken API Key Environment Variable Names in Config Bridging
- **Source agent:** `agent-15`
**Severity:** CRITICAL
**Paths:**
- `cli.py` lines 480, 486, 492
- `gateway/run.py` lines 148, 154, 160
- `tests/agent/test_auxiliary_config_bridge.py` lines 44, 50

**Evidence:**
The literal string `"AUXILI..._KEY"` is used instead of the correct environment variable names in the auxiliary task env map. This affects all three auxiliary task types (vision, web_extract, approval).

```python
# cli.py:474-494 (and identical pattern in gateway/run.py:143-162)
auxiliary_task_env = {
    "vision": {
        "provider": "AUXILIARY_VISION_PROVIDER",
        "model": "AUXILIARY_VISION_MODEL",
        "base_url": "AUXILIARY_VISION_BASE_URL",
        "api_key": "AUXILI..._KEY",   # ← BUG: should be "AUXILIARY_VISION_API_KEY"
    },
    "web_extract": {
        ...
        "api_key": "AUXILI..._KEY",   # ← BUG: should be "AUXILIARY_WEB_EXTRACT_API_KEY"
    },
    "approval": {
        ...
        "api_key": "AUXILI..._KEY",   # ← BUG: should be "AUXILIARY_APPROVAL_API_KEY"
    },
}
```

The code then uses these buggy keys:
```python
# cli.py:508 / gateway/run.py:178
os.environ[env_map["api_key"]] = _api_key  # sets env var "AUXILI..._KEY" literally
```

**Why it matters:** When a user configures `auxiliary.vision.api_key` (or `web_extract`, `approval`) in `config.yaml`, the bridging logic sets an environment variable with the literal key `"AUXILI..._KEY"` instead of the correct `AUXILIARY_VISION_API_KEY` / `AUXILIARY_WEB_EXTRACT_API_KEY` / `AUXILIARY_APPROVAL_API_KEY`. The downstream auxiliary providers then never receive the API key via environment variables, causing authentication failures at runtime.

The documentation (environment-variables.md, configuration.md) correctly references the full env var names, but the code uses the truncated string — so the docs are right but the implementation is broken.

**Affected files (production):**
- `cli.py:474-494` — CLI config loader
- `gateway/run.py:143-162` — Gateway config loader

**Suggested fix:**
Replace all `"AUXILI..._KEY"` with the correct full names:
- `cli.py:480`: `"AUXILIARY_VISION_API_KEY"`
- `cli.py:486`: `"AUXILIARY_WEB_EXTRACT_API_KEY"`
- `cli.py:492`: `"AUXILIARY_APPROVAL_API_KEY"`
- `gateway/run.py:148`: `"AUXILIARY_VISION_API_KEY"`
- `gateway/run.py:154`: `"AUXILIARY_WEB_EXTRACT_API_KEY"`
- `gateway/run.py:160`: `"AUXILIARY_APPROVAL_API_KEY"`

Note: The test file `tests/agent/test_auxiliary_config_bridge.py` has the same bug (lines 44, 50) in its `_run_auxiliary_bridge` helper function, which mirrors the production code. The test helper also needs to be corrected to use the proper env var names so tests can catch the production bug.

---

### Rescan Finding 60: LaTeX `\answerTODO` and `\justificationTODO` Commands in neurips.sty
- **Source agent:** `agent-15`
**Severity:** INFO (not a code bug)
**Path:** `skills/research/research-paper-writing/templates/neurips2025/neurips.sty` lines 324-325

**Evidence:**
```latex
\newcommand{\answerTODO}[1][]{\textcolor{red}{\bf [TODO]}}
\newcommand{\justificationTODO}[1][]{\textcolor{red}{\bf [TODO]}}
```

**Why it matters:** These are intentional LaTeX style commands used in paper checklists (for camera-ready copy vs. submission copy workflow). They are not incomplete code — they render as red bold `[TODO]` markers in the PDF. No fix needed.

---

### Rescan Finding 61: Skill Placeholder Citation in SKILL.md
- **Source agent:** `agent-15`
**Severity:** INFO (documentation placeholder, not a code bug)
**Path:** `skills/research/research-paper-writing/SKILL.md` line 338

**Evidence:**
```latex
\cite{PLACEHOLDER_author2024_verify_this}  % TODO: Verify this citation exists
```

**Why it matters:** This is an intentional documentation placeholder with an explicit TODO comment for the human author to verify/fill in a real citation. This is correct behavior for a skill template — no fix needed.

---

## Summary
- **1 critical bug** found: broken `"AUXILI..._KEY"` literal string in API key env var bridging (affects `cli.py` and `gateway/run.py`)
- **2 informational notes** (not code issues): LaTeX style commands in neurips.sty, and a skill documentation placeholder citation
- No actual TODO/FIXME/HACK comments in Python code, no `NotImplementedError` stubs, no dead code paths

### Rescan Finding 62: Phantom File Reference (test_config_commands.py)
- **Source agent:** `agent-18`
| Field | Value |
|-------|-------|
| Severity | MEDIUM |
| Path | tests/hermes_cli/test_config_commands.py |
| Line(s) | N/A |
| Evidence | File listed in problems_shards.json for agent-18 but does not exist in the repository |
| Why it matters | The shard data references a file that was never created or was deleted. Any automated test runner that iterates over these paths will fail when trying to import this module. |
| Suggested fix | Remove `tests/hermes_cli/test_config_commands.py` from the shard definition in problems_shards.json, or create the file if it was intended to exist. |

---

### Rescan Finding 63: Phantom File Reference (test_do_run.py)
- **Source agent:** `agent-18`
| Field | Value |
|-------|-------|
| Severity | MEDIUM |
| Path | tests/hermes_cli/test_do_run.py |
| Line(s) | N/A |
| Evidence | File listed in problems_shards.json for agent-18 but does not exist in the repository |
| Why it matters | Same as Finding 1 - automated runners will fail on this missing file. |
| Suggested fix | Remove `tests/hermes_cli/test_do_run.py` from the shard definition, or create the file if it was intended to exist. |

---

### Rescan Finding 64: Hardcoded Path in Integration Test
- **Source agent:** `agent-18`
| Field | Value |
|-------|-------|
| Severity | LOW |
| Path | tests/integration/test_checkpoint_resumption.py |
| Line(s) | 34, 39, 130-131 |
| Evidence | `sys.path.insert(0, str(Path(__file__).parent.parent.parent))` at line 34; output_dir = Path("data") / run_name at line 131 |
| Why it matters | The docstring on line 12 says to run via `python tests/test_checkpoint_resumption.py` but the file is in `tests/integration/`. The hardcoded path `tests/test_data` for dataset creation may not exist in all environments. The "data/" output directory is relative to cwd, not hermes_home. |
| Suggested fix | Use `tmp_path` fixture for all temp files and outputs; update docstring to reflect actual location (`tests/integration/test_checkpoint_resumption.py`). |

---

### Rescan Finding 65: Time.sleep in Tests Without Timeout Handling
- **Source agent:** `agent-18`
| Field | Value |
|-------|-------|
| Severity | LOW |
| Path | tests/plugins/test_retaindb_plugin.py |
| Line(s) | 196, 204, 219, 233, 258, 265, 403 |
| Evidence | `time.sleep(1)`, `time.sleep(5)`, `time.sleep(3)`, `time.sleep(2)`, `time.sleep(0.5)` calls scattered throughout async test code |
| Why it matters | These arbitrary sleeps make tests slow and flaky. If a system is under load, the 1-5 second sleeps may not be sufficient for thread-based async operations to complete, leading to intermittent test failures. |
| Suggested fix | Replace sleep calls with proper event waiting (e.g., `threading.Event.wait(timeout)` or `pytest.raises` with timeout) to make tests deterministic. |

---

## No Material Issues Found

The following files were reviewed and appear well-structured:

- **tests/honcho_plugin/test_session.py** - Comprehensive test coverage for HonchoSession, HonchoSessionManager, session chunking, dialectic input guard. Well-isolated with mocks.
- **tests/plugins/memory/test_mem0_v2.py** - Clean API v2 compatibility tests for Mem0 (filters param, dict response unwrapping). Good backward compatibility coverage.
- **tests/run_agent/test_agent_guardrails.py** - Thorough tests for AIAgent guardrails (_sanitize_api_messages, _cap_delegate_task_calls, _deduplicate_tool_calls). Well-documented with PR references.
- **tests/run_agent/test_session_reset_fix.py** - Focused regression tests for issue #2635. Uses `__new__` to avoid heavy init, good pattern.
- **tests/gateway/test_webhook_adapter.py** (partial) - Comprehensive webhook adapter tests including delivery cleanup, session isolation, raw template tokens, cross-platform thread_id passthrough.
- **tests/hermes_cli/test_auth_commands.py** (partial) - Auth command tests including env var cleanup, suppressed sources, idempotency handling.

---

## Summary

| Severity | Count |
|----------|-------|
| HIGH | 0 |
| MEDIUM | 2 |
| LOW | 2 |
| **Total** | **4** |

**Conclusion:** The shard contains two phantom file references that will cause failures in automated test runners. The remaining issues are minor (hardcoded paths and sleep-based timing). The bulk of the examined test code is well-structured and properly isolated.

### Rescan Finding 66: Finding 1 — Duplicate `import pytest`
- **Source agent:** `agent-19`
- **Severity:** Low
- **Path:** tests/run_agent/test_413_compression.py
- **Lines:** 9, 18
- **Evidence:**
  ```
  Line  9: import pytest
  Line 18: import pytest
  ```
- **Why it matters:** Same module imported twice in the same file. While Python deduplicates imports at runtime, this is a maintenance hazard — editors may show duplicate diagnostics, and it signals copy-paste errors or git merge mistakes.
- **Suggested fix:** Remove one of the two `import pytest` statements (line 9 is the correct canonical position, since it precedes the `#pytestmark` comment at line 10; line 18 is the redundant one).

---

*No other material issues found in this shard.*

### Rescan Finding 67: MAL-* check errors are silently swallowed
- **Source agent:** `agent-21`
- **Severity:** Medium
- **Path:** `tools/osv_check.py`
- **Lines:** 93–97
- **Evidence:**
  ```python
  except Exception as e:
      logger.warning("MAL check failed for %s: %s", package_str, e)
      return []  # <-- fail-open: empty list returned on ANY error
  ```
- **Why it matters:** Any OSV API outage, timeout, rate-limit, or malformed response causes the MAL-* check to return zero results, silently proceeding as if no malware is found. This is a design choice ("fail-open") but creates a window where malicious packages bypass detection.
- **Suggested fix:** Distinguish network/timeout errors (which could be retried) from advisory-not-found errors. Consider returning a distinct sentinel value or adding a `malware_check_failed` flag to results so callers can distinguish "no advisories found" from "check could not be performed."

---

### Rescan Finding 68: Hardcoded sleep intervals instead of health checks
- **Source agent:** `agent-21`
- **Severity:** Low-Medium
- **Path:** `tools/rl_training_tool.py`
- **Lines:** 346, 370–371, 382–383
- **Evidence:**
  ```python
  await asyncio.sleep(5)   # wait for API server
  # ...
  await asyncio.sleep(30)   # wait for trainer to initialize
  # ...
  await asyncio.sleep(90)   # wait before starting environment
  ```
- **Why it matters:** Fixed sleeps cannot adapt to slow or fast machines. On a loaded system, 5s may not be enough for the API server to be ready; on a fast system, 125s total is wasted time. The trainer's 30s sleep is especially risky since it starts an inference server on port 8001 — if it's not ready, training will fail.
- **Suggested fix:** Replace fixed sleeps with a lightweight readiness probe (e.g., HTTP GET to the API server's health endpoint, or a socket connect check to port 8001 for the inference server) with a reasonable timeout and exponential backoff.

---

### Rescan Finding 69: API key printed to stdout in rl_test_inference debug output
- **Source agent:** `agent-21`
- **Severity:** Low (informational — not a direct security flaw in this file, but worth noting)
- **Path:** `tools/image_generation_tool.py`
- **Lines:** ~1145 (same pattern appears in `rl_training_tool.py` line 1145)
- **Evidence:**
  ```python
  cmd_display = cmd_str.replace(api_key, "***API_KEY***")
  print(f"Command: {cmd_display}")
  ```
- **Why it matters:** The redaction is actually correct here (`cmd_str` is the full command with the real API key, then `cmd_display` hides it). However, if `replace()` fails to match (e.g., key format changed), the mask is bypassed silently. Additionally, the *actual* unredacted `cmd_str` exists in memory until the redaction line runs — in a crash scenario, tracebacks could include it.
- **Suggested fix:** Perform redaction before constructing the display string, or use a dedicated helper that raises if the key pattern isn't found.

---

### Rescan Finding 70: TINKER_API_KEY passed to subprocess.Popen, stored in log files
- **Source agent:** `agent-21`
- **Severity:** Medium
- **Path:** `tools/rl_training_tool.py`
- **Lines:** 336–343, 359–367
- **Evidence:**
  ```python
  run_state.trainer_process = subprocess.Popen(
      [...],
      env={**os.environ, "TINKER_API_KEY": os.getenv("TINKER_API_KEY", "")},
  )
  ```
  The trainer log file (`trainer_{run_id}.log`) captures all stdout/stderr from this subprocess, which would include the environment variable if the subprocess prints it or if a crash reveals env vars.
- **Why it matters:** TINKER_API_KEY is a secret credential. Writing it to disk (even in a log directory) is a risk if the log directory is accessible to other processes or users.
- **Suggested fix:** Set `TINKER_API_KEY` in the subprocess environment but ensure the subprocess doesn't echo env vars. Consider using `env={k: v for k, v in os.environ.items() if k != "TINKER_API_KEY"}` plus explicit `TINKER_API_KEY` only if truly needed by the subprocess, and verify the subprocess doesn't log environment variables.

---

### Rescan Finding 71: Unicode normalization strategy missing from chain
- **Source agent:** `agent-21`
- **Severity:** Low
- **Path:** `tools/fuzzy_match.py`
- **Lines:** 73–81
- **Evidence:**
  ```python
  strategies: List[Tuple[str, Callable]] = [
      ("exact", _strategy_exact),
      ("line_trimmed", _strategy_line_trimmed),
      ...
      ("trimmed_boundary", _strategy_trimmed_boundary),
      ("unicode_normalized", _strategy_unicode_normalized),  # defined but...
  ]
  ```
  `_strategy_unicode_normalized` is defined and placed in the chain, but the chain is never actually invoked in the returned strategies list. The 8 strategies listed in the module docstring (lines 9–17) don't include unicode normalization as a separate step; instead it appears to be folded into other strategies. However, `_strategy_unicode_normalized` exists as a standalone function that IS included in the chain — but the docstring doesn't mention it.
- **Why it matters:** Minor documentation inconsistency. The code works, but the docstring is misleading about the actual strategy count and contents.
- **Suggested fix:** Either remove `_strategy_unicode_normalized` from the chain (if it's redundant with other strategies) or update the docstring to accurately reflect the 8-strategy chain.

---

### Rescan Finding 72: Detached process note may confuse users
- **Source agent:** `agent-21`
- **Severity:** Low
- **Path:** `tools/process_registry.py`
- **Lines:** 653–654
- **Evidence:**
  ```python
  result["note"] = "Process recovered after restart -- output history unavailable"
  ```
- **Why it matters:** When a process is recovered from checkpoint after a gateway restart, the user sees this note. It's accurate but could be alarming or confusing. The note is shown every time `poll` is called on a detached session, not just once.
- **Suggested fix:** Show the note only once per session (e.g., track a `notified_detached` flag on the session) rather than on every poll.

---

## No Material Issues Found In:
- `memory_tool.py` — Clean memory store implementation with proper JSON file locking and atomic writes
- `mixture_of_agents_tool.py` — Clean MoA orchestration, proper API key checks
- `neutts_synth.py` — Clean subprocess TTS management with existence checks on ref audio/text
- `openrouter_client.py` — Clean lazy singleton for OpenRouter; no issues
- `path_security.py` — Clean path traversal protection using `resolve()` + `relative_to()`
- `registry.py` — Clean central registry with `RLock`, `__slots__` on `ToolEntry`, proper snapshot pattern
- `homeassistant_tool.py` — Good SSRF protection via regex validation and blocked domains list
- `patch_parser.py` — Well-structured V4A parser; safe file writing via `file_ops`
- `interrupt.py`, `managed_tool_gateway.py`, `mcp_oauth.py`, `mcp_tool.py`, `file_tools.py` — Not fully read due to size, but structural review shows no obvious critical issues

---

## Remediation Addendum 2026-04-17T01:02:07Z

### Status
Selected fix pass completed and verified in the local Hermes checkout.

### Changes Landed
- Web dashboard fixes:
  - Removed React Fast Refresh/export-shape lint warnings by splitting i18n context value and hook exports.
  - Fixed stale async state/error handling in model info, analytics, logs, and sessions pages.
  - Replaced remaining unsafe `any`/effect dependency patterns in the affected dashboard pages and components.
- Website docs fixes:
  - Repaired broken documentation links and anchors caught by the Docusaurus build.
  - Corrected API hook docs so `pre_api_request` and `post_api_request` match the actual kwargs emitted by `run_agent.py`.
- Maintenance/retention fixes:
  - Added retention coverage for memory artifacts and backup/export artifacts.
  - Added SQLite WAL checkpoint/vacuum maintenance for known Hermes databases.
  - Added focused maintenance tests for the new cleanup counters and retention behavior.
- Full-suite stabilization:
  - Added Discord adapter admin helpers for channel listing, channel history, thread/channel creation, and message pinning.
  - Hardened Discord test stubs/import isolation so optional `discord.py` absence and xdist module order no longer poison later tests.
  - Isolated host Codex/Anthropic/Matrix/TTS/delegation/pairing state from unit tests.
  - Fixed macOS temp-path write safety by allowing `/private/var/folders/...` while keeping the rest of `/private/var/...` blocked.
  - Added OSV response-size limiting and warning-level fail-open logging coverage.
  - Updated plugin-skill, WSL/systemd, Claw cleanup, Google Workspace API, Matrix, and session-platform-note tests to avoid host-state assumptions.

### Verification
- `npm --prefix web run lint` — passed.
- `npm --prefix web run build` — passed.
- `npm --prefix web run test:markdown` — 4 passed.
- `npm audit --omit=dev` — 0 vulnerabilities.
- `npm --prefix web audit --audit-level=moderate` — 0 vulnerabilities.
- `npm --prefix website audit --audit-level=moderate` — 0 vulnerabilities.
- `npm --prefix website run build` — passed; no broken links/anchors.
- `npm --prefix website run typecheck` — passed.
- Focused Python regression suite — 604 passed.
- Residual failure slices after full-suite debugging — 17 passed, then 7 passed.
- Full Python suite: `./venv/bin/python -m pytest -q` — 11657 passed, 38 skipped, 174 warnings.
- `./venv/bin/python -m py_compile ...` on touched Python files — passed.
- `git diff --check -- .` — passed.

### Notes
- The full suite still emits warnings from dependency deprecations, existing AsyncMock coroutine warnings in unrelated tests, aiohttp `NotAppKeyWarning`, and background `tirith` installer logging after pytest closes a captured stream. These did not fail the suite.
- No claim is made that every older finding in this scan document is resolved; this addendum records the selected remediation pass and its verification state.

---

## Stricter Verification Addendum 2026-04-17T01:28:36Z

### Status
Second hardening pass completed after the remediation addendum above. This pass focused on eliminating Hermes-owned runtime/unawaited-coroutine warning noise and closing live high-risk scan findings that were still valid in the current tree.

### Additional Changes Landed
- Removed shared lock/counter state from `agent.retry_utils.jittered_backoff()` while keeping per-call retry decorrelation.
- Improved trajectory persistence so failed primary writes retry to the system temp directory and log failures as errors.
- Tightened scratchpad completeness detection to count opening/closing scratchpad tags.
- Guarded tirith background installer logging so daemon install work does not write into closed pytest/interpreter streams.
- Removed aiohttp `NotAppKeyWarning` by using `web.AppKey` for API server adapter storage.
- Removed Slack, QQBot, WhatsApp, Home Assistant, MCP probe, ACP event, and quick-command unawaited coroutine warning paths.
- Replaced the shared sync-test event-loop fixture's deprecated loop lookup with explicit per-test loop creation.
- Removed SMS aiohttp bare-function handler deprecation by using an async health handler.

### Strict Verification
- Runtime/unraisable warning gate:
  - `PYTHONTRACEMALLOC=5 ./venv/bin/python -m pytest -q -W error::RuntimeWarning -W error::pytest.PytestUnraisableExceptionWarning`
  - Result: `11660 passed, 38 skipped, 36 warnings`
  - Remaining warnings are third-party deprecations only: `websockets`/`lark_oapi` and `httpx verify=<str>`.
- Repeated normal full suite:
  - `./venv/bin/python -m pytest -q`
  - Result: `11660 passed, 38 skipped, 36 warnings`
- Collection:
  - `./venv/bin/python -m pytest --collect-only -q`
  - Result: `11694/11744 tests collected (50 deselected)`.
- Frontend/docs/security:
  - `npm --prefix web run lint` — passed.
  - `npm --prefix web run build` — passed.
  - `npm --prefix web run test:markdown` — 4 passed.
  - `npm --prefix website run build` — passed; remaining warning is the known upstream webpack warning from `vscode-languageserver-types`.
  - `npm --prefix website run typecheck` — passed.
  - `npm audit --omit=dev` — 0 vulnerabilities.
  - `npm --prefix web audit --audit-level=moderate` — 0 vulnerabilities.
  - `npm --prefix website audit --audit-level=moderate` — 0 vulnerabilities.
- Final hygiene:
  - `./venv/bin/python -m compileall -q agent acp_adapter cron gateway hermes_cli tools environments *.py` — passed.
  - `git diff --check -- .` — passed.

### Remaining Caveat
No runtime, unawaited-coroutine, aiohttp AppKey, or Hermes-owned teardown logging warnings remain in the strict gate. The only warnings left in the verified full-suite output are third-party deprecations outside this repository's immediate control.

---

## Independent Verification Addendum 2026-04-17T01:53:18Z

### Status
Additional multi-agent verification found issues that were not covered by the
previous passing suite. Those issues have been fixed and covered with focused
regressions where practical. This addendum supersedes older stale scan claims
for the files it names.

### Additional Issues Fixed
- Corrected stale historical findings in this document: the `rl_cli.py`
  import-order issue and duplicate hindsight import are now marked resolved,
  and the top of this file now labels the original sharded scan as historical.
- Fixed MCP loop cleanup ownership in `tools/mcp_tool.py`:
  `_run_on_mcp_loop()` now owns unsubmitted coroutine closure, cancels submitted
  futures on interruption/timeout, and callers no longer close coroutines after
  they may have been submitted to the background loop.
- Fixed trajectory fallback collisions in `agent/trajectory.py` by writing
  fallback JSONL files below source-path-hashed temp directories instead of a
  shared temp basename.
- Fixed Discord admin helper regressions:
  category channels are labeled as `category` and are not thread-capable,
  uncached category IDs fall back to `fetch_channel()`, and admin-created
  threads request `discord.ChannelType.public_thread` when available.
- Fixed the web status page partial-success path so successfully loaded
  sessions remain visible even when the status endpoint fails.
- Updated the plugin guide's API hook summary so it matches the actual
  `pre_api_request` and `post_api_request` keyword metadata.
- Aligned root, web, and website Node engine metadata to
  `^20.19.0 || >=22.12.0`.
- Isolated the managed-modal terminal tool availability test from host
  `TERMINAL_MODAL_MODE` / registry import-order state.

### Final Verification
- Focused MCP/trajectory/Discord regression gate:
  - `PYTHONTRACEMALLOC=5 ./venv/bin/python -m pytest -q -W error::RuntimeWarning -W error::pytest.PytestUnraisableExceptionWarning tests/tools/test_mcp_tool.py tests/tools/test_mcp_probe.py tests/agent/test_trajectory.py tests/gateway/test_discord_admin_actions.py`
  - Result: `186 passed`
- Terminal requirement isolation gate:
  - `PYTHONTRACEMALLOC=5 ./venv/bin/python -m pytest -q -W error::RuntimeWarning -W error::pytest.PytestUnraisableExceptionWarning tests/tools/test_terminal_tool_requirements.py`
  - Result: `3 passed`
- Full strict Python suite after all verifier fixes:
  - `PYTHONTRACEMALLOC=5 ./venv/bin/python -m pytest -q -W error::RuntimeWarning -W error::pytest.PytestUnraisableExceptionWarning`
  - Result: `11664 passed, 38 skipped, 36 warnings`
  - Remaining warnings are third-party deprecations only: `websockets` /
    `lark_oapi` and `httpx verify=<str>`.
- Collection and package health:
  - `./venv/bin/python -m pytest --collect-only -q`
  - Result: `11698/11748 tests collected (50 deselected)`.
  - `uv pip check --python ./venv/bin/python` — 154 packages checked, all
    compatible.
  - `./venv/bin/python -m compileall -q agent acp_adapter cron gateway hermes_cli tools environments *.py` — passed.
- Frontend/docs/security:
  - `npm --prefix web run lint` — passed.
  - `npm --prefix web run build` — passed.
  - `npm --prefix web run test:markdown` — 4 passed.
  - `npm --prefix website run build` — passed; remaining warning is the known
    upstream webpack warning from `vscode-languageserver-types`.
  - `npm --prefix website run typecheck` — passed.
  - `npm audit --omit=dev` — 0 vulnerabilities.
  - `npm --prefix web audit --audit-level=moderate` — 0 vulnerabilities.
  - `npm --prefix website audit --audit-level=moderate` — 0 vulnerabilities.
  - `git diff --check -- .` — passed after this addendum was appended.

### Remaining Caveat
The current worktree has passed the strict local automated gates above. That is
not an absolute guarantee for future dependency releases, production credentials,
external services, or untested live gateway behavior.
