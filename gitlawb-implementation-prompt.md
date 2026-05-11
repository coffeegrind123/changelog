# Gitlawb implementation pass — session prompt

The Gitlawb audit research is **complete** (see `gitlawb-fix-audit.md`,
~93 GAPs across CRITICAL/HIGH/MEDIUM/LOW). This session is the
**implementation pass** — port the gap-list into openclaude using the same
methodology proven on the CCB audit:

- Land each fix as a focused commit on `main`
- Hot-patch the running interactive container after every edit
- Smoke-test against z.ai before committing
- Update `CHANGELOG.md` for each commit (one bullet per commit)
- After every push, do a "trust-but-verify" pass against
  `https://github.com/Gitlawb/openclaude` to catch architectural
  divergence skips that should actually be ports
- Document SKIP / VERIFIED-SKIP / DEFERRED with reasons next to landed
  commit SHAs

## Reference docs to read first

1. `gitlawb-fix-audit.md` — the gap catalog (this session's worklist)
2. `gitlawb-gap-batch{1..8}.md` — per-batch raw research (look here when
   the audit's one-line description isn't enough)
3. `ccb-fix-audit.md` — the *previous* implementation pass; mimic the
   "Implementation Status" section format for Gitlawb when done
4. `coffeegrind123/openclaude:CLAUDE.md` — fork conventions, especially:
   - `bun:bundle` vs `bundle` import semantics (DCE traps)
   - Hot-patch protocol: `docker cp <file> openclaude-interactive:...`
   - `<sha>` ↔ `coffeegrind123/changelog:CHANGELOG.md` requirement

## Workflow per gap (matches CCB pass)

```
1. Read gap row → understand fix
2. Read OC source at the cited file:line to confirm gap
3. Edit
4. bun build src/entrypoints/cli.tsx --target=bun  (must exit 0)
5. docker cp <file> openclaude-interactive:/opt/openclaude-src/<file>
6. docker exec openclaude-interactive bash -c \
     'cd /opt/openclaude-src && IS_SANDBOX=1 timeout 30 bun run \
      src/entrypoints/cli.tsx -p "say ok" --dangerously-skip-permissions'
7. git add <file> && git commit -m "..."
8. Edit /tmp/changelog-repo/CHANGELOG.md (today's section, top of file)
9. cd /tmp/changelog-repo && git pull --rebase && git add CHANGELOG.md \
     && git commit && git push
10. git push
```

Batch related fixes into one commit when they touch the same file or
share a theme — keeps the changelog readable. Examples from CCB pass:
`1594427` (3 unrelated safety fixes batched), `e2940e0` (5 MEDIUM
ports across 5 different files).

## Trust-but-verify pass (do once near the end)

```
git clone --depth 1 https://github.com/Gitlawb/openclaude.git /tmp/gitlawb
```

For every architectural-divergence SKIP, check Gitlawb's actual source
to verify the divergence claim. Convert to LANDED port when the actual
implementation is more applicable than the audit's one-line description
suggested. The CCB pass upgraded 3 of 7 skips to ports this way.

## When done

Update `gitlawb-fix-audit.md` with an "Implementation Status" section
mirroring the CCB doc — per-gap rows with status + commit SHA, plus
chronological commits-to-items index. Then delete the per-batch files
(`gitlawb-gap-batch{1..8}.md`) the same way we did for CCB, leaving
only the consolidated audit doc.

## Things to watch out for (Gitlawb-specific)

- Gitlawb's "OpenAI-compatible provider shim" lives in
  `packages/openai-shim/` — fundamentally different layer from our
  `src/services/api/openaiBridge/`. Many Gitlawb fixes target their
  shim and have no analog in our tree.
- Gitlawb has its own MCP server set, auto-update mechanism, CLI
  entrypoints — fixes targeting those subsystems should SKIP.
- We've already adopted some Gitlawb features per CLAUDE.md
  ("Hook Chains" §15, "AutoFix" §15) — gaps that point at code we
  already ported are likely already addressed.
- High-value fix categories: Bash security validators, hook lifecycle
  fixes, permission system fixes, memory leak fixes, provider-agnostic
  bug fixes (apply to all providers, not shim-specific).

## Suggested entry prompt for the next session

> Read `coffeegrind123/changelog:gitlawb-fix-audit.md` and start the
> Gitlawb implementation pass. Work through CRITICAL → HIGH → MEDIUM →
> LOW. Follow the workflow in `gitlawb-implementation-prompt.md`. Do a
> trust-but-verify pass against `github.com/Gitlawb/openclaude` before
> calling it done. Update `gitlawb-fix-audit.md` with an Implementation
> Status section when finished and tidy the per-batch files.
