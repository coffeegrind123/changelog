# CCB Gap Analysis — Batch 5 (commits 329-410 from CCB main)

## 71144047 | Add brave as alternative WebSearchTool | NOT_APPLICABLE | — | CCB-specific adapter architecture (braveAdapter). Our WebSearchTool uses DuckDuckGo via zendriver browser MCP — completely different implementation
## 1071270c | chore: 更新版本到 1.3.2 | NOT_APPLICABLE | — | Version bump
## bd6448ec | fix: 修正顺序 | NOT_APPLICABLE | — | Swaps Brave/Bing adapter priority in CCB's adapter factory. We don't have those adapters
## 9a3081df | Merge branch 'pr/Eric-Guo/245' | NOT_APPLICABLE | — | Merge commit
## 3cf94fbd | fix: 修复对穷鬼模式的 auto dream 和 session memory 越过 | ALREADY_HAVE | query/stopHooks.ts:138 | Our code already guards with `!isLowContextMode()` which covers same purpose
## 9b8503d1 | fix: 修复 node 环境没有 bun 的问题 | NOT_APPLICABLE | — | Node.js Bun API polyfill — we're Bun-only
## c63b875a | chore: 1.3.3 版本 | NOT_APPLICABLE | — | Version bump
## bbb8b613 | docs: update contributors | NOT_APPLICABLE | — | Docs
## 2fb1c9dc | feat: 工具层及 mcp 大重构 (#252) | NOT_APPLICABLE | — | CCB monorepo workspace split (agent-tools/builtin-tools/mcp-client packages)
## e0484e28 | fix: 使用简化版本的 chrome 桥接器 | NOT_APPLICABLE | — | CCB's mcp-chrome-bridge dependency change
## d4b30d32 | fix: 修复 chrome 链接版本 | NOT_APPLICABLE | — | CCB's mcp-chrome-bridge version bump
## 05cabbbd | feat: langfuse 工具调用显示为嵌套结构 | NOT_APPLICABLE | — | CCB's Langfuse observability integration
## a7e03a5b | fix: 修复 interrupt 日志不上传 | NOT_APPLICABLE | — | CCB's Langfuse query.ts changes
## fce40fed | feat: 加上 userId 的传递 | NOT_APPLICABLE | — | CCB's Langfuse user identity passing
## be80da4c | fix: 修复缓存 | NOT_APPLICABLE | — | CCB's Langfuse cache token recording
## ecbd5a93 | fix: 修复 Bun.hash 不存在的问题 | NOT_APPLICABLE | — | Node.js polyfill for Bun.hash — we're Bun-only
## b5b81dfe | chore: 更改 chrome 的依赖 | NOT_APPLICABLE | — | CCB's chrome bridge dependency version
## dad3ad2b | docs: 添加浏览器说明支持 | NOT_APPLICABLE | — | Docs
## 8442aaad | fix: 修复 n 快捷键导致关闭的问题 | GAP | keybindings/defaultBindings.ts:137-138 | Removes 'y'/'n' from Confirmation context keybindings (prevents accidental 'n' close). We still have them
## b80483c2 | fix: 修复 node 下 ws 没打包问题 | NOT_APPLICABLE | — | Node.js build issue (ws moved to deps)
## 2273a0bc | docs: 修复链接 | NOT_APPLICABLE | — | Docs
## 1a4e9702 | fix: 修复类型问题(#267) (#271) | NOT_APPLICABLE | — | Type fixes + Node.js compat build changes
## 5a4c820e | test: 修复类型校验 (#279) | NOT_APPLICABLE | — | Test changes
## fe08cacf | fix(remote-control): harden self-hosted session flows (#278) | NOT_APPLICABLE | — | CCB's remote-control-server package changes
## 8169b962 | docs: update contributors | NOT_APPLICABLE | — | Docs
## 3470783c | build: 新增 vite 构建流程 | NOT_APPLICABLE | — | CCB build system (vite)
## 90027279 | feat: 添加环境变量支持以覆盖 max_tokens 设置 | NOT_APPLICABLE | — | CCB's src/services/api/openai/ adapter — we have separate openaiBridge architecture
## cfab161e | feat(langfuse): LLM generation 记录工具定义 | NOT_APPLICABLE | — | CCB's Langfuse integration
## 3cb1e50b | feat: 添加对 ACP 协议的支持 (#284) | ALREADY_HAVE | services/acp/ agent.ts bridge.ts entry.ts permissions.ts utils.ts | We already ported ACP from CCB. QueryEngine changes (resetAbortController/getAbortSignal) already present at QueryEngine.ts:1185,1191
## a02dc0bd | chore: 1.4.0 | NOT_APPLICABLE | — | Version bump
## c8d08d23 | Feat/integrate lint preview (#285) | NOT_APPLICABLE | — | Docs + tsconfig + CCB package changes. No core source logic changes
## bddd146f | feat: 重构供应商层次 (#286) | NOT_APPLICABLE | — | CCB's @ant/model-provider package refactor
## 03b7f9b4 | chore: 1.4.1 | NOT_APPLICABLE | — | Version bump
## c5ab83a3 | fix: 修复 linux 端的安装问题 | NOT_APPLICABLE | — | Install/build
## a14b7f35 | test: 修正 mock 的滥用情况 | NOT_APPLICABLE | — | Test changes
## c6599125 | docs: 更新说明 | NOT_APPLICABLE | — | Docs
## ac42ce2d | fix: 解决 node 下 loading 按钮计算错误问题 | NOT_APPLICABLE | — | Node.js-specific UI fix
## b5c299f5 | build: CI 添加通过过滤 | NOT_APPLICABLE | — | CI config
## 72a2093c | feat(remote-control): 优化 Web 展示、状态同步与桥接控制流程 (#288) | NOT_APPLICABLE | — | CCB's remote-control-server package
## d70e7f7f | feat: 支持 langfuse 工具调用映射 | NOT_APPLICABLE | — | CCB's Langfuse integration
## d2b66d9d | docs: update contributors | NOT_APPLICABLE | — | Docs
## 29cc74a1 | docs: 更新 CLAUDE.md | NOT_APPLICABLE | — | Docs
## 34154ee3 | feat: 支持 acp-link 包进行 acp 通用的 remote-control (#292) | NOT_APPLICABLE | — | CCB's acp-link package
## 2e9aaf49 | feat: ACP 协议版本 remote control (#293) | NOT_APPLICABLE | — | CCB's remote-control + ACP integration
## 4d939e57 | chore: 更新构建 feature 的问题 | NOT_APPLICABLE | — | Build/chore
## 7e4df5c3 | build: 更改构建逻辑 | NOT_APPLICABLE | — | Build
## a0dc4540 | fix: 修复服务器两个 / 的问题 | NOT_APPLICABLE | — | CCB's remote-control server fix
## 65367574 | feat: 对其他 provider 提供 langfuse 监控 | NOT_APPLICABLE | — | CCB's Langfuse for other providers
## a57ca085 | fix: 修复 node 的 es 版本太高不兼容的构建问题 | NOT_APPLICABLE | — | Node.js build compat
## c5edee43 | docs: 文档检查/check 20260419 (#296) | NOT_APPLICABLE | — | Docs
## 481e2a58 | feat: 恢复 --channels 能力 (#297) | NOT_APPLICABLE | — | CCB-specific Channels feature (MCP channel notifications)
## f9d01116 | fix: 替换 web 端 crypto.randomUUID 为 uuid 库以支持 HTTP 环境 | NOT_APPLICABLE | — | CCB's remote-control-server web frontend changes
## d1ab38c0 | chore: 移除 pre-commit git hook | NOT_APPLICABLE | — | Chore
## 673ccd18 | chore: 1.5.0 | NOT_APPLICABLE | — | Version bump
## c7bc8c86 | feat: remote control 支持 auto bind 功能 (#300) | NOT_APPLICABLE | — | CCB's remote-control feature
## 66d2671c | feat: acp manager (#304) | NOT_APPLICABLE | — | CCB's acp-link packages
## b83c3008 | docs: 更新 discord 地址 | NOT_APPLICABLE | — | Docs
## 494eab72 | feat: 接入内建 weixin channel(同 #301 重构版本) (#303) | NOT_APPLICABLE | — | CCB's WeChat channel integration
## 8c629858 | chore: 1.6.0 | NOT_APPLICABLE | — | Version bump
## a67e2d0e | docs: 更新 npm 安装 | NOT_APPLICABLE | — | Docs
## 92f8a92f | feat: 正式启用 auto mode (#307) | NOT_APPLICABLE | — | CCB-specific auto mode feature — large feature set touching many files. Debug logging changes are all Langfuse-specific
## e4ce08fe | Fixture/langfuse record auto mode data error (#308) | NOT_APPLICABLE | — | CCB's Langfuse auto mode fix
## ed4bdb93 | feat: 增强 auto mode 的易用性 (#312) | NOT_APPLICABLE | — | CCB's auto mode enhancements (permission hints, token estimation, awaySummary, etc.)
## 84f02718 | chore: 1.7.1 | NOT_APPLICABLE | — | Version bump
## 13a0bfc4 | fix: 修复构建产物 import 失效问题 | NOT_APPLICABLE | — | Vite build config change
## 96ec96c7 | feat: 添加 ccb update 命令，支持 npm/bun 自动更新 | NOT_APPLICABLE | — | CCB-specific update command
## 300faa18 | Merge branch 'feature/unknown-llm-feature-test' | NOT_APPLICABLE | — | Merge commit
## 5fc7c8e1 | chore: 添加 highlight.js 包 | NOT_APPLICABLE | — | Dependency addition
## cee62bc6 | fix: 修复 model alias 导致无限递归栈溢出 | NOT_APPLICABLE | utils/model/model.ts:149-182 | Our getDefault*Model() functions don't fall back to getUserSpecifiedModelSetting(), so no recursion risk. Different architecture
## 956e98a4 | fix: 修复重复依赖声明 | NOT_APPLICABLE | — | Package.json fix
## 711927f0 | chore: 更新 lock 文件 | NOT_APPLICABLE | — | Lock file
## 04c7ed42 | chore: 删除废弃文档和残留文件 | NOT_APPLICABLE | — | Cleanup
## 1837df5f | feat: 添加 skill learning 技能学习闭环系统 | ALREADY_HAVE | commands/skill-learning/ services/skillLearning/ | Already ported from CCB in April 2026
## 31b2fdd9 | feat: 添加 provider usage 统计与余额查询 | NOT_APPLICABLE | — | CCB's providerUsage service (Anthropic/Bedrock/OpenAI adapters, DeepSeek balance) — we use claudeAiLimits.ts
## c4775fff | feat: 添加 autonomy 自主模式命令系统 | ALREADY_HAVE | commands/autonomy.ts cli/handlers/autonomy.ts utils/autonomyAuthority.ts | Already ported from CCB in §9 slash command ports
## 59f8675f | feat: 添加 Windows Terminal swarm 后端及 swarm 增强 | NOT_APPLICABLE | — | Windows-specific (TmuxBackend, PaneBackendExecutor for Windows Terminal)
## be97a0b0 | feat: 添加 Bedrock API 客户端及 API 层增强 | NOT_APPLICABLE | — | Bedrock-specific provider (we don't support AWS Bedrock)
## 6c5df395 | feat: 添加 compact 缓存与上下文压缩增强 | ALREADY_HAVE | services/compact/cachedMicrocompact.ts | Already ported — full implementation with proper function exports
## 94c4b37e | feat: 添加 summary 命令 TypeScript 重写与其他命令增强 | NOT_APPLICABLE | — | CCB's command visibility reorg + summary command rewrite. Our commands already properly registered
## fb41513b | feat: 添加工具类增强与状态管理改进 | GAP | utils/advisor.ts:93 | CCB adds `opus-4-7` to modelSupportsAdvisor() and isValidAdvisorModel(). We only have opus-4-6
## eec96135 | feat: 添加 napi 包测试覆盖与 stub 改进 | NOT_APPLICABLE | — | napi package tests
## 2247026b | chore: 添加脚本与构建配置更新 | GAP | constants/prompts.ts:139,143 constants/figures.ts:13 | Updates FRONTIER_MODEL_NAME to Claude Opus 4.7, opus model ID to claude-opus-4-7, adds EFFORT_XHIGH. We still reference Opus 4.6. Our EFFORT_XHIGH already exists but with ◈ char (CCB uses ⦿)

## Summary

Total commits analyzed: 82
- NOT_APPLICABLE: 75 (docs/build/test/version/merge/CCB-specific packages or features)
- ALREADY_HAVE: 5 (low-context guard, cachedMicrocompact, ACP, skill learning, autonomy)
- GAP: 3

### GAPs found:
1. **8442aaad** — Confirmation keybinding 'n' removal (prevents accidental close). We still have 'y'/'n' in Confirmation context at keybindings/defaultBindings.ts:137-138
2. **fb41513b** — Missing `opus-4-7` in advisor model checks at utils/advisor.ts:93
3. **2247026b** — Still referencing Opus 4.6 instead of Opus 4.7 in constants/prompts.ts and model configs
