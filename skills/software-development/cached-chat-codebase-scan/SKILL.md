---
name: cached-chat-codebase-scan
description: Use when a user asks to scan, audit, or review a codebase/folder/repository with N agents/workers. Prefer an efficient cached chat-agent map/reduce scan first, then use Hermes delegate_task agents only for targeted verification. Writes shard outputs to disk before aggregation to avoid truncation.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [codebase-scan, audit, cached-chat, autogen, map-reduce, delegation]
    related_skills: [subagent-driven-development, requesting-code-review, systematic-debugging]
---

# Cached Chat Codebase Scan

## Goal

When the user says something like "scan this repo with 25 agents", treat "agents"
as **logical workers**, not as a command to start 25 unconstrained autonomous
tool loops.

Use the most efficient reliable plan automatically:

1. Cached chat fan-out for broad coverage.
2. Local deterministic tools for indexing, search, and test execution.
3. Hermes `delegate_task` agents only for high-value verification.
4. Disk-spooled shard outputs for aggregation.

The user should not need to choose chat vs agent manually.

## Preferred Harness

Use Hermes' `scan_codebase` tool for broad scans. It provides the efficient
default path:

- local file inventory
- stable file-hash response caching
- logical worker fan-out
- disk-spooled worker reports
- Hermes runtime/provider routing for live model calls

AutoGen AgentChat is an optional open-source extension point for
OpenAI-compatible cached chat-completion orchestration:

- `autogen-agentchat`
- `autogen-ext[openai,diskcache]`
- `ChatCompletionCache`
- `DiskCacheStore`
- `OpenAIChatCompletionClient`

Configure any OpenAI-compatible client from the active Hermes provider route
when possible. For providers with known chat-compatible endpoints, use the
provider's chat-completions base URL and API key. If the selected provider only
has a non-OpenAI-compatible route, fall back to Hermes' native model client.

Do not import a second full agent runtime when the task can be handled by cached
chat map/reduce plus Hermes verification.

## Execution Policy

For codebase scans:

1. Identify the repository root and current git commit.
2. Build an inventory with `git ls-files` or `rg --files`.
3. Exclude credential-like and low-value files:
   - `.env`
   - `auth.json`
   - private keys
   - binary assets
   - lock files unless dependency drift is in scope
4. Hash each shard's input files.
5. Cache shard analyses under:

   ```text
   tmp/hermes-scans/cache/
   ```

6. Spool every worker output under:

   ```text
   tmp/hermes-scans/<scan-id>/task-01.md
   tmp/hermes-scans/<scan-id>/task-02.md
   ...
   ```

7. Aggregate from those files, never from one giant tool response.

## Worker Semantics

If the user asks for `N agents`, run `N` logical workers.

This does not mean all workers must be full Hermes agents or all active at once:

- Broad scan workers may be cached chat calls.
- Verification workers may be Hermes `delegate_task` children.
- Provider-specific active concurrency caps must be respected.

For MiniMax:

- Chat fan-out can be higher.
- Full Hermes agent loops should use the configured active worker cap.
- Avoid synchronized retry storms.

## Cache Keys

Cache model analysis using stable keys that include:

- repo root
- git commit or dirty file hashes
- shard id
- file paths
- file content hashes
- prompt version
- model/provider
- scan focus

If a shard's file hashes and prompt version are unchanged, reuse the cached
analysis unless the user explicitly asks for a cold scan.

## Accuracy Policy

Use cached chat for candidate discovery.

Use Hermes agents for:

- high severity findings
- findings that need file-following across multiple modules
- findings that need tests or reproduction
- ambiguous memory, auth, session, or concurrency issues

The final report must distinguish:

- candidate findings
- verified findings
- discarded false positives
- areas not fully covered

## Output Policy

Write the final report to the user-requested file, commonly:

```text
problems.md
```

Include:

- scan id
- worker count requested
- actual execution mix: cached chat vs Hermes agent verification
- cache hit/miss counts
- active provider caps used
- rate-limit/retry counts
- tests or commands run
- findings with concrete file paths and line numbers
- residual uncertainty

## Fallbacks

If AutoGen is unavailable:

1. Tell the user the optional `code-scan` extra is not installed.
2. Use Hermes' native direct chat/API path when available.
3. Fall back to `delegate_task` with result spooling or small batches.

Do not run a 25-child rich `delegate_task` scan that returns all findings in one
tool response. It can succeed internally but truncate before the parent sees all
results.
