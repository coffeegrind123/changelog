# CCB Batch 6 Gap Analysis (commits 411–492 in reverse main log)
# Analyzed 2026-05-11

## Format: SHA | SUBJECT | VERDICT | OC_FILE:LINE | NOTES

c7e1c50b | feat: 添加服务层增强与零散改进 | ALREADY_HAVE | Multiple files | History parseInt radix + yoga-layout lint fixes; openclaude already has equivalent fixes; langfuse test additions are CCB-specific
7881cc61 | feat: 增强 ACP 桥接与权限处理 | NOT_APPLICABLE | N/A | ACP test coverage expansion only, no functional source changes to core logic
d208855f | feat: 添加 builtin-tools 增强与测试覆盖 | NOT_APPLICABLE | N/A | Mostly test additions + CCB-specific spawnMultiAgent refactor; openclaude has its own forkSubagent implementation
23bb09d2 | feat: 添加 model/provider 层改进 | GAP | src/utils/model/model.ts | Default model bumped to Opus 4.7; removed fallback recursion guards (isAliasOrAliasWithSuffix). openclaude still uses opus46 defaults
23fcbf90 | feat: 添加 UI 组件增强与测试覆盖 | NOT_APPLICABLE | N/A | EffortIndicator + FrustrationDetection UI test coverage; CCB-specific FrustrationDetection differs from openclaude
f43350e6 | fix: 修复 4 个测试失败 | NOT_APPLICABLE | N/A | Test fixes only (path normalization, SDK signature changes, empty message guards)
4e82fb59 | Merge PR #330 | NOT_APPLICABLE | N/A | Merge commit
7ea69ca2 | fix: 修复 build 过程中的问题 | NOT_APPLICABLE | N/A | Build system fix
1173a623 | refactor: 统一测试 mock | NOT_APPLICABLE | N/A | Test infrastructure refactor
93bfdabf | feat: 添加 Exa AI 搜索适配器 | NOT_APPLICABLE | N/A | Exa AI is CCB-specific search provider; openclaude uses WebSearch/WebFetch via own adapters
7d4c4278 | fix: highlight.js 静态导入 | NOT_APPLICABLE | N/A | Build change for Bun --compile compatibility (CCB's build tooling)
c3d63c8f | chore: 添加 release 脚本 | NOT_APPLICABLE | N/A | Chore
b966eef5 | Merge branch 'main' into feature/exa-search | NOT_APPLICABLE | N/A | Merge commit
78118886 | Merge PR #333 | NOT_APPLICABLE | N/A | Merge commit
b642977a | Merge PR #335 | NOT_APPLICABLE | N/A | Merge commit
7a3fdf6e | chore: 1.9.0 | NOT_APPLICABLE | N/A | Version bump
299953b0 | fix: cliHighlight 类型不兼容问题 | NOT_APPLICABLE | N/A | CCB-specific cliHighlight module; openclaude doesn't ship this feature
85e5a8cf | chore: 贡献者更新工作流 | NOT_APPLICABLE | N/A | CI chore
9624f880 | fix: 第三方 Anthropic base URL 应使用 ExaSearchAdapter | NOT_APPLICABLE | N/A | CCB-specific ExaSearchAdapter; openclaude uses its own WebSearchTool adapter selection
cfe1552e | ci: 统一 typecheck 命令 | NOT_APPLICABLE | N/A | CI
a92af994 | ci: GitHub Release 和 changelog | NOT_APPLICABLE | N/A | CI
047634af | ci: 删除冗余 release 工作流 | NOT_APPLICABLE | N/A | CI
792777d6 | chore: 1.9.1 | NOT_APPLICABLE | N/A | Version bump
5bc12b00 | chore: 更新版本流水线 | NOT_APPLICABLE | N/A | Chore
fc7a85f5 | chore: 1.9.2 | NOT_APPLICABLE | N/A | Version bump
ca1c87f4 | fix: usePipeIpc require 返回 undefined 崩溃 | GAP | src/hooks/usePipeIpc.ts:22-37 | CCB changed lazy require() functions to static imports to fix crash. openclaude still uses lazy require() pattern. Low impact (Bun runtime handles require fine) but structurally diverged
7a0dd305 | chore: 1.9.3 | NOT_APPLICABLE | N/A | Version bump
0b304730 | docs: DEFAULT_BUILD_FEATURES 注释 | NOT_APPLICABLE | N/A | Docs only
4dcbaf1e | fix: ACP messageSelector require 失败导致 submitMessage 崩溃 | GAP | src/QueryEngine.ts:87-89 | CCB wraps messageSelector require() in try/catch + null checks at call sites. openclaude has unprotected lazy require
f2dd5142 | refactor: 解耦 BRIDGE_MODE 与 DAEMON | ALREADY_HAVE | src/commands.ts:108 | CCB disables DAEMON feature flag and decouples BRIDGE_MODE from DAEMON. openclaude has DAEMON enabled (all flags true) so no practical gap
2a5b2636 | chore: 1.9.4 | NOT_APPLICABLE | N/A | Version bump
02ab1a03 | docs: Bun 安装说明 | NOT_APPLICABLE | N/A | Docs only
03811f97 | feat: 实现 SSH Remote | ALREADY_HAVE | src/ssh/ | Already ported (see CLAUDE.md SSH Remote section). CCB's original implementation
95bb1919 | Merge PR #341 | NOT_APPLICABLE | N/A | Merge commit
5582bb47 | docs: 五一 lint 提示 | NOT_APPLICABLE | N/A | Docs only
3c55a8c8 | Merge PR #344 | NOT_APPLICABLE | N/A | Merge commit
eadd32ae | docs: 同步 AGENTS.md 与 CLAUDE.md | NOT_APPLICABLE | N/A | Docs only
eb833da3 | fix: 创建 agent 后刷新 loadMarkdownFilesForSubdir 缓存 | GAP | src/tools/AgentTool/loadAgentsDir.ts:395-398 | CCB clears loadMarkdownFilesForSubdir.cache in clearAgentDefinitionsCache(). openclaude only clears getAgentDefinitionsWithOverrides.cache + clearPluginAgentCache()
9d35f98e | feat: 启用 SKILL_LEARNING 编译开关 | NOT_APPLICABLE | N/A | CCB build config (scripts/defines.ts); openclaude has own build system
d09f3634 | Merge PR #347 | NOT_APPLICABLE | N/A | Merge commit
5125a159 | docs: correct Bun post-install | NOT_APPLICABLE | N/A | Docs only
d4223abc | Merge PR #1 | NOT_APPLICABLE | N/A | Merge commit
017c251f | docs: clarify bun setup | NOT_APPLICABLE | N/A | Docs only
8613d558 | Merge PR #350 | NOT_APPLICABLE | N/A | Merge commit
da6d0636 | fix: 修复 anthropic 煞笔的四个 bug | MULTI | Multiple files | (1) FileEdit/FileWrite read-before-edit removal: GAP (openclaude keeps restriction per "Don't Touch" policy). (2) DeepSeek thinking detection: GAP (openclaude uses different openaiBridge). (3) Opus effort default: ALREADY_HAVE. (4) Teach-me notes: NOT_APPLICABLE (docs)
047c85fc | fix: DeepSeek V4 reasoning_content 回传 400 错误 | NOT_APPLICABLE | N/A | CCB's fix in teach-me + specific test files; openclaude uses own openaiBridge provider-agnostic DeepSeek support
e0c8e9da | chore: 添加学习文件夹 | NOT_APPLICABLE | N/A | Chore
e38d4546 | fix: Windows Node.js stdin.ref() 泄漏 | NOT_APPLICABLE | N/A | Windows/Node.js-specific; openclaude runs on Bun/Linux
c07ad4c7 | chore: 清理仓库审计问题 | NOT_APPLICABLE | N/A | Chore (CLAUDE.md + unused stubs cleanup)
b0a3ef90 | chore: 1.9.5 | NOT_APPLICABLE | N/A | Version bump
ad09f38f | fix: 斜杠命令补全 Tab 覆盖问题 | GAP | src/hooks/useTypeahead.tsx | CCB uses commandInput (= value substring to cursor) to fix mid-line command completion + splices at cursor. openclaude uses full value string
2e7fc428 | feat: 集成豆包 ASR 语音识别 | NOT_APPLICABLE | N/A | CCB-specific Chinese speech recognition backend (doubao); openclaude has own local faster-whisper STT
7a3cc24a | fix: nodejs windows 环境 UDS | NOT_APPLICABLE | N/A | Node.js/Windows-specific UDS messaging fix
1c3b280c | fix: 多轮对话缓存失效 skill 提升 | GAP | src/utils/attachments.ts | CCB adds skill discovery dedup across turns. openclaude needs equivalent cache-busting. Needs deeper investigation
a8ed0cdc | fix: vendor 二进制路径解析错误 | NOT_APPLICABLE | N/A | CCB build tooling fix (Vite dist/chunks/); openclaude uses Bun build
e8ef955f | docs: /login 说明 | NOT_APPLICABLE | N/A | Docs only
d03af7bd | chore: 1.10.0 | NOT_APPLICABLE | N/A | Version bump
9e61e7a9 | chore: 更新 biome 注释 | NOT_APPLICABLE | N/A | Chore
e4403ff0 | fix: 移除 RCS machineName 复用逻辑 | NOT_APPLICABLE | N/A | CCB-specific RCS (remote control server) store change; openclaude has own CCR server
6585d0f6 | fix: 禁用 COORDINATOR_MODE 和 TEAMMEM | NOT_APPLICABLE | N/A | CCB disables these feature flags for memory reasons; openclaude keeps both enabled
e0ca1d05 | chore: 1.10.2 | NOT_APPLICABLE | N/A | Version bump
cf33c060 | feat: deepseek-v4-pro max 思考深度 | ALREADY_HAVE | src/utils/effort.ts:25-51,67-81 | openclaude's modelSupportsEffort/modelSupportsMaxEffort defaults to true for firstParty (which includes z.ai DeepSeek). Explicit check not needed
901628b4 | fix: OpenAI provider MCP 工具不可见 | NOT_APPLICABLE | N/A | CCB-specific OpenAI provider fix (gpt-5.4/gpt-5.3-codex); openclaude uses Anthropic-compatible API
4591432a | Fix mintlify validate errors | NOT_APPLICABLE | N/A | Docs tooling fix
fc438bd2 | feat: auto mode settings + bug fix | GAP | Multiple files | (1) RSS memory indicator: NOT_APPLICABLE (feature). (2) Permission mode auto handling in Config.tsx: GAP (openclaude converts auto to default). (3) PowerShell null-safety: ALREADY_HAVE (openclaude already has !input?.command). (4) Keybinding prevValue/nextValue: NOT_APPLICABLE (CCB-specific)
c2ac9a74 | fix: dependency audit findings | NOT_APPLICABLE | N/A | CI/dependency lock changes
f5c3ee5b | fix: 长时间运行会话的内存泄漏 | GAP | Multiple files | (1) clearConversation leak fix (lastAPIRequest/lastAPIRequestMessages/lastClassifierRequests reset): GAP (openclaude only resets cost state). (2) MAX_FULLSCREEN_SCROLLBACK=500 cap: GAP (openclaude has no hard cap). (3) Progress entry dedup scan: GAP (openclaude only checks last message)
3cb4828d | chore: 1.10.4 | NOT_APPLICABLE | N/A | Version bump
52b61c2c | fix: bound agent communication memory growth | GAP | src/utils/forkedAgent.ts:520 | CCB adds filterIncompleteToolCalls as separate module with tests + boundary enforcement. openclaude has the function in runAgent.ts but misses test coverage + has comment saying NOT to filter in forkedAgent.ts (which differs from CCB). Low risk — functionality present
b47731a3 | test: Codecov coverage | NOT_APPLICABLE | N/A | Test config only
c80e5932 | feature: langfuse thinking + 文本 edit 修复 | NOT_APPLICABLE | N/A | CCB Langfuse tracing; openclaude has own Observe tracing
7cc1785f | chore: 1.10.5 | NOT_APPLICABLE | N/A | Version bump
42661498 | fix: keep UDS peer failures structured | GAP | src/utils/udsClient.ts:176-186 | CCB refactors connectToPeer: adds onSocketError callback, UdsPeerConnectionError, settled guard, cleanupListeners, timeout parameter. openclaude has older simpler impl
c81dac8c | fix: Node.js UDS socket chmod ENOENT | NOT_APPLICABLE | N/A | macOS+Node.js-specific; openclaude runs on Bun/Linux in Docker
7f864a47 | chore: 1.10.6 | NOT_APPLICABLE | N/A | Version bump
1a1d5705 | fix: skill-learning evidence 无限增长 | GAP | src/services/skillLearning/ | CCB adds caps: MAX_EVIDENCE_ENTRIES=10, observationIds cap=20, evidence lines cap=20 per append, MAX_SKILL_FILE_BYTES=50000. openclaude has no such caps
73130bde | chore: 1.10.7 | NOT_APPLICABLE | N/A | Version bump
0a9e6c03 | fix: 先关闭 skill learning | NOT_APPLICABLE | N/A | CCB build config (disables SKILL_LEARNING in defines.ts)
de9dbcdc | chore: 1.10.8 | NOT_APPLICABLE | N/A | Version bump
b8b48bf7 | fix: truncate 函数 undefined/null 崩溃 | GAP | src/utils/truncate.ts:140 | CCB adds null guard (str: string → str: string|undefined|null, if str==null return ''). openclaude has unguarded string param
4b97e663 | Fix README.md links formatting | NOT_APPLICABLE | N/A | Docs only

## Summary

Total commits: 82
GAPs found: 13
ALREADY_HAVE: 3
NOT_APPLICABLE: 65 (merges, CI, chore, version, docs, tests, CCB-specific, platform-specific)
MULTI (mixed verdict): 1

### Gap severity breakdown:

HIGH (potential crash/data loss):
- b8b48bf7: truncate null guard (crash on undefined/null input)
- ca1c87f4: usePipeIpc lazy require crash (low risk in Bun)
- 4dcbaf1e: messageSelector unprotected require crash (low risk but defensive)

MEDIUM (memory leak / growth):
- f5c3ee5b: session memory leak (3 fixes: clearConversation state reset, 500 msg scrollback cap, progress dedup)
- 1a1d5705: skill-learning evidence unbounded growth
- eb833da3: agent creation cache not flushed

LOW (correctness):
- ad09f38f: tab completion mid-line bug
- 42661498: UDS peer error handling
- 23bb09d2: model defaults not bumped to Opus 4.7
- da6d0636: read-before-edit restriction (intentionally kept per CLAUDE.md policy)
- da6d0636: DeepSeek thinking detection (different implementation path)
- fc438bd2: permission mode auto handling in Config
- 1c3b280c: multi-turn skill discovery cache

ALREADY_HAVE features already ported:
- SSH Remote (03811f97)
- BRIDGE_MODE/DAEMON decoupling (f2dd5142)
- DeepSeek max effort (cf33c060)
- PowerShell null-safety (fc438bd2 subset)
