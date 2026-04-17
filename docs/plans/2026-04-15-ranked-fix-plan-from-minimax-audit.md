# Hermes MiniMax Audit Ranked Fix Plan

> **For Hermes:** Use subagent-driven-development skill to execute this plan batch-by-batch. Start with Batch A, then B, then C. Do not begin docs/skill cleanup until core runtime and security breakages are handled.

**Goal:** Turn the deduped MiniMax audit output into a concrete execution order so we can fix the real runtime/security/build breakages first and defer low-signal docs/skill/test noise until later.

**Architecture:** This plan is derived from `likely_fix_clusters.json` produced from the 25-agent convergence scan. Clusters were grouped into execution batches by path, severity, recurrence across passes, and whether the issue is a product runtime defect, a security risk, a build/integration breakage, or mostly documentation/test content drift.

**Tech Stack:** Hermes Python runtime, gateway/platform adapters, CLI, packaging scripts, docs/skills/test suite.

---

- Source run: `minimax-convergence-20260415T131609Z`
- Source clusters: `/Users/openclaw/.hermes/hermes-agent/tmp/minimax-convergence-20260415T131609Z/likely_fix_clusters.json`
- Canonical summary: `/Users/openclaw/.hermes/hermes-agent/tmp/minimax-convergence-20260415T131609Z/canonical_summary.md`
- Total likely-fix clusters: **139**

## Batch summary

- **Batch A — Core security / auth / exposure fixes: 11 clusters** | severity mix `{'CRITICAL': 2, 'HIGH': 9}`
- **Batch B — Core runtime breakages and product correctness: 37 clusters** | severity mix `{'CRITICAL': 3, 'HIGH': 29, 'INFO': 1, 'LOW': 2, 'MEDIUM': 2}`
- **Batch C — Packaging / integration / build pipeline breakages: 22 clusters** | severity mix `{'CRITICAL': 5, 'HIGH': 14, 'LOW': 1, 'MEDIUM': 2}`
- **Batch D — Core medium-severity correctness and infrastructure debt: 5 clusters** | severity mix `{'MEDIUM': 5}`
- **Batch E — Documentation / skill / content review: 11 clusters** | severity mix `{'HIGH': 2, 'LOW': 5, 'MEDIUM': 4}`
- **Batch F — Tests / docs / skill content / cleanup debt: 31 clusters** | severity mix `{'CRITICAL': 1, 'HIGH': 15, 'INFO': 1, 'LOW': 3, 'MEDIUM': 11}`
- **Batch G — Red-team / intentionally risky content review: 22 clusters** | severity mix `{'CRITICAL': 3, 'HIGH': 16, 'LOW': 2, 'MEDIUM': 1}`

## Execution order

1. **Batch A** — shipped security/auth/exposure issues in core runtime code
2. **Batch B** — hard runtime breakages and recurring core-product defects
3. **Batch C** — packaging/workflow/build/onboarding failures
4. **Batch D** — medium-severity core correctness/infrastructure debt
5. **Batch E** — documentation / skill / content review that is not clearly product-breaking
6. **Batch F** — tests/docs/skill cleanup and low-signal audit noise
7. **Batch G** — red-team / intentionally risky content review

## Batch A: Core security / auth / exposure fixes

Fix first — high-severity product security and auth issues in shipped runtime code.

### Task A.1: `agent/redact.py`

**Objective:** Resolve the 1 ranked cluster(s) in `agent/redact.py` before moving to the next file batch.

**Files:**
- Modify: `agent/redact.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `CRITICAL`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0032] severity=CRITICAL passes=2 lines=60-62 — Wrong regex pattern for secret env var detection

**Step 1: Investigate root cause**
- Read `agent/redact.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address agent/redact.py audit findings`

### Task A.2: `tools/process_registry.py`

**Objective:** Resolve the 1 ranked cluster(s) in `tools/process_registry.py` before moving to the next file batch.

**Files:**
- Modify: `tools/process_registry.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `CRITICAL`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0501] severity=CRITICAL passes=2 lines=507-559 — Missing interrupt check in background poller

**Step 1: Investigate root cause**
- Read `tools/process_registry.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tools/process_registry.py audit findings`

### Task A.3: `hermes_cli/auth.py`

**Objective:** Resolve the 2 ranked cluster(s) in `hermes_cli/auth.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_cli/auth.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `3` pass(es).

**Clusters in this task:**
- [CC0120] severity=HIGH passes=3 lines=58,625,654 — hermes_cli/auth.py hardcoded AUTH_STORE_VERSION prevents forward-compat migration
- [CC0121] severity=HIGH passes=1 lines=73-74,76-77 — OAuth placeholder secrets in provider registry

**Step 1: Investigate root cause**
- Read `hermes_cli/auth.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_cli/auth.py audit findings`

### Task A.4: `agent/credential_pool.py`

**Objective:** Resolve the 1 ranked cluster(s) in `agent/credential_pool.py` before moving to the next file batch.

**Files:**
- Modify: `agent/credential_pool.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0020] severity=HIGH passes=1 lines=183-186 — Duplicate priority assignment on first credential add

**Step 1: Investigate root cause**
- Read `agent/credential_pool.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address agent/credential_pool.py audit findings`

### Task A.5: `gateway/platforms/base.py`

**Objective:** Resolve the 1 ranked cluster(s) in `gateway/platforms/base.py` before moving to the next file batch.

**Files:**
- Modify: `gateway/platforms/base.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0079] severity=HIGH passes=1 lines=485-498 — BasePlatformAdapter._ssrf_redirect_guard reads body on redirect

**Step 1: Investigate root cause**
- Read `gateway/platforms/base.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address gateway/platforms/base.py audit findings`

### Task A.6: `hermes_cli/copilot_auth.py`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_cli/copilot_auth.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_cli/copilot_auth.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0130] severity=HIGH passes=1 lines=~120-135(resolve_copilot_tokenandcallers) — copilot_auth.py: GitHub token may appear in plaintext error messages

**Step 1: Investigate root cause**
- Read `hermes_cli/copilot_auth.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_cli/copilot_auth.py audit findings`

### Task A.7: `hermes_cli/runtime_provider.py`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_cli/runtime_provider.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_cli/runtime_provider.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0162] severity=HIGH passes=2 lines=585-586 — Nous agent_key falls back to access_token which returns 404 on inference endpoint

**Step 1: Investigate root cause**
- Read `hermes_cli/runtime_provider.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_cli/runtime_provider.py audit findings`

### Task A.8: `tools/approval.py`

**Objective:** Resolve the 1 ranked cluster(s) in `tools/approval.py` before moving to the next file batch.

**Files:**
- Modify: `tools/approval.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0472] severity=HIGH passes=1 lines=601-602,703-704 — Container backends bypass ALL security checks

**Step 1: Investigate root cause**
- Read `tools/approval.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tools/approval.py audit findings`

### Task A.9: `tools/mcp_tool.py`

**Objective:** Resolve the 1 ranked cluster(s) in `tools/mcp_tool.py` before moving to the next file batch.

**Files:**
- Modify: `tools/mcp_tool.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0491] severity=HIGH passes=2 lines=175-187 — MCP credential redaction regex has truncation artifact

**Step 1: Investigate root cause**
- Read `tools/mcp_tool.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tools/mcp_tool.py audit findings`

### Task A.10: `tools/terminal_tool.py`

**Objective:** Resolve the 1 ranked cluster(s) in `tools/terminal_tool.py` before moving to the next file batch.

**Files:**
- Modify: `tools/terminal_tool.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0542] severity=HIGH passes=1 lines=1498 — Broken import of non-existent agent.redact module

**Step 1: Investigate root cause**
- Read `tools/terminal_tool.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tools/terminal_tool.py audit findings`


## Batch B: Core runtime breakages and product correctness

Fix next — startup/import/runtime failures and repeatedly recurring core-product defects.

### Task B.1: `rl_cli.py`

**Objective:** Resolve the 2 ranked cluster(s) in `rl_cli.py` before moving to the next file batch.

**Files:**
- Modify: `rl_cli.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `CRITICAL`, max recurrence `5` pass(es).

**Clusters in this task:**
- [CC0226] severity=CRITICAL passes=5 lines=32 — rl_cli.py calls get_hermes_home before it is defined
- [CC0227] severity=HIGH passes=1 lines=35–39 — rl_cli.py imports env_loader after using it

**Step 1: Investigate root cause**
- Read `rl_cli.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address rl_cli.py audit findings`

### Task B.2: `environments/hermes_swe_env/default.yaml`

**Objective:** Resolve the 1 ranked cluster(s) in `environments/hermes_swe_env/default.yaml` before moving to the next file batch.

**Files:**
- Modify: `environments/hermes_swe_env/default.yaml`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `CRITICAL`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0064] severity=CRITICAL passes=1 lines=21-22 — steps_per_eval and total_steps swapped in SWE env YAML

**Step 1: Investigate root cause**
- Read `environments/hermes_swe_env/default.yaml` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address environments/hermes_swe_env/default.yaml audit findings`

### Task B.3: `hermes_state.py`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_state.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_state.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `CRITICAL`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0191] severity=CRITICAL passes=1 lines=1060-1085 — `search_messages` lock thrashing on context fetch loop

**Step 1: Investigate root cause**
- Read `hermes_state.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_state.py audit findings`

### Task B.4: `tools/rl_training_tool.py`

**Objective:** Resolve the 4 ranked cluster(s) in `tools/rl_training_tool.py` before moving to the next file batch.

**Files:**
- Modify: `tools/rl_training_tool.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0509] severity=HIGH passes=1 lines=253 — Import from uninstalled package atroposlib
- [CC0510] severity=HIGH passes=1 lines=47 — Wrong import path for hermes_constants
- [CC0511] severity=HIGH passes=1 lines=55-58 — Hardcoded path assumes tinker-atropos sibling directory
- [CC0514] severity=HIGH passes=1 lines=unknown(filecorrupted) — Corrupted file: rl_training_tool.py

**Step 1: Investigate root cause**
- Read `tools/rl_training_tool.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tools/rl_training_tool.py audit findings`

### Task B.5: `environments/hermes_swe_env/hermes_swe_env.py`

**Objective:** Resolve the 2 ranked cluster(s) in `environments/hermes_swe_env/hermes_swe_env.py` before moving to the next file batch.

**Files:**
- Modify: `environments/hermes_swe_env/hermes_swe_env.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0065] severity=HIGH passes=2 lines=179,187 — HermesSweEnv.compute_reward hardcodes /workspace path
- [CC0066] severity=HIGH passes=1 lines=195-209 — HermesSweEnv.evaluate is a no-op stub

**Step 1: Investigate root cause**
- Read `environments/hermes_swe_env/hermes_swe_env.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address environments/hermes_swe_env/hermes_swe_env.py audit findings`

### Task B.6: `tools/send_message_tool.py`

**Objective:** Resolve the 2 ranked cluster(s) in `tools/send_message_tool.py` before moving to the next file batch.

**Files:**
- Modify: `tools/send_message_tool.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0515] severity=HIGH passes=1 lines=107 — send_message_tool calls undefined tool_error
- [CC0516] severity=HIGH passes=1 lines=~1000-1011(mediadispatchin_send_to_platform) — send_message_tool uses send_voice for all audio

**Step 1: Investigate root cause**
- Read `tools/send_message_tool.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tools/send_message_tool.py audit findings`

### Task B.7: `agent/models_dev.py`

**Objective:** Resolve the 1 ranked cluster(s) in `agent/models_dev.py` before moving to the next file batch.

**Files:**
- Modify: `agent/models_dev.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0027] severity=HIGH passes=1 lines=~80-100(fetch_models_devfunction) — models_dev.py requests call has no timeout

**Step 1: Investigate root cause**
- Read `agent/models_dev.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address agent/models_dev.py audit findings`

### Task B.8: `cron/scheduler.py`

**Objective:** Resolve the 1 ranked cluster(s) in `cron/scheduler.py` before moving to the next file batch.

**Files:**
- Modify: `cron/scheduler.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0043] severity=HIGH passes=1 lines=111-112,141 — Platform name case inconsistency in cron delivery routing

**Step 1: Investigate root cause**
- Read `cron/scheduler.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address cron/scheduler.py audit findings`

### Task B.9: `gateway/platforms/base.py`

**Objective:** Resolve the 1 ranked cluster(s) in `gateway/platforms/base.py` before moving to the next file batch.

**Files:**
- Modify: `gateway/platforms/base.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0078] severity=HIGH passes=1 lines=388-399 — BasePlatformAdapter.is_network_accessible blocks localhost on all interfaces

**Step 1: Investigate root cause**
- Read `gateway/platforms/base.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address gateway/platforms/base.py audit findings`

### Task B.10: `gateway/platforms/slack.py`

**Objective:** Resolve the 1 ranked cluster(s) in `gateway/platforms/slack.py` before moving to the next file batch.

**Files:**
- Modify: `gateway/platforms/slack.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0082] severity=HIGH passes=1 lines=299 — SlackAdapter uses undefined `_BOT_TS_MAX` constant

**Step 1: Investigate root cause**
- Read `gateway/platforms/slack.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address gateway/platforms/slack.py audit findings`

### Task B.11: `gateway/platforms/telegram_network.py`

**Objective:** Resolve the 1 ranked cluster(s) in `gateway/platforms/telegram_network.py` before moving to the next file batch.

**Files:**
- Modify: `gateway/platforms/telegram_network.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0088] severity=HIGH passes=1 lines=245-246 — Missing retry for `asyncio.TimeoutError` in Telegram fallback transport

**Step 1: Investigate root cause**
- Read `gateway/platforms/telegram_network.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address gateway/platforms/telegram_network.py audit findings`

### Task B.12: `gateway/platforms/wecom_crypto.py`

**Objective:** Resolve the 1 ranked cluster(s) in `gateway/platforms/wecom_crypto.py` before moving to the next file batch.

**Files:**
- Modify: `gateway/platforms/wecom_crypto.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0095] severity=HIGH passes=1 lines=97,132 — Deprecated `default_backend()` call in wecom_crypto

**Step 1: Investigate root cause**
- Read `gateway/platforms/wecom_crypto.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address gateway/platforms/wecom_crypto.py audit findings`

### Task B.13: `gateway/platforms/whatsapp.py`

**Objective:** Resolve the 1 ranked cluster(s) in `gateway/platforms/whatsapp.py` before moving to the next file batch.

**Files:**
- Modify: `gateway/platforms/whatsapp.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0102] severity=HIGH passes=1 lines=355–390 — whatsapp.py unclosed file handle on error path

**Step 1: Investigate root cause**
- Read `gateway/platforms/whatsapp.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address gateway/platforms/whatsapp.py audit findings`

### Task B.14: `gateway/run.py`

**Objective:** Resolve the 1 ranked cluster(s) in `gateway/run.py` before moving to the next file batch.

**Files:**
- Modify: `gateway/run.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0107] severity=HIGH passes=1 lines=7683–7860(_run_agent_via_proxy) — Proxy mode uses unfiltered history length for transcript offset

**Step 1: Investigate root cause**
- Read `gateway/run.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address gateway/run.py audit findings`

### Task B.15: `hermes_cli/ (multiple)`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_cli/ (multiple)` before moving to the next file batch.

**Files:**
- Modify: `hermes_cli/ (multiple)`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0116] severity=HIGH passes=1 lines=n/a — Six files in shard scope do not exist

**Step 1: Investigate root cause**
- Read `hermes_cli/ (multiple)` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_cli/ (multiple) audit findings`

### Task B.16: `hermes_cli/cron.py`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_cli/cron.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_cli/cron.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0131] severity=HIGH passes=1 lines=9 — cron.py imports non-existent cron.jobs module

**Step 1: Investigate root cause**
- Read `hermes_cli/cron.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_cli/cron.py audit findings`

### Task B.17: `hermes_cli/runtime_provider.py`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_cli/runtime_provider.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_cli/runtime_provider.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0163] severity=HIGH passes=1 lines=727 — `_agent_key_is_usable` called at line 727 but not defined in runtime_provider.py scope

**Step 1: Investigate root cause**
- Read `hermes_cli/runtime_provider.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_cli/runtime_provider.py audit findings`

### Task B.18: `hermes_cli/setup.py`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_cli/setup.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_cli/setup.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `3` pass(es).

**Clusters in this task:**
- [CC0167] severity=HIGH passes=3 lines=1972-2018and2085-2091 — Duplicate `_setup_qqbot` function definition

**Step 1: Investigate root cause**
- Read `hermes_cli/setup.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_cli/setup.py audit findings`

### Task B.19: `hermes_cli/web_server.py`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_cli/web_server.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_cli/web_server.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0184] severity=HIGH passes=1 lines=496-497 — `search_sessions` endpoint creates new SessionDB per request

**Step 1: Investigate root cause**
- Read `hermes_cli/web_server.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_cli/web_server.py audit findings`

### Task B.20: `mini_swe_runner.py`

**Objective:** Resolve the 1 ranked cluster(s) in `mini_swe_runner.py` before moving to the next file batch.

**Files:**
- Modify: `mini_swe_runner.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0199] severity=HIGH passes=1 lines=149 — Hardcoded invalid model name as default

**Step 1: Investigate root cause**
- Read `mini_swe_runner.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address mini_swe_runner.py audit findings`

### Task B.21: `plugins/memory/hindsight/__init__.py`

**Objective:** Resolve the 1 ranked cluster(s) in `plugins/memory/hindsight/__init__.py` before moving to the next file batch.

**Files:**
- Modify: `plugins/memory/hindsight/__init__.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0214] severity=HIGH passes=1 lines=607-615 — Hindsight embedded daemon writes masked API key to profile env

**Step 1: Investigate root cause**
- Read `plugins/memory/hindsight/__init__.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address plugins/memory/hindsight/__init__.py audit findings`

### Task B.22: `plugins/memory/honcho/session.py`

**Objective:** Resolve the 1 ranked cluster(s) in `plugins/memory/honcho/session.py` before moving to the next file batch.

**Files:**
- Modify: `plugins/memory/honcho/session.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0219] severity=HIGH passes=1 lines=13 — honcho session.py imports get_honcho_client at module level

**Step 1: Investigate root cause**
- Read `plugins/memory/honcho/session.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address plugins/memory/honcho/session.py audit findings`

### Task B.23: `tools/skill_manager_tool.py`

**Objective:** Resolve the 1 ranked cluster(s) in `tools/skill_manager_tool.py` before moving to the next file batch.

**Files:**
- Modify: `tools/skill_manager_tool.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0521] severity=HIGH passes=1 lines=~200-300(writeaction),56-74(_security_scan_skill) — skill_manager_tool writes skills to disk before security scan completes

**Step 1: Investigate root cause**
- Read `tools/skill_manager_tool.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tools/skill_manager_tool.py audit findings`

### Task B.24: `tools/skill_manager_tool.py, tools/skills_guard.py`

**Objective:** Resolve the 1 ranked cluster(s) in `tools/skill_manager_tool.py, tools/skills_guard.py` before moving to the next file batch.

**Files:**
- Modify: `tools/skill_manager_tool.py, tools/skills_guard.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0522] severity=HIGH passes=1 lines=skill_manager_tool.py:56-74,skills_guard.py:642-676 — skills_guard scans agent-created skills with "ask" verdict but exception returns allow

**Step 1: Investigate root cause**
- Read `tools/skill_manager_tool.py, tools/skills_guard.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tools/skill_manager_tool.py, tools/skills_guard.py audit findings`

### Task B.25: `tools/terminal_tool.py`

**Objective:** Resolve the 1 ranked cluster(s) in `tools/terminal_tool.py` before moving to the next file batch.

**Files:**
- Modify: `tools/terminal_tool.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0540] severity=HIGH passes=1 lines=1350 — terminal_tool PTY mode lacks fallback on allocation failure

**Step 1: Investigate root cause**
- Read `tools/terminal_tool.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tools/terminal_tool.py audit findings`

### Task B.26: `tools/tirith_security.py`

**Objective:** Resolve the 1 ranked cluster(s) in `tools/tirith_security.py` before moving to the next file batch.

**Files:**
- Modify: `tools/tirith_security.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0547] severity=HIGH passes=1 lines=37 — tirith_security imports non-existent `is_tool_gateway_ready`

**Step 1: Investigate root cause**
- Read `tools/tirith_security.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tools/tirith_security.py audit findings`

### Task B.27: `environments/tool_context.py`

**Objective:** Resolve the 1 ranked cluster(s) in `environments/tool_context.py` before moving to the next file batch.

**Files:**
- Modify: `environments/tool_context.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `3` pass(es).

**Clusters in this task:**
- [CC0070] severity=MEDIUM passes=3 lines=357,373 — - web_search/web_extract missing task_id in ToolContext

**Step 1: Investigate root cause**
- Read `environments/tool_context.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address environments/tool_context.py audit findings`

### Task B.28: `hermes_cli/model_normalize.py`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_cli/model_normalize.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_cli/model_normalize.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `3` pass(es).

**Clusters in this task:**
- [CC0142] severity=MEDIUM passes=3 lines=54,58 — Duplicate dict key in _VENDOR_PREFIXES

**Step 1: Investigate root cause**
- Read `hermes_cli/model_normalize.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_cli/model_normalize.py audit findings`

### Task B.29: `hermes_cli/logs.py`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_cli/logs.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_cli/logs.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `LOW`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0137] severity=LOW passes=2 lines=~100-200(estimated) — - logs.py regex timestamp pattern misses microseconds

**Step 1: Investigate root cause**
- Read `hermes_cli/logs.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_cli/logs.py audit findings`

### Task B.30: `hermes_cli/providers.py`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_cli/providers.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_cli/providers.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `LOW`, max recurrence `4` pass(es).

**Clusters in this task:**
- [CC0159] severity=LOW passes=4 lines=295 — TODO in providers.py for unimplemented Phase 4 user-defined providers feature

**Step 1: Investigate root cause**
- Read `hermes_cli/providers.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_cli/providers.py audit findings`

### Task B.31: `environments/patches.py`

**Objective:** Resolve the 1 ranked cluster(s) in `environments/patches.py` before moving to the next file batch.

**Files:**
- Modify: `environments/patches.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `INFO`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0067] severity=INFO passes=2 lines=1-35 — environments/patches.py is a no-op stub with dead docstring

**Step 1: Investigate root cause**
- Read `environments/patches.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address environments/patches.py audit findings`


## Batch C: Packaging / integration / build pipeline breakages

Then fix installer, workflow, script, website, and packaging failures that break deployment or onboarding.

### Task C.1: `scripts/hermes-gateway`

**Objective:** Resolve the 2 ranked cluster(s) in `scripts/hermes-gateway` before moving to the next file batch.

**Files:**
- Modify: `scripts/hermes-gateway`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `CRITICAL`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0239] severity=CRITICAL passes=1 lines=297 — hermes-gateway imports non-existent gateway.run module
- [CC0240] severity=HIGH passes=1 lines=38 — hermes-gateway imports non-existent dotenv package

**Step 1: Investigate root cause**
- Read `scripts/hermes-gateway` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address scripts/hermes-gateway audit findings`

### Task C.2: `scripts/whatsapp-bridge/bridge.js`

**Objective:** Resolve the 2 ranked cluster(s) in `scripts/whatsapp-bridge/bridge.js` before moving to the next file batch.

**Files:**
- Modify: `scripts/whatsapp-bridge/bridge.js`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `CRITICAL`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0258] severity=CRITICAL passes=2 lines=559,368-399 — WhatsApp bridge HTTP endpoints lack authentication
- [CC0261] severity=HIGH passes=1 lines=~439-460(post/send-mediaendpoint) — WhatsApp bridge allows arbitrary URL fetch for media attachment

**Step 1: Investigate root cause**
- Read `scripts/whatsapp-bridge/bridge.js` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address scripts/whatsapp-bridge/bridge.js audit findings`

### Task C.3: `scripts/build_skills_index.py`

**Objective:** Resolve the 1 ranked cluster(s) in `scripts/build_skills_index.py` before moving to the next file batch.

**Files:**
- Modify: `scripts/build_skills_index.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `CRITICAL`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0232] severity=CRITICAL passes=1 lines=34 — build_skills_index.py imports non-existent tools.skills_hub

**Step 1: Investigate root cause**
- Read `scripts/build_skills_index.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address scripts/build_skills_index.py audit findings`

### Task C.4: `scripts/contributor_audit.py`

**Objective:** Resolve the 1 ranked cluster(s) in `scripts/contributor_audit.py` before moving to the next file batch.

**Files:**
- Modify: `scripts/contributor_audit.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `CRITICAL`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0234] severity=CRITICAL passes=1 lines=33 — contributor_audit.py broken import from release module

**Step 1: Investigate root cause**
- Read `scripts/contributor_audit.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address scripts/contributor_audit.py audit findings`

### Task C.5: `scripts/whatsapp-bridge/package.json`

**Objective:** Resolve the 1 ranked cluster(s) in `scripts/whatsapp-bridge/package.json` before moving to the next file batch.

**Files:**
- Modify: `scripts/whatsapp-bridge/package.json`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `CRITICAL`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0262] severity=CRITICAL passes=1 lines=11 — WhatsApp bridge pins Baileys to raw git commit

**Step 1: Investigate root cause**
- Read `scripts/whatsapp-bridge/package.json` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address scripts/whatsapp-bridge/package.json audit findings`

### Task C.6: `packaging/homebrew/hermes-agent.rb`

**Objective:** Resolve the 3 ranked cluster(s) in `packaging/homebrew/hermes-agent.rb` before moving to the next file batch.

**Files:**
- Modify: `packaging/homebrew/hermes-agent.rb`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0211] severity=HIGH passes=2 lines=8 — Homebrew formula version drift
- [CC0210] severity=HIGH passes=1 lines=15 — Homebrew depends on Python 3.14 (nonexistent)
- [CC0212] severity=HIGH passes=1 lines=9 — Homebrew formula SHA256 placeholder

**Step 1: Investigate root cause**
- Read `packaging/homebrew/hermes-agent.rb` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address packaging/homebrew/hermes-agent.rb audit findings`

### Task C.7: `.github/workflows/contributor-check.yml`

**Objective:** Resolve the 1 ranked cluster(s) in `.github/workflows/contributor-check.yml` before moving to the next file batch.

**Files:**
- Modify: `.github/workflows/contributor-check.yml`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0006] severity=HIGH passes=2 lines=51 — contributor-check.shell AUTHOR=*** is invalid git syntax

**Step 1: Investigate root cause**
- Read `.github/workflows/contributor-check.yml` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address .github/workflows/contributor-check.yml audit findings`

### Task C.8: `.github/workflows/docker-publish.yml`

**Objective:** Resolve the 1 ranked cluster(s) in `.github/workflows/docker-publish.yml` before moving to the next file batch.

**Files:**
- Modify: `.github/workflows/docker-publish.yml`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0007] severity=HIGH passes=1 lines=58 — docker-publish.yml login step runs on unintended events

**Step 1: Investigate root cause**
- Read `.github/workflows/docker-publish.yml` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address .github/workflows/docker-publish.yml audit findings`

### Task C.9: `website/docs/user-guide/features/delegation.md`

**Objective:** Resolve the 1 ranked cluster(s) in `website/docs/user-guide/features/delegation.md` before moving to the next file batch.

**Files:**
- Modify: `website/docs/user-guide/features/delegation.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0588] severity=HIGH passes=1 lines=125 — delegation.md states MAX_CONCURRENT_CHILDREN=3, actual default is 100

**Step 1: Investigate root cause**
- Read `website/docs/user-guide/features/delegation.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address website/docs/user-guide/features/delegation.md audit findings`

### Task C.10: `website/docs/user-guide/features/mcp.md`

**Objective:** Resolve the 1 ranked cluster(s) in `website/docs/user-guide/features/mcp.md` before moving to the next file batch.

**Files:**
- Modify: `website/docs/user-guide/features/mcp.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0591] severity=HIGH passes=1 lines=503 — Wrong Discord channel format in MCP messages_send example

**Step 1: Investigate root cause**
- Read `website/docs/user-guide/features/mcp.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address website/docs/user-guide/features/mcp.md audit findings`

### Task C.11: `website/docs/user-guide/git-worktrees.md`

**Objective:** Resolve the 1 ranked cluster(s) in `website/docs/user-guide/git-worktrees.md` before moving to the next file batch.

**Files:**
- Modify: `website/docs/user-guide/git-worktrees.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0605] severity=HIGH passes=1 lines=36,136 — Missing doc referenced: checkpoints-and-rollback.md

**Step 1: Investigate root cause**
- Read `website/docs/user-guide/git-worktrees.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address website/docs/user-guide/git-worktrees.md audit findings`

### Task C.12: `website/docs/user-guide/messaging/index.md`

**Objective:** Resolve the 1 ranked cluster(s) in `website/docs/user-guide/messaging/index.md` before moving to the next file batch.

**Files:**
- Modify: `website/docs/user-guide/messaging/index.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0607] severity=HIGH passes=1 lines=11 — Missing doc referenced: guides/use-voice-mode-with-hermes

**Step 1: Investigate root cause**
- Read `website/docs/user-guide/messaging/index.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address website/docs/user-guide/messaging/index.md audit findings`

### Task C.13: `website/docs/user-guide/skills/godmode.md`

**Objective:** Resolve the 1 ranked cluster(s) in `website/docs/user-guide/skills/godmode.md` before moving to the next file batch.

**Files:**
- Modify: `website/docs/user-guide/skills/godmode.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0610] severity=HIGH passes=1 lines=14 — Broken cross-ref: skills-catalog#mlopsinference does not exist

**Step 1: Investigate root cause**
- Read `website/docs/user-guide/skills/godmode.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address website/docs/user-guide/skills/godmode.md audit findings`

### Task C.14: `website/src/`

**Objective:** Resolve the 1 ranked cluster(s) in `website/src/` before moving to the next file batch.

**Files:**
- Modify: `website/src/`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0616] severity=HIGH passes=1 lines=unknown(structuralgap) — Missing `src/data/` directory breaks skills page build

**Step 1: Investigate root cause**
- Read `website/src/` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address website/src/ audit findings`

### Task C.15: `website/src/pages/skills/index.tsx`

**Objective:** Resolve the 1 ranked cluster(s) in `website/src/pages/skills/index.tsx` before moving to the next file batch.

**Files:**
- Modify: `website/src/pages/skills/index.tsx`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `3` pass(es).

**Clusters in this task:**
- [CC0618] severity=HIGH passes=3 lines=3 — Missing skills.json build-time dependency

**Step 1: Investigate root cause**
- Read `website/src/pages/skills/index.tsx` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address website/src/pages/skills/index.tsx audit findings`

### Task C.16: `website/scripts/extract-skills.py`

**Objective:** Resolve the 2 ranked cluster(s) in `website/scripts/extract-skills.py` before moving to the next file batch.

**Files:**
- Modify: `website/scripts/extract-skills.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `3` pass(es).

**Clusters in this task:**
- [CC0614] severity=MEDIUM passes=3 lines=52-57 — extract-skills.py hardcodes community "openai_skills" source but no such source exists in SOURCE_LABELS
- [CC0613] severity=LOW passes=2 lines=10 — extract-skills.py uses hardcoded repo-relative paths that assume CWD

**Step 1: Investigate root cause**
- Read `website/scripts/extract-skills.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address website/scripts/extract-skills.py audit findings`

### Task C.17: `scripts/sample_and_compress.py`

**Objective:** Resolve the 1 ranked cluster(s) in `scripts/sample_and_compress.py` before moving to the next file batch.

**Files:**
- Modify: `scripts/sample_and_compress.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0249] severity=MEDIUM passes=2 lines=77-85,172-177 — sample_and_compress.py multiprocessing global tokenizer is fragile

**Step 1: Investigate root cause**
- Read `scripts/sample_and_compress.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address scripts/sample_and_compress.py audit findings`


## Batch D: Core medium-severity correctness and infrastructure debt

Important but lower urgency than hard breakages/security.

### Task D.1: `tools/skills_guard.py`

**Objective:** Resolve the 2 ranked cluster(s) in `tools/skills_guard.py` before moving to the next file batch.

**Files:**
- Modify: `tools/skills_guard.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0526] severity=MEDIUM passes=2 lines=880-904 — skills_guard trusts any source starting with openai/ or anthropic/ prefix
- [CC0528] severity=MEDIUM passes=2 lines=907-919(_determine_verdictfunction) — skills_guard verdict logic bug: high+medium returns dangerous

**Step 1: Investigate root cause**
- Read `tools/skills_guard.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tools/skills_guard.py audit findings`

### Task D.2: `agent/credential_pool.py`

**Objective:** Resolve the 1 ranked cluster(s) in `agent/credential_pool.py` before moving to the next file batch.

**Files:**
- Modify: `agent/credential_pool.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0022] severity=MEDIUM passes=2 lines=423–458 — Race condition in _sync_anthropic_entry_from_credentials_file

**Step 1: Investigate root cause**
- Read `agent/credential_pool.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address agent/credential_pool.py audit findings`

### Task D.3: `hermes_cli/mcp_config.py`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_cli/mcp_config.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_cli/mcp_config.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0139] severity=MEDIUM passes=2 lines=33 — _MCP_PRESETS dict is never populated in mcp_config.py

**Step 1: Investigate root cause**
- Read `hermes_cli/mcp_config.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_cli/mcp_config.py audit findings`

### Task D.4: `tools/mcp_oauth.py`

**Objective:** Resolve the 1 ranked cluster(s) in `tools/mcp_oauth.py` before moving to the next file batch.

**Files:**
- Modify: `tools/mcp_oauth.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0489] severity=MEDIUM passes=2 lines=85,312-363 — mcp_oauth callback port shared mutable state

**Step 1: Investigate root cause**
- Read `tools/mcp_oauth.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tools/mcp_oauth.py audit findings`


## Batch E: Documentation / skill / content review

Review after core runtime/security/build work; often content drift rather than executable breakage.

### Task E.1: `pyproject.toml`

**Objective:** Resolve the 2 ranked cluster(s) in `pyproject.toml` before moving to the next file batch.

**Files:**
- Modify: `pyproject.toml`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0223] severity=HIGH passes=1 lines=rlextradependencies — Unpinned git direct references in pyproject.toml rl extra
- [CC0222] severity=MEDIUM passes=2 lines=81–82 — pyproject.toml rl extra pins git dependencies without version tags

**Step 1: Investigate root cause**
- Read `pyproject.toml` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address pyproject.toml audit findings`

### Task E.2: `web/src/components/autofield.tsx`

**Objective:** Resolve the 1 ranked cluster(s) in `web/src/components/autofield.tsx` before moving to the next file batch.

**Files:**
- Modify: `web/src/components/autofield.tsx`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0556] severity=HIGH passes=1 lines=111 — Unlocalized placeholder in AutoField textarea

**Step 1: Investigate root cause**
- Read `web/src/components/autofield.tsx` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address web/src/components/autofield.tsx audit findings`

### Task E.3: `acp_adapter/auth.py`

**Objective:** Resolve the 1 ranked cluster(s) in `acp_adapter/auth.py` before moving to the next file batch.

**Files:**
- Modify: `acp_adapter/auth.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0010] severity=MEDIUM passes=2 lines=13-23 — detect_provider() silently swallows all exceptions

**Step 1: Investigate root cause**
- Read `acp_adapter/auth.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address acp_adapter/auth.py audit findings`

### Task E.4: `requirements.txt`

**Objective:** Resolve the 1 ranked cluster(s) in `requirements.txt` before moving to the next file batch.

**Files:**
- Modify: `requirements.txt`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0225] severity=MEDIUM passes=2 lines=1–3 — requirements.txt documents itself as deprecated but is actively maintained

**Step 1: Investigate root cause**
- Read `requirements.txt` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address requirements.txt audit findings`

### Task E.5: `web/src/lib/api.ts`

**Objective:** Resolve the 1 ranked cluster(s) in `web/src/lib/api.ts` before moving to the next file batch.

**Files:**
- Modify: `web/src/lib/api.ts`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0565] severity=MEDIUM passes=2 lines=27-35,12-25 — api.ts getSessionToken() throws if token is missing, but fetchJSON silently catches all errors

**Step 1: Investigate root cause**
- Read `web/src/lib/api.ts` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address web/src/lib/api.ts audit findings`

### Task E.6: `cron/scheduler.py`

**Objective:** Resolve the 1 ranked cluster(s) in `cron/scheduler.py` before moving to the next file batch.

**Files:**
- Modify: `cron/scheduler.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `LOW`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0046] severity=LOW passes=2 lines=43-49 — `_KNOWN_DELIVERY_PLATFORMS` in scheduler.py is a static copy of Platform enum

**Step 1: Investigate root cause**
- Read `cron/scheduler.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address cron/scheduler.py audit findings`

### Task E.7: `gateway/stream_consumer.py`

**Objective:** Resolve the 1 ranked cluster(s) in `gateway/stream_consumer.py` before moving to the next file batch.

**Files:**
- Modify: `gateway/stream_consumer.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `LOW`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0113] severity=LOW passes=2 lines=188-189 — stream_consumer: partial-tag buffer held indefinitely on slow stream

**Step 1: Investigate root cause**
- Read `gateway/stream_consumer.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address gateway/stream_consumer.py audit findings`

### Task E.8: `hermes_cli/skills_hub.py`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_cli/skills_hub.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_cli/skills_hub.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `LOW`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0172] severity=LOW passes=2 lines=908-909 — Skill snapshot `hermes_version` hardcoded to `"0.1.0"`

**Step 1: Investigate root cause**
- Read `hermes_cli/skills_hub.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_cli/skills_hub.py audit findings`

### Task E.9: `hermes_state.py`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_state.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_state.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `LOW`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0194] severity=LOW passes=2 lines=1-1238(schemaat~1-100) — Schema version mismatch risk in hermes_state

**Step 1: Investigate root cause**
- Read `hermes_state.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_state.py audit findings`

### Task E.10: `hermes_time.py`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes_time.py` before moving to the next file batch.

**Files:**
- Modify: `hermes_time.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `LOW`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0195] severity=LOW passes=2 lines=1-104 — hermes_time.py is clean — no issues found

**Step 1: Investigate root cause**
- Read `hermes_time.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes_time.py audit findings`


## Batch F: Tests / docs / skill content / cleanup debt

Defer until product/runtime/security issues are fixed; many are low-signal quality issues.

### Task F.1: `skills/productivity/powerpoint/scripts/office/pack.py`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/productivity/powerpoint/scripts/office/pack.py` before moving to the next file batch.

**Files:**
- Modify: `skills/productivity/powerpoint/scripts/office/pack.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `CRITICAL`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0345] severity=CRITICAL passes=2 lines=22 — Missing validators module causes import failure

**Step 1: Investigate root cause**
- Read `skills/productivity/powerpoint/scripts/office/pack.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/productivity/powerpoint/scripts/office/pack.py audit findings`

### Task F.2: `skills/mlops/research/dspy/skill.md`

**Objective:** Resolve the 2 ranked cluster(s) in `skills/mlops/research/dspy/skill.md` before moving to the next file batch.

**Files:**
- Modify: `skills/mlops/research/dspy/skill.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `4` pass(es).

**Clusters in this task:**
- [CC0293] severity=HIGH passes=4 lines=51,73,293,328 — Deprecated `dspy.Claude` class in DSPy SKILL.md
- [CC0291] severity=HIGH passes=1 lines=258 — Broken import path for ChromaRM retriever

**Step 1: Investigate root cause**
- Read `skills/mlops/research/dspy/skill.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/mlops/research/dspy/skill.md audit findings`

### Task F.3: `skills/mlops/training/pytorch-fsdp/skill.md`

**Objective:** Resolve the 2 ranked cluster(s) in `skills/mlops/training/pytorch-fsdp/skill.md` before moving to the next file batch.

**Files:**
- Modify: `skills/mlops/training/pytorch-fsdp/skill.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `4` pass(es).

**Clusters in this task:**
- [CC0308] severity=HIGH passes=4 lines=29-31 — Garbled/truncated Quick Reference in pytorch-fsdp SKILL.md
- [CC0310] severity=MEDIUM passes=2 lines=92-96 — pytorch-fsdp SKILL.md references non-existent reference file

**Step 1: Investigate root cause**
- Read `skills/mlops/training/pytorch-fsdp/skill.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/mlops/training/pytorch-fsdp/skill.md audit findings`

### Task F.4: `skills/research/research-paper-writing/skill.md`

**Objective:** Resolve the 2 ranked cluster(s) in `skills/research/research-paper-writing/skill.md` before moving to the next file batch.

**Files:**
- Modify: `skills/research/research-paper-writing/skill.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0394] severity=HIGH passes=2 lines=1-14(frontmatter) — research-paper-writing SKILL.md declares unused dependencies
- [CC0395] severity=MEDIUM passes=2 lines=338 — Stale PLACEHOLDER citation in research-paper-writing SKILL

**Step 1: Investigate root cause**
- Read `skills/research/research-paper-writing/skill.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/research/research-paper-writing/skill.md audit findings`

### Task F.5: `skills/creative/popular-web-designs/skill.md (and 50+ template files)`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/creative/popular-web-designs/skill.md (and 50+ template files)` before moving to the next file batch.

**Files:**
- Modify: `skills/creative/popular-web-designs/skill.md (and 50+ template files)`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0269] severity=HIGH passes=1 lines=skill.md35;all50+templatefilesat13 — `generative-widgets` skill referenced but does not exist

**Step 1: Investigate root cause**
- Read `skills/creative/popular-web-designs/skill.md (and 50+ template files)` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/creative/popular-web-designs/skill.md (and 50+ template files) audit findings`

### Task F.6: `skills/creative/popular-web-designs/templates/*.md`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/creative/popular-web-designs/templates/*.md` before moving to the next file batch.

**Files:**
- Modify: `skills/creative/popular-web-designs/templates/*.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0270] severity=HIGH passes=1 lines=~13(uniformacross30+templatefiles) — Missing `generative-widgets` skill (broken cross-skill reference)

**Step 1: Investigate root cause**
- Read `skills/creative/popular-web-designs/templates/*.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/creative/popular-web-designs/templates/*.md audit findings`

### Task F.7: `skills/media/youtube-content/skill.md`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/media/youtube-content/skill.md` before moving to the next file batch.

**Files:**
- Modify: `skills/media/youtube-content/skill.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0276] severity=HIGH passes=1 lines=26,29,32,35 — SKILL_DIR placeholder undefined at runtime

**Step 1: Investigate root cause**
- Read `skills/media/youtube-content/skill.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/media/youtube-content/skill.md audit findings`

### Task F.8: `skills/mlops/research/description.md`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/mlops/research/description.md` before moving to the next file batch.

**Files:**
- Modify: `skills/mlops/research/description.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0287] severity=HIGH passes=1 lines=1-3 — Empty DESCRIPTION.md files have no content

**Step 1: Investigate root cause**
- Read `skills/mlops/research/description.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/mlops/research/description.md audit findings`

### Task F.9: `skills/mlops/training/description.md`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/mlops/training/description.md` before moving to the next file batch.

**Files:**
- Modify: `skills/mlops/training/description.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0299] severity=HIGH passes=1 lines=1-3 — Empty training DESCRIPTION.md is a stub

**Step 1: Investigate root cause**
- Read `skills/mlops/training/description.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/mlops/training/description.md audit findings`

### Task F.10: `skills/mlops/training/grpo-rl-training/readme.md`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/mlops/training/grpo-rl-training/readme.md` before moving to the next file batch.

**Files:**
- Modify: `skills/mlops/training/grpo-rl-training/readme.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0300] severity=HIGH passes=1 lines=14-15 — grpo-rl-training README.md references non-existent examples/

**Step 1: Investigate root cause**
- Read `skills/mlops/training/grpo-rl-training/readme.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/mlops/training/grpo-rl-training/readme.md audit findings`

### Task F.11: `skills/mlops/training/grpo-rl-training/skill.md`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/mlops/training/grpo-rl-training/skill.md` before moving to the next file batch.

**Files:**
- Modify: `skills/mlops/training/grpo-rl-training/skill.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0301] severity=HIGH passes=2 lines=501-575(truncated~75) — grpo-rl-training SKILL.md truncated at line 575

**Step 1: Investigate root cause**
- Read `skills/mlops/training/grpo-rl-training/skill.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/mlops/training/grpo-rl-training/skill.md audit findings`

### Task F.12: `skills/mlops/training/grpo-rl-training/templates/basic_grpo_training.py`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/mlops/training/grpo-rl-training/templates/basic_grpo_training.py` before moving to the next file batch.

**Files:**
- Modify: `skills/mlops/training/grpo-rl-training/templates/basic_grpo_training.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0302] severity=HIGH passes=1 lines=78 — basic_grpo_training.py reward function parameter order mismatch

**Step 1: Investigate root cause**
- Read `skills/mlops/training/grpo-rl-training/templates/basic_grpo_training.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/mlops/training/grpo-rl-training/templates/basic_grpo_training.py audit findings`

### Task F.13: `skills/mlops/training/unsloth/skill.md`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/mlops/training/unsloth/skill.md` before moving to the next file batch.

**Files:**
- Modify: `skills/mlops/training/unsloth/skill.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `3` pass(es).

**Clusters in this task:**
- [CC0325] severity=HIGH passes=3 lines=18-50 — SKILL.md content underfilled / placeholder quality

**Step 1: Investigate root cause**
- Read `skills/mlops/training/unsloth/skill.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/mlops/training/unsloth/skill.md audit findings`

### Task F.14: `tests/gateway/test_run_progress_topics.py`

**Objective:** Resolve the 1 ranked cluster(s) in `tests/gateway/test_run_progress_topics.py` before moving to the next file batch.

**Files:**
- Modify: `tests/gateway/test_run_progress_topics.py`
- Test: `tests/gateway/test_run_progress_topics.py`

**Priority context:** highest severity `HIGH`, max recurrence `3` pass(es).

**Clusters in this task:**
- [CC0435] severity=HIGH passes=3 lines=76 — Hardcoded absolute path in test fixture artifact

**Step 1: Investigate root cause**
- Read `tests/gateway/test_run_progress_topics.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tests/gateway/test_run_progress_topics.py audit findings`

### Task F.15: `tests/run_agent/test_compression_persistence.py`

**Objective:** Resolve the 1 ranked cluster(s) in `tests/run_agent/test_compression_persistence.py` before moving to the next file batch.

**Files:**
- Modify: `tests/run_agent/test_compression_persistence.py`
- Test: `tests/run_agent/test_compression_persistence.py`

**Priority context:** highest severity `HIGH`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0458] severity=HIGH passes=2 lines=91–93 — test_compression_persistence.py documents known message-loss bug

**Step 1: Investigate root cause**
- Read `tests/run_agent/test_compression_persistence.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tests/run_agent/test_compression_persistence.py audit findings`

### Task F.16: `tests/run_agent/test_413_compression.py`

**Objective:** Resolve the 2 ranked cluster(s) in `tests/run_agent/test_413_compression.py` before moving to the next file batch.

**Files:**
- Modify: `tests/run_agent/test_413_compression.py`
- Test: `tests/run_agent/test_413_compression.py`

**Priority context:** highest severity `MEDIUM`, max recurrence `3` pass(es).

**Clusters in this task:**
- [CC0454] severity=MEDIUM passes=3 lines=10 — Dead commented-out skip in test_413_compression.py
- [CC0455] severity=LOW passes=2 lines=9-10 — Compressed pytest fixture with empty docstring

**Step 1: Investigate root cause**
- Read `tests/run_agent/test_413_compression.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tests/run_agent/test_413_compression.py audit findings`

### Task F.17: `skills/index-cache/openai_skills_skills_.json`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/index-cache/openai_skills_skills_.json` before moving to the next file batch.

**Files:**
- Modify: `skills/index-cache/openai_skills_skills_.json`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0273] severity=MEDIUM passes=2 lines=1 — Empty skills index cache for OpenAI

**Step 1: Investigate root cause**
- Read `skills/index-cache/openai_skills_skills_.json` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/index-cache/openai_skills_skills_.json audit findings`

### Task F.18: `skills/mlops/models/stable-diffusion/references/advanced-usage.md`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/mlops/models/stable-diffusion/references/advanced-usage.md` before moving to the next file batch.

**Files:**
- Modify: `skills/mlops/models/stable-diffusion/references/advanced-usage.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0279] severity=MEDIUM passes=2 lines=19,23,27,31,35,153,450,513,578 — Same deprecated path in advanced-usage.md

**Step 1: Investigate root cause**
- Read `skills/mlops/models/stable-diffusion/references/advanced-usage.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/mlops/models/stable-diffusion/references/advanced-usage.md audit findings`

### Task F.19: `skills/mlops/models/stable-diffusion/skill.md`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/mlops/models/stable-diffusion/skill.md` before moving to the next file batch.

**Files:**
- Modify: `skills/mlops/models/stable-diffusion/skill.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `3` pass(es).

**Clusters in this task:**
- [CC0284] severity=MEDIUM passes=3 lines=59,81,214,237,301,397 — Deprecated model IDs in Stable Diffusion docs

**Step 1: Investigate root cause**
- Read `skills/mlops/models/stable-diffusion/skill.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/mlops/models/stable-diffusion/skill.md audit findings`

### Task F.20: `skills/mlops/research/dspy/references/examples.md`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/mlops/research/dspy/references/examples.md` before moving to the next file batch.

**Files:**
- Modify: `skills/mlops/research/dspy/references/examples.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0289] severity=MEDIUM passes=2 lines=150 — Wrong DSPy import for ReAct module

**Step 1: Investigate root cause**
- Read `skills/mlops/research/dspy/references/examples.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/mlops/research/dspy/references/examples.md audit findings`

### Task F.21: `skills/mlops/training/axolotl/references/api.md`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/mlops/training/axolotl/references/api.md` before moving to the next file batch.

**Files:**
- Modify: `skills/mlops/training/axolotl/references/api.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `6` pass(es).

**Clusters in this task:**
- [CC0297] severity=MEDIUM passes=6 lines=1610 — Dead upstream TODO in axolotl API reference

**Step 1: Investigate root cause**
- Read `skills/mlops/training/axolotl/references/api.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/mlops/training/axolotl/references/api.md audit findings`

### Task F.22: `skills/mlops/training/peft/references/advanced-usage.md`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/mlops/training/peft/references/advanced-usage.md` before moving to the next file batch.

**Files:**
- Modify: `skills/mlops/training/peft/references/advanced-usage.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `MEDIUM`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0304] severity=MEDIUM passes=2 lines=501-514(truncated~13) — peft references/advanced-usage.md truncated at line 514

**Step 1: Investigate root cause**
- Read `skills/mlops/training/peft/references/advanced-usage.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/mlops/training/peft/references/advanced-usage.md audit findings`

### Task F.23: `tests/gateway/test_transcript_offset.py`

**Objective:** Resolve the 1 ranked cluster(s) in `tests/gateway/test_transcript_offset.py` before moving to the next file batch.

**Files:**
- Modify: `tests/gateway/test_transcript_offset.py`
- Test: `tests/gateway/test_transcript_offset.py`

**Priority context:** highest severity `MEDIUM`, max recurrence `3` pass(es).

**Clusters in this task:**
- [CC0450] severity=MEDIUM passes=3 lines=90,156,191,259 — Test comments document OLD buggy behavior alongside FIXED behavior

**Step 1: Investigate root cause**
- Read `tests/gateway/test_transcript_offset.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tests/gateway/test_transcript_offset.py audit findings`

### Task F.24: `tests/run_agent/test_compression_boundary.py`

**Objective:** Resolve the 1 ranked cluster(s) in `tests/run_agent/test_compression_boundary.py` before moving to the next file batch.

**Files:**
- Modify: `tests/run_agent/test_compression_boundary.py`
- Test: `tests/run_agent/test_compression_boundary.py`

**Priority context:** highest severity `MEDIUM`, max recurrence `3` pass(es).

**Clusters in this task:**
- [CC0457] severity=MEDIUM passes=3 lines=84 — Context compressor tool result group boundary bug untracked

**Step 1: Investigate root cause**
- Read `tests/run_agent/test_compression_boundary.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tests/run_agent/test_compression_boundary.py audit findings`

### Task F.25: `hermes-already-has-routines.md`

**Objective:** Resolve the 1 ranked cluster(s) in `hermes-already-has-routines.md` before moving to the next file batch.

**Files:**
- Modify: `hermes-already-has-routines.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `LOW`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0115] severity=LOW passes=2 lines=1-160 — hermes-already-has-routines.md is an opinionated marketing doc in repo

**Step 1: Investigate root cause**
- Read `hermes-already-has-routines.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address hermes-already-has-routines.md audit findings`

### Task F.26: `tests/gateway/test_voice_command.py`

**Objective:** Resolve the 1 ranked cluster(s) in `tests/gateway/test_voice_command.py` before moving to the next file batch.

**Files:**
- Modify: `tests/gateway/test_voice_command.py`
- Test: `tests/gateway/test_voice_command.py`

**Priority context:** highest severity `LOW`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0452] severity=LOW passes=2 lines=2113 — One conditional skip for optional `nacl` dependency

**Step 1: Investigate root cause**
- Read `tests/gateway/test_voice_command.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address tests/gateway/test_voice_command.py audit findings`

### Task F.27: `skills/dogfood/skill.md`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/dogfood/skill.md` before moving to the next file batch.

**Files:**
- Modify: `skills/dogfood/skill.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `INFO`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0271] severity=INFO passes=2 lines=8 — Inconsistent `related_skills` metadata in dogfood skill

**Step 1: Investigate root cause**
- Read `skills/dogfood/skill.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/dogfood/skill.md audit findings`


## Batch G: Red-team / intentionally risky content review

Review separately; many findings may be intentional or policy-content rather than core product bugs.

### Task G.1: `skills/red-teaming/godmode/scripts/auto_jailbreak.py`

**Objective:** Resolve the 7 ranked cluster(s) in `skills/red-teaming/godmode/scripts/auto_jailbreak.py` before moving to the next file batch.

**Files:**
- Modify: `skills/red-teaming/godmode/scripts/auto_jailbreak.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `CRITICAL`, max recurrence `3` pass(es).

**Clusters in this task:**
- [CC0359] severity=CRITICAL passes=3 lines=47-54 — auto_jailbreak.py uses exec() to load sibling modules into caller globals
- [CC0358] severity=CRITICAL passes=1 lines=497-498 — auto_jailbreak.py:498 has unclosed return statement
- [CC0354] severity=HIGH passes=2 lines=34-38,60-61 — Auto-jailbreak uses HERMES_HOME which may not match agent install path
- [CC0355] severity=HIGH passes=1 lines=383-406 — auto_jailbreak config merge can silently corrupt YAML
- [CC0357] severity=HIGH passes=1 lines=479 — `score_response` used in auto_jailbreak.py without local definition
- [CC0360] severity=HIGH passes=1 lines=653-671,715-739 — auto_jailbreak.py writes jailbreak config to user-facing HERMES_HOME
- [CC0361] severity=HIGH passes=1 lines=68-75 — auto_jailbreak.py contains explicit harmful-content canary queries

**Step 1: Investigate root cause**
- Read `skills/red-teaming/godmode/scripts/auto_jailbreak.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/red-teaming/godmode/scripts/auto_jailbreak.py audit findings`

### Task G.2: `skills/red-teaming/godmode/templates/prefill-subtle.json`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/red-teaming/godmode/templates/prefill-subtle.json` before moving to the next file batch.

**Files:**
- Modify: `skills/red-teaming/godmode/templates/prefill-subtle.json`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `CRITICAL`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0385] severity=CRITICAL passes=1 lines=1-10 — prefill-subtle.json impersonates a security researcher to suppress refusals

**Step 1: Investigate root cause**
- Read `skills/red-teaming/godmode/templates/prefill-subtle.json` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/red-teaming/godmode/templates/prefill-subtle.json audit findings`

### Task G.3: `skills/red-teaming/godmode/scripts/godmode_race.py`

**Objective:** Resolve the 4 ranked cluster(s) in `skills/red-teaming/godmode/scripts/godmode_race.py` before moving to the next file batch.

**Files:**
- Modify: `skills/red-teaming/godmode/scripts/godmode_race.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0364] severity=HIGH passes=2 lines=104-130 — race_models() anti-hedge directive instructs models to override safety
- [CC0369] severity=HIGH passes=2 lines=35-96 — Future-dated model entries in godmode_race.py
- [CC0365] severity=HIGH passes=1 lines=165 — `tool_choice` references non-existent `get_response_quality` function in godmode_race.py
- [CC0367] severity=HIGH passes=1 lines=272,279,298,305 — `score_response` referenced but never defined in godmode_race.py

**Step 1: Investigate root cause**
- Read `skills/red-teaming/godmode/scripts/godmode_race.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/red-teaming/godmode/scripts/godmode_race.py audit findings`

### Task G.4: `skills/red-teaming/godmode/skill.md`

**Objective:** Resolve the 4 ranked cluster(s) in `skills/red-teaming/godmode/skill.md` before moving to the next file batch.

**Files:**
- Modify: `skills/red-teaming/godmode/skill.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `3` pass(es).

**Clusters in this task:**
- [CC0377] severity=HIGH passes=1 lines=1-403(entirefile) — Godmode SKILL.md documents jailbreak techniques without red-team scope guard
- [CC0381] severity=HIGH passes=1 lines=55-79 — Broken reference to non-existent load_godmode.py
- [CC0380] severity=MEDIUM passes=2 lines=41,46 — Godmode skill references non-existent files
- [CC0379] severity=LOW passes=3 lines=353-388 — SKILL.md tested-results section may be model-version specific but doesn't say so

**Step 1: Investigate root cause**
- Read `skills/red-teaming/godmode/skill.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/red-teaming/godmode/skill.md audit findings`

### Task G.5: `skills/red-teaming/godmode/scripts/parseltongue.py`

**Objective:** Resolve the 2 ranked cluster(s) in `skills/red-teaming/godmode/scripts/parseltongue.py` before moving to the next file batch.

**Files:**
- Modify: `skills/red-teaming/godmode/scripts/parseltongue.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0375] severity=HIGH passes=1 lines=unknown — parseltongue.py encode_variants() creates prompt injection variants
- [CC0372] severity=LOW passes=2 lines=196-205 — parseltongue.py _apply_piglatin crashes on single-char words

**Step 1: Investigate root cause**
- Read `skills/red-teaming/godmode/scripts/parseltongue.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/red-teaming/godmode/scripts/parseltongue.py audit findings`

### Task G.6: `optional-skills/security/oss-forensics/scripts/evidence-store.py`

**Objective:** Resolve the 1 ranked cluster(s) in `optional-skills/security/oss-forensics/scripts/evidence-store.py` before moving to the next file batch.

**Files:**
- Modify: `optional-skills/security/oss-forensics/scripts/evidence-store.py`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0208] severity=HIGH passes=1 lines=158 — Evidence store writes evidence files with 0o644 permissions

**Step 1: Investigate root cause**
- Read `optional-skills/security/oss-forensics/scripts/evidence-store.py` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address optional-skills/security/oss-forensics/scripts/evidence-store.py audit findings`

### Task G.7: `skills/inference-sh/`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/inference-sh/` before moving to the next file batch.

**Files:**
- Modify: `skills/inference-sh/`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0274] severity=HIGH passes=1 lines=entiredirectory — `inference-sh` skill has no implementation (DESCRIPTION.md only)

**Step 1: Investigate root cause**
- Read `skills/inference-sh/` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/inference-sh/ audit findings`

### Task G.8: `skills/red-teaming/godmode/references/jailbreak-templates.md`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/red-teaming/godmode/references/jailbreak-templates.md` before moving to the next file batch.

**Files:**
- Modify: `skills/red-teaming/godmode/references/jailbreak-templates.md`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `1` pass(es).

**Clusters in this task:**
- [CC0350] severity=HIGH passes=1 lines=9,31,45,59,78 — jailbreak-templates.md uses outdated model IDs vs godmode_race.py

**Step 1: Investigate root cause**
- Read `skills/red-teaming/godmode/references/jailbreak-templates.md` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/red-teaming/godmode/references/jailbreak-templates.md audit findings`

### Task G.9: `skills/red-teaming/godmode/templates/prefill.json`

**Objective:** Resolve the 1 ranked cluster(s) in `skills/red-teaming/godmode/templates/prefill.json` before moving to the next file batch.

**Files:**
- Modify: `skills/red-teaming/godmode/templates/prefill.json`
- Test: identify or add the nearest relevant regression test before changing code

**Priority context:** highest severity `HIGH`, max recurrence `2` pass(es).

**Clusters in this task:**
- [CC0386] severity=HIGH passes=2 lines=1-18 — prefill.json primes model for unrestricted responses

**Step 1: Investigate root cause**
- Read `skills/red-teaming/godmode/templates/prefill.json` and inspect the cited line ranges above.
- Confirm whether multiple clusters are one bug or truly separate fixes.

**Step 2: Write or identify regression coverage**
- Add/extend targeted tests where practical before changing code.
- If the issue is docs/skills-only, add a verification step instead of code tests.

**Step 3: Implement the minimal fix**
- Fix the real defect only; do not bundle adjacent cleanup unless required for correctness.

**Step 4: Verify**
- Run the narrowest relevant tests first, then a slightly broader suite for the touched subsystem.
- Re-check the affected path against the original cluster descriptions.

**Step 5: Commit**
- Commit message: `fix: address skills/red-teaming/godmode/templates/prefill.json audit findings`


## Notes on scope

- Findings under `skills/red-teaming/` are grouped later unless they break tooling at runtime. Many are intentionally risky content, not necessarily product bugs.
- Findings in `tests/` are mostly treated as signal for stale comments/coverage gaps rather than immediate product breakage.
- Repeated findings across 2+ passes got elevated because they are more likely to be true stable defects than wording noise.

## Recommended next action

Start with **Batch A** and **Batch B** only. Once those are resolved and verified, move to **Batch C**. Leave the rest for later cleanup unless Brendan explicitly wants docs/skills/test debt fixed in the same sweep.
