# CCB Batch 1 (commits 1-82) — Gap Analysis vs openclaude

## Summary
- **Total commits analyzed:** 82
- **GAP (OC missing this fix):** 4
- **ALREADY_HAVE (fix already in OC):** 2
- **NOT_APPLICABLE (doc/CI/merge/test/build/CCB-specific):** 76

---

## Detailed per-commit analysis

8fc3ddb6 | feat: 补全依赖 | NOT_APPLICABLE | — | — (package.json, tsconfig.json, .gitignore, bun.lock — dependency/config scaffolding)

c26d614f | feat: 调整依赖 | NOT_APPLICABLE | — | — (RECORD.md, package.json, tsconfig.json — dependency adjustments)

bd756cc3 | feat: 完成stub | NOT_APPLICABLE | — | — (RECORD.md only — documents type-stub progress, no source code changes)

751a684d | feat: 第一个可启动版本 | NOT_APPLICABLE | — | — (RECORD.md + entrypoints/cli.tsx + main.tsx — initial bootstrap, not a bug fix)

3d4cb096 | feat: monorepo 构建完成 | NOT_APPLICABLE | — | — (monorepo packages config, @ant/* packages — CCB build infrastructure)

c4d92178 | feat: 完成大部分操作 | NOT_APPLICABLE | — | — (massive type-fix pass across ~50 files — all CCB-specific decompilation type errors, not discrete bug fixes)

2c759fe6 | feat: 类型修复 | NOT_APPLICABLE | — | — (type fixes in Config.tsx, Spinner.tsx, REPL.tsx, global.d.ts, message.ts, sessionStorage.ts — CCB type cleanup)

4c0a655a | feat: 大规模清理 claude 的类型问题及依赖 | NOT_APPLICABLE | — | — (type/import fixes across ~30 files — CCB bootstrap type cleanup)

d7a729ca | feat: 完成第二版类型清理 | NOT_APPLICABLE | — | — (type fixes across ~25 files — CCB bootstrap type cleanup)

dd9cd782 | feat: 问就是封包 | NOT_APPLICABLE | — | — (package.json, type fixes across ~20 files — packaging/type cleanup)

91f77ea5 | feat: 完成一大波类型修复, 虽然 any 很多 | NOT_APPLICABLE | — | — (type fixes across ~25 files — CCB type cleanup)

58f1bd49 | feat: 加入 TODO; 开始夜间行者模式 | NOT_APPLICABLE | — | — (.gitignore + TODO.md only)

fac9341e | feat: 全面清理类型错误 — tsc 零错误，any 标注全部消除 | NOT_APPLICABLE | — | — (massive type-fix pass across ~70 files — CCB bootstrap, not discrete bug fixes)

7e15974b | feat: 实现 4 个 NAPI 包 — modifiers/image-processor/audio-capture/url-handler | NOT_APPLICABLE | — | — (macOS/Windows native addons — platform-specific, not applicable to OC)

f10d179a | docs: 更新 TODO.md 标记 NAPI 包全部完成 | NOT_APPLICABLE | — | — (TODO.md only)

2de3d309 | feat: 添加 bun 说明 | NOT_APPLICABLE | — | — (docs only)

b1c6249f | docs: 添加说明 | NOT_APPLICABLE | — | — (docs only)

4692c3e2 | docs: 修复命令错误 | NOT_APPLICABLE | — | — (docs only)

074ea844 | feat: 配置 Biome 代码格式化与校验工具 | NOT_APPLICABLE | — | — (biome.json tooling config)

4319afc0 | feat: 配置 git pre-commit hook — 提交前自动运行 Biome 检查 | NOT_APPLICABLE | — | — (git hooks tooling)

1d15e30f | docs: 改进说明 | NOT_APPLICABLE | — | — (docs only)

dc2fdc7c | Merge remote-tracking branch 'origin/main' into feature/prod | NOT_APPLICABLE | — | — (merge commit)

9dd1eeff | feat: 添加 todo | NOT_APPLICABLE | — | — (TODO.md only)

e443a8fa | feat: 搭建单元测试基础设施 — Bun test runner + 示例测试 | NOT_APPLICABLE | — | — (test infrastructure)

17ec716d | feat: 添加 GitHub Actions CI 流水线 | NOT_APPLICABLE | — | — (CI pipeline config)

c587a643 | feat: 添加 knip 冗余代码检查工具 | NOT_APPLICABLE | — | — (tooling config)

173d18be | feat: 添加代码健康度检查脚本 | NOT_APPLICABLE | — | — (scripts only)

b759df5b | docs: 继续更新 | NOT_APPLICABLE | — | — (docs only)

04c8ef2e | docs: 调整样式 | NOT_APPLICABLE | — | — (docs only)

c6491372 | fix: 同步 lock 文件 | NOT_APPLICABLE | — | — (bun.lock only)

30e863c9 | fix: 调优 Biome lint 规则，关闭 formatter 避免大规模代码变更 | NOT_APPLICABLE | — | — (biome.json tooling config)

975b4876 | feat: 实现 @ant/computer-use-input — macOS 键鼠模拟 | NOT_APPLICABLE | — | — (macOS-specific native module)

b51b2d76 | feat: 升级 @ant/computer-use-mcp — 类型安全 stub + sentinel apps | NOT_APPLICABLE | — | — (macOS-specific, @ant packages)

722d59b6 | feat: 实现 @ant/computer-use-swift — macOS JXA/screencapture | NOT_APPLICABLE | — | — (macOS-specific native module)

8f6800f5 | Create SECURITY.md | NOT_APPLICABLE | — | — (docs only)

c57f5a29 | Merge pull request #4 from claude-code-best/feature/prod | NOT_APPLICABLE | — | — (merge commit)

f6fe9446 | docs: mintlify 文档撰写 | NOT_APPLICABLE | — | — (docs only)

ce2f19cc | Merge pull request #5 from claude-code-best/feature/prod | NOT_APPLICABLE | — | — (merge commit)

65d7f199 | chore: 调整配置 | NOT_APPLICABLE | — | — (biome.json + package.json config)

9018c7af | Merge branch 'feature/prod' | NOT_APPLICABLE | — | — (merge commit)

0135ad99 | chore: 更新 lock 文件 | NOT_APPLICABLE | — | — (bun.lock only)

b32dd454 | fix: 修复构建问题 | NOT_APPLICABLE | — | — (Adds #!/usr/bin/env bun shebang to cli.tsx and local feature() polyfill — CCB-specific, OC imports feature from bun:bundle directly)

60411027 | docs: 尝试修复 docs 的位置 | NOT_APPLICABLE | — | — (docs only)

9a57642d | feat: 完成最新的可构建版本 | NOT_APPLICABLE | — | — (README.md whitespace cleanup only)

ecf885d6 | docs: 添加赞助说明 | NOT_APPLICABLE | — | — (docs only)

03cff1b7 | docs: 修正格式 | NOT_APPLICABLE | — | — (docs only)

4233ee7d | docs: 更新文档, 加上配图 | NOT_APPLICABLE | — | — (docs only)

2fa91489 | docs: 新增「揭秘：隐藏功能与内部机制」文档栏目 | NOT_APPLICABLE | — | — (docs only)

33fe4940 | fix: 启用 /loop 命令，移除 feature('AGENT_TRIGGERS') gate | **GAP** | src/tools/ScheduleCronTool/prompt.ts:37 | Removes feature('AGENT_TRIGGERS') ternary gate from isKairosCronEnabled() — OC still has it at line 37, and since OC imports feature from bun:bundle (DCE'd to false in source mode), cron scheduling is permanently disabled. CCB fix makes it always check only CLAUDE_CODE_DISABLE_CRON env var.

2934f300 | fix: 彻底移除 /loop 及 cron 工具的 feature('AGENT_TRIGGERS') gate | **GAP** | src/cli/print.ts:365-376, src/constants/tools.ts:86, src/screens/REPL.tsx:199/4395, src/skills/bundled/index.ts:71, src/tools.ts:29 | Removes feature('AGENT_TRIGGERS') gating from 6 files: cronSchedulerModule/cronJitterConfigModule/cronGate/dynamicLoopModule requires in print.ts, IN_PROCESS_TEAMMATE_ALLOWED_TOOLS in tools.ts, useScheduledTasks hook in REPL.tsx, loop skill registration in bundled/index.ts, and cronTools array in tools.ts. OC still has the feature gate in all 6 locations. In source mode (feature from bun:bundle = false), this means: cron scheduler never starts, cron tools are empty [], loop skill is never registered, and scheduled tasks hook is null.

c5b55c1b | docs: 完成大量文档 | NOT_APPLICABLE | — | — (docs only)

64f79dc3 | feat: 改善 seo | NOT_APPLICABLE | — | — (docs SEO config)

a889ed84 | fix: 移除 Settings 中未定义的 Gates 引用，修复 config 命令报错 | **ALREADY_HAVE** | src/components/Settings/Settings.tsx:104 | Removes `const GatesComponent = Gates as any; t7 = false ? [<Tab key="gates"...` and replaces with `t7 = []`. OC already has `const t7 = [] as React.ReactNode[]` at line 104 — the Gates tab was already stripped.

503a40f4 | docs: 调整一下表达 | NOT_APPLICABLE | — | — (docs only)

7d5271e6 | docs: 更新文档 | NOT_APPLICABLE | — | — (docs only)

8b63e54e | docs: 文档更新 | NOT_APPLICABLE | — | — (docs only)

221fb6eb | fix: 修复 @ typeahead 文件搜索无结果的问题 | **GAP** | src/native-ts/file-index/index.ts:222 | Rewrites search algorithm from greedy-leftmost indexOf to multi-start-position approach. Old code only tried leftmost occurrence of needle[0], so searching "sett" would fail on "src/settings/" because 's' matches early in "src/" and subsequent chars fail. New code collects all word-boundary start positions for needle[0] and tries each, keeping the best score. OC still has the old greedy-leftmost algorithm at line 222-224. Also fixes variable ordering in getFilesUsingGit (cwd before findGitRoot) and brace-style in refresh throttle — both are cosmetic in OC's context (OC's getCwd() calls are already functionally equivalent).

c57e6ee3 | docs: 文档优化完成 | NOT_APPLICABLE | — | — (docs only)

c57ad656 | 支持buddy命令 | **ALREADY_HAVE** | src/commands.ts:88/183/394 | Converts buddy command from feature-gated require to direct import. OC already has buddy working via dual-fallback pattern: `import buddyDirect from './commands/buddy/index.js'` (line 88) + feature-gated require (line 183) + `...(buddy ? [buddy] : [buddyDirect])` (line 394). The added buddy.ts implementation (species labels, stats rendering, companion info) is already present in OC's buddy infrastructure.

f71530a1 | 修复buddy rehatch的问题 | **GAP** | src/buddy/companion.ts:138, src/buddy/types.ts (no seed field) | Bug: re-hatching a buddy always produces the same companion because it's based on companionUserId() which never changes. Fix: generates a random seed string (generateSeed()), stores it on the companion soul (seed field in types), and uses rollWithSeed(seed) instead of roll(companionUserId()) for re-hatch. getCompanion() uses stored.seed ?? companionUserId() for loading. OC missing generateSeed(), seed field in CompanionSoul, and seed-based hatching logic — re-hatch is deterministic (always same species/rarity).

8e9933ee | Merge branch 'claude-code-best:main' into main | NOT_APPLICABLE | — | — (merge commit)

3b0a5e48 | docs: 更新说明文档 | NOT_APPLICABLE | — | — (docs only)

a426a50c | docs: 完善测试文档编写 | NOT_APPLICABLE | — | — (docs only)

67baea3c | test: 添加 Tool 系统单元测试 (测试计划 01) | NOT_APPLICABLE | — | — (tests only)

cad6409b | test: 添加 Utils 纯函数单元测试 (测试计划 02) | NOT_APPLICABLE | — | — (tests only)

c4344c4d | test: 添加 Context 构建单元测试 (测试计划 03) | NOT_APPLICABLE | — | — (tests only)

583d0433 | test: 添加权限规则解析器单元测试 (测试计划 04) | NOT_APPLICABLE | — | — (tests only)

25839ab4 | test: 添加模型路由单元测试 (测试计划 05) | NOT_APPLICABLE | — | — (tests only)

f81a767f | test: 添加 Cron 调度单元测试 (测试计划 07) | NOT_APPLICABLE | — | — (tests only)

3df4b95f | test: 添加 Git 工具函数单元测试 (测试计划 08) | NOT_APPLICABLE | — | — (tests only)

18342136 | test: 添加配置与设置系统单元测试 (测试计划 09) | NOT_APPLICABLE | — | — (tests only)

c57950e1 | test: 添加消息处理单元测试 (测试计划 06) | NOT_APPLICABLE | — | — (tests only)

fd2ad71a | docs: 更新测试规范，记录当前 517 个测试的覆盖状态 | NOT_APPLICABLE | — | — (docs only)

43af2603 | test: 添加 json/truncate/path/tokens 模块测试 | NOT_APPLICABLE | — | — (tests only)

a28a44f9 | test: 添加 FileEditTool/permissions/filterToolsByDenyRules 测试 | NOT_APPLICABLE | — | — (tests only)

0d890796 | docs: 更新测试覆盖状态至 647 tests / 32 files | NOT_APPLICABLE | — | — (docs only)

717cc551 | docs: 更改 readme | NOT_APPLICABLE | — | — (docs only)

91c5bea2 | docs: 添加后续测试覆盖计划 (Phase 1-4) | NOT_APPLICABLE | — | — (docs only)

2ca56977 | Merge pull request #30 from claude-code-best/test/test-most-core-func | NOT_APPLICABLE | — | — (merge commit)

acfaac5f | test: Phase 1 — 添加 8 个纯函数测试文件 (+134 tests) | NOT_APPLICABLE | — | — (tests only)

2d9c2adc | docs: 排查 test 文件夹 | NOT_APPLICABLE | — | — (docs only)

21ac9e44 | test: Phase 2-4 — 添加 12 个测试文件 (+321 tests, 968 total) | NOT_APPLICABLE | — | — (tests only)

---

## GAP Details

### GAP 1: 33fe4940 — ScheduleCronTool prompt.ts AGENT_TRIGGERS gate
- **OC file:** `src/tools/ScheduleCronTool/prompt.ts:37`
- **Bug:** `isKairosCronEnabled()` returns `false` when `feature('AGENT_TRIGGERS')` is false (all source-mode runs)
- **Fix:** Remove the feature gate ternary, always check CLAUDE_CODE_DISABLE_CRON env var
- **OC status:** Still has `return feature('AGENT_TRIGGERS') ? !isEnvTruthy(...) && getFeatureValue_CACHED_WITH_REFRESH(...) : false`

### GAP 2: 2934f300 — Complete AGENT_TRIGGERS gate removal (6 files)
- **OC files:**
  - `src/cli/print.ts:365-376` — cron module requires gated to null
  - `src/constants/tools.ts:86` — cron tool names excluded from IN_PROCESS_TEAMMATE_ALLOWED_TOOLS
  - `src/screens/REPL.tsx:199,4395` — useScheduledTasks null + conditional call
  - `src/skills/bundled/index.ts:71` — registerLoopSkill() gated
  - `src/tools.ts:29` — cronTools array empty
- **Fix:** Remove all feature('AGENT_TRIGGERS') gates, load modules unconditionally

### GAP 3: 221fb6eb — @ typeahead file search
- **OC file:** `src/native-ts/file-index/index.ts:222`
- **Bug:** Greedy-leftmost indexOf for first needle char causes false negatives when the first char appears early in path (e.g., 's' matches "src/" before "settings/")
- **Fix:** Collect all word-boundary start positions for needle[0] and try each, keeping best score
- **OC status:** Still has the old greedy-leftmost algorithm

### GAP 4: f71530a1 — Buddy rehatch always produces same companion
- **OC files:** `src/buddy/companion.ts:138`, `src/buddy/types.ts`
- **Bug:** Re-hatching uses `roll(companionUserId())` which is deterministic — always same species/rarity
- **Fix:** Add `generateSeed()` random seed, store `seed` field on CompanionSoul, use `rollWithSeed(stored.seed ?? companionUserId())` in getCompanion()
- **OC status:** Missing generateSeed(), seed type field, and seed-based re-hatch logic
