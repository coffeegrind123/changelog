Audit all 587 Gitlawb commits (github.com/Gitlawb/openclaude, main branch, oldest-first, skip initial d2542c9) against openclaude. Pure research — document every fix gap into a single file. No openclaude code edits.

### Infrastructure (already set up)
- Gitlawb repo: /tmp/gitlawb-openclaude (already cloned)
- Openclaude src: /home/openclaudeuser/openclaude/src/
- Tracking file: /tmp/changelog-repo/gitlawb-fix-audit.md (skeleton ready)
- Push: cd /tmp/changelog-repo && git -c credential.helper=/tmp/git-cred-helper.sh push
- OC branch: ccb-fix-port (or create gitlawb-fix-port)

### Protocol (per commit)
1. git show <sha> 2>&1 | head -100 — read Gitlawb diff
2. If doc/CI/merge/version-bump/test/build-only → NOT_APPLICABLE, next
3. If source change: Read the openclaude file at /home/openclaudeuser/openclaude/src/
4. Compare — is the same bug present? Is the fix already applied?
5. Verdict: GAP (missing) / ALREADY_HAVE / NOT_APPLICABLE
6. For each GAP: add row to gitlawb-fix-audit.md with SHA, date, subject, OC files, what to fix, priority

### Approach
Launch 8 agents, each processing ~73 commits. After all complete, compile results into the master tracking file, commit, push.

### Agent batch commands
Batch 1:  git log --oneline --reverse main | tail -n +2 | sed -n '1,73p'
Batch 2:  git log --oneline --reverse main | tail -n +2 | sed -n '74,146p'
Batch 3:  git log --oneline --reverse main | tail -n +2 | sed -n '147,219p'
Batch 4:  git log --oneline --reverse main | tail -n +2 | sed -n '220,292p'
Batch 5:  git log --oneline --reverse main | tail -n +2 | sed -n '293,365p'
Batch 6:  git log --oneline --reverse main | tail -n +2 | sed -n '366,438p'
Batch 7:  git log --oneline --reverse main | tail -n +2 | sed -n '439,511p'
Batch 8:  git log --oneline --reverse main | tail -n +2 | sed -n '512,587p'

### Gitlawb-specific notes
- Gitlawb is ALSO a fork of the same upstream Claude Code source as openclaude and CCB
- Gitlawb uses an "OpenAI-compatible provider shim" for multi-provider support — this is their equivalent of our openaiBridge
- Their provider shim is in packages/openai-shim/ (separate from our src/services/api/openaiBridge/)
- Many Gitlawb commits will be their own feature additions or shim-specific fixes — mark these NOT_APPLICABLE
- Gitlawb may have fixed bugs that exist in openclaude's equivalent code paths — those ARE gaps
- Gitlawb has its own MCP server set (different from ours), its own auto-update mechanism, its own CLI entrypoints
- Pay special attention to: Bash security fixes, hook fixes, permission fixes, memory leak fixes, provider-agnostic fixes

---

### Agent 1 (commits 1-73)

CRITICAL PROTOCOL — find fixes openclaude is MISSING. Research only, NO edits.

Working dirs: Gitlawb at /tmp/gitlawb-openclaude, openclaude at /home/openclaudeuser/openclaude/src/

Get your commits:
  cd /tmp/gitlawb-openclaude && git log --oneline --reverse main | tail -n +2 | sed -n '1,73p'

For EVERY commit:
1. git show <sha> 2>&1 | head -100 — read the Gitlawb diff
2. EXTRACT CHANGED FILES from the diff header
3. If ALL changed files are doc/CI/config/merge/version/test/build-only → NOT_APPLICABLE
4. If source change: Read() the openclaude file at /home/openclaudeuser/openclaude/src/ at the relevant lines
5. Compare Gitlawb's fixed code vs openclaude's current code
6. Verdict: GAP / ALREADY_HAVE / NOT_APPLICABLE

IMPORTANT: You MUST actually Read() the openclaude source files. Do NOT skip this step.

OUTPUT FORMAT (one line per commit):
  SHA | SUBJECT | VERDICT | OC_FILE:LINE | WHAT_THE_FIX_DOES

At the end, add:
## Summary
Total: N. GAP: X, ALREADY_HAVE: Y, NOT_APPLICABLE: Z.

### GAPs found:
1. **SHA** — description. OC file: path:line. Fix: what to change.

Write complete output to /tmp/gitlawb-gap-batch1.md
DO NOT edit openclaude files. Research only.

### Agent 2 (commits 74-146)

CRITICAL PROTOCOL — find fixes openclaude is MISSING. Research only, NO edits.

Working dirs: Gitlawb at /tmp/gitlawb-openclaude, openclaude at /home/openclaudeuser/openclaude/src/
Get commits: cd /tmp/gitlawb-openclaude && git log --oneline --reverse main | tail -n +2 | sed -n '74,146p'

For EVERY commit:
1. git show <sha> 2>&1 | head -100
2. If doc/CI/merge/version/test/build → NOT_APPLICABLE
3. If source change: Read() openclaude file at the relevant lines, compare → GAP / ALREADY_HAVE / NOT_APPLICABLE

IMPORTANT: You MUST Read() the openclaude source files. Do NOT skip this step.

Output: SHA | SUBJECT | VERDICT | OC_FILE:LINE | NOTES per commit.
Write to /tmp/gitlawb-gap-batch2.md. NO edits to openclaude.

### Agent 3 (commits 147-219)

CRITICAL PROTOCOL — find fixes openclaude is MISSING. Research only, NO edits.

Working dirs: Gitlawb at /tmp/gitlawb-openclaude, openclaude at /home/openclaudeuser/openclaude/src/
Get commits: cd /tmp/gitlawb-openclaude && git log --oneline --reverse main | tail -n +2 | sed -n '147,219p'

For EVERY commit:
1. git show <sha> 2>&1 | head -100
2. If doc/CI/merge/version/test/build → NOT_APPLICABLE
3. If source change: Read() openclaude file, compare → GAP / ALREADY_HAVE / NOT_APPLICABLE

IMPORTANT: You MUST Read() the openclaude source files. Do NOT skip this step.

Output: SHA | SUBJECT | VERDICT | OC_FILE:LINE | NOTES
Write to /tmp/gitlawb-gap-batch3.md. NO edits to openclaude.

### Agent 4 (commits 220-292)

CRITICAL PROTOCOL — find fixes openclaude is MISSING. Research only, NO edits.

Working dirs: Gitlawb at /tmp/gitlawb-openclaude, openclaude at /home/openclaudeuser/openclaude/src/
Get commits: cd /tmp/gitlawb-openclaude && git log --oneline --reverse main | tail -n +2 | sed -n '220,292p'

For EVERY commit:
1. git show <sha> 2>&1 | head -100
2. If doc/CI/merge/version/test/build → NOT_APPLICABLE
3. If source change: Read() openclaude file, compare → GAP / ALREADY_HAVE / NOT_APPLICABLE

IMPORTANT: You MUST Read() the openclaude source files. Do NOT skip this step.

Output: SHA | SUBJECT | VERDICT | OC_FILE:LINE | NOTES
Write to /tmp/gitlawb-gap-batch4.md. NO edits to openclaude.

### Agent 5 (commits 293-365)

CRITICAL PROTOCOL — find fixes openclaude is MISSING. Research only, NO edits.

Working dirs: Gitlawb at /tmp/gitlawb-openclaude, openclaude at /home/openclaudeuser/openclaude/src/
Get commits: cd /tmp/gitlawb-openclaude && git log --oneline --reverse main | tail -n +2 | sed -n '293,365p'

For EVERY commit:
1. git show <sha> 2>&1 | head -100
2. If doc/CI/merge/version/test/build → NOT_APPLICABLE
3. If source change: Read() openclaude file, compare → GAP / ALREADY_HAVE / NOT_APPLICABLE

IMPORTANT: You MUST Read() the openclaude source files. Do NOT skip this step.

Output: SHA | SUBJECT | VERDICT | OC_FILE:LINE | NOTES
Write to /tmp/gitlawb-gap-batch5.md. NO edits to openclaude.

### Agent 6 (commits 366-438)

CRITICAL PROTOCOL — find fixes openclaude is MISSING. Research only, NO edits.

Working dirs: Gitlawb at /tmp/gitlawb-openclaude, openclaude at /home/openclaudeuser/openclaude/src/
Get commits: cd /tmp/gitlawb-openclaude && git log --oneline --reverse main | tail -n +2 | sed -n '366,438p'

For EVERY commit:
1. git show <sha> 2>&1 | head -100
2. If doc/CI/merge/version/test/build → NOT_APPLICABLE
3. If source change: Read() openclaude file, compare → GAP / ALREADY_HAVE / NOT_APPLICABLE

IMPORTANT: You MUST Read() the openclaude source files. Do NOT skip this step.

Output: SHA | SUBJECT | VERDICT | OC_FILE:LINE | NOTES
Write to /tmp/gitlawb-gap-batch6.md. NO edits to openclaude.

### Agent 7 (commits 439-511)

CRITICAL PROTOCOL — find fixes openclaude is MISSING. Research only, NO edits.

Working dirs: Gitlawb at /tmp/gitlawb-openclaude, openclaude at /home/openclaudeuser/openclaude/src/
Get commits: cd /tmp/gitlawb-openclaude && git log --oneline --reverse main | tail -n +2 | sed -n '439,511p'

For EVERY commit:
1. git show <sha> 2>&1 | head -100
2. If doc/CI/merge/version/test/build → NOT_APPLICABLE
3. If source change: Read() openclaude file, compare → GAP / ALREADY_HAVE / NOT_APPLICABLE

IMPORTANT: You MUST Read() the openclaude source files. Do NOT skip this step.

Output: SHA | SUBJECT | VERDICT | OC_FILE:LINE | NOTES
Write to /tmp/gitlawb-gap-batch7.md. NO edits to openclaude.

### Agent 8 (commits 512-587)

CRITICAL PROTOCOL — find fixes openclaude is MISSING. Research only, NO edits.

Working dirs: Gitlawb at /tmp/gitlawb-openclaude, openclaude at /home/openclaudeuser/openclaude/src/
Get commits: cd /tmp/gitlawb-openclaude && git log --oneline --reverse main | tail -n +2 | sed -n '512,587p'

For EVERY commit:
1. git show <sha> 2>&1 | head -100
2. If doc/CI/merge/version/test/build → NOT_APPLICABLE
3. If source change: Read() openclaude file, compare → GAP / ALREADY_HAVE / NOT_APPLICABLE

IMPORTANT: You MUST Read() the openclaude source files. Do NOT skip this step.

Output: SHA | SUBJECT | VERDICT | OC_FILE:LINE | NOTES
Write to /tmp/gitlawb-gap-batch8.md. NO edits to openclaude.

---

### Compilation prompt (after all agents complete)

All 8 audit agents have completed. Compile results:

1. Read /tmp/gitlawb-gap-batch1.md through /tmp/gitlawb-gap-batch8.md
2. Extract every GAP entry (not ALREADY_HAVE, not NOT_APPLICABLE)
3. Read /tmp/changelog-repo/gitlawb-fix-audit.md for the current skeleton
4. Classify GAPs into priority tiers:
   - CRITICAL: memory leaks, crashes, API 400 errors, security issues, broken core features
   - HIGH: missing guards/params, feature gaps, unbounded growth, architectural divergence
   - MEDIUM: correctness fixes, optimizations, UX improvements
   - LOW: minor polish, model name updates, cosmetic fixes
5. Add all GAP entries to the GAP Catalog tables with SHA, batch#, subject, OC file(s), what to fix
6. Add all ALREADY_HAVE entries to the ALREADY_HAVE table
7. Update the Audit Progress table (mark all batches done with counts)
8. Copy all 8 batch files to /tmp/changelog-repo/
9. Commit and push to changelog repo:
   cd /tmp/changelog-repo && git add -A && git commit -m "Gitlawb fix audit: N GAPs" && git -c credential.helper=/tmp/git-cred-helper.sh push
