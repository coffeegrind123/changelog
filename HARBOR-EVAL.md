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
| Variable *(optional)* | `ZAI_BASE_URL` | overrides the default base URL `https://api.z.ai/anthropic` |

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
| `n_concurrent` | `3` | parallel trials |
| `n_attempts` | `1` | pass@k attempts per task |
| `include_task` | _(empty)_ | glob to run only matching task names |
| `base_url` | `https://api.z.ai/anthropic` | agent endpoint |
| `harbor_ref` | `main` | pin the Harbor git ref |
| `timeout_minutes` | `120` | job timeout |

Start small (`n_tasks=5`) to sanity-check cost and that openclaude installs and
runs in the task container before launching a full sweep. Results download from
the run's **Artifacts** (`harbor-jobs-<run_id>`) and a stats summary appears in
the run's **Summary** tab.

Terminal-Bench tasks use programmatic verifiers (no LLM-judge key needed), so
only the agent's provider token is required.
