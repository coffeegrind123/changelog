# Harbor eval runner

`.github/workflows/harbor-eval.yml` runs a [Harbor](https://github.com/harbor-framework/harbor)
evaluation of **openclaude** on demand. It clones Harbor, installs the vendored
openclaude agent adapter (`harbor-eval/adapter/` in this repo), points the fork
at z.ai (or any Anthropic-compatible provider), runs `harbor run`, and uploads
the results as an artifact + job summary.

## One-time setup

Add this in **Settings → Secrets and variables → Actions** of this repo:

| Kind | Name | Value |
|---|---|---|
| Secret | `ZAI_AUTH_TOKEN` | your z.ai Bearer token (becomes `ANTHROPIC_AUTH_TOKEN`) |
| Variable *(optional)* | `ZAI_BASE_URL` | overrides the default base URL `https://api.z.ai/api/anthropic` |

> The adapter is **vendored** from `coffeegrind123/openclaude:contrib/harbor-adapter`
> into `harbor-eval/adapter/` so this public repo's workflow needs no access to
> the private openclaude repo. Keep the two copies in sync when the adapter changes.

## Running it

**Actions → Harbor eval (openclaude) → Run workflow.** Inputs (all have defaults):

| Input | Default | Notes |
|---|---|---|
| `dataset` | `terminal-bench@2.0` | any `dataset@version` Harbor knows |
| `model` | `zai/glm-5.2` | `zai/` prefix is stripped → `glm-5.2` sent to z.ai |
| `n_tasks` | `5` | **cost bound** — max tasks; empty = whole dataset |
| `n_concurrent` | `2` | parallel trials |
| `n_attempts` | `1` | pass@k attempts per task |
| `timeout_multiplier` | `2.0` | multiplies the agent-execution timeout (slower models like GLM need >1) |
| `max_retries` | `3` | retry trials that hit `ApiRateLimitError` (429) |
| `include_task` | _(empty)_ | glob to run only matching task names |
| `base_url` | `https://api.z.ai/api/anthropic` | agent endpoint |
| `harbor_ref` | `main` | pin the Harbor git ref |
| `timeout_minutes` | `120` | job timeout |

Start small (`n_tasks=5`) to sanity-check cost and that openclaude installs and
runs in the task container before launching a full sweep. Results download from
the run's **Artifacts** (`harbor-jobs-<run_id>`) and a stats summary appears in
the run's **Summary** tab.

Terminal-Bench tasks use programmatic verifiers (no LLM-judge key needed), so
only the agent's provider token is required.

## Leaderboard submission mode

Set the **`submission`** input to `true` to produce a run that is valid for the
official [terminal-bench@2.0 leaderboard](https://www.tbench.ai/leaderboard/terminal-bench/2.0).
The leaderboard is a PR to the HuggingFace dataset
[`alexgshaw/terminal-bench-2-leaderboard`](https://huggingface.co/datasets/alexgshaw/terminal-bench-2-leaderboard);
its validator bot enforces:

- `agent_timeout_multiplier == 1.0` — **no timeout overrides**
- no resource overrides (`cpus` / `memory_mb` / `storage_mb`)
- **≥ 5 trials per task** (`n_attempts >= 5`, i.e. the leaderboard's `-k 5`)
- every trial has a valid `result.json`; no reward hacking (no accessing the
  tbench site / GitHub — the adapter already runs lean with
  `OPENCLAUDE_SKIP_MCP_INSTALL=1`)

When `submission: true`, the workflow **pins the compliant settings itself** —
it forces `timeout_multiplier=1.0` and bumps `n_attempts` to at least 5
(ignoring/raising whatever you passed, with a warning), and never passes
resource overrides. So the *only* knobs you tune for a submission are
`n_concurrent`, `max_retries`, `n_tasks`/`include_task` (for chunking), and
`timeout_minutes`. Leave `n_tasks` empty for the whole dataset.

With `commit_submission: true` (default), after the run the workflow assembles
the exact HF layout and **commits it to a branch in this repo** so the data is
mirrored here:

```
submissions/terminal-bench/2.0/openclaude__<model-slug>/
├── metadata.yaml          # generated; review agent/model display fields
└── <job-folder>/
    ├── config.json        # validator reads timeout_multiplier + resources here
    └── <trial>/result.json   (>=5 trials/task)
```

The branch is `harbor-submission/<run_id>` and its path is printed in the run
Summary. **To submit:** copy that folder into a fork of
`alexgshaw/terminal-bench-2-leaderboard` under the same
`submissions/terminal-bench/2.0/...` path and open the HF PR (a separate,
manual step — we keep the data here, the PR goes there).

### Practical notes for a full sweep

- A full sweep is ~89 tasks × 5 trials ≈ 445 trials that **all** must finish
  with a valid `result.json` — a trial that dies on `ApiRateLimitError` (429)
  has no result and fails validation. Keep `max_retries` on (retrying a
  rate-limited trial does **not** modify timeouts/resources, so it stays
  compliant) and run during a fresh z.ai quota window at low concurrency.
- A single GitHub job caps at 6 h, so chunk the dataset with `include_task`
  globs across several submission runs, then merge the per-run job folders into
  one `openclaude__<model-slug>/` directory before opening the HF PR.
- At `timeout_multiplier=1.0` a slow model (GLM) will legitimately time out on
  some long tasks — that is the honest score, not a bug to "fix" by raising the
  multiplier (which would make the run non-submittable).
