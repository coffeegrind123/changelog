# CCB Gap Analysis — Batch 4 (commits 247-328 of main)
## /tmp/claude-code-ccb vs /home/openclaudeuser/openclaude/src/
## 2026-05-11

Verdict key: GAP | ALREADY_HAVE | NOT_APPLICABLE

2c660daf | docs: 加点 emoji 好看点 | NOT_APPLICABLE | — | docs-only
1b47333d | feat: enable GrowthBook local gate defaults for P0/P1 features | ALREADY_HAVE | — | openclaude enables all features via node_modules/bundle polyfill + GrowthBook disabled; different approach, same effect
379e40f1 | fix: 回退全屏模式 | ALREADY_HAVE | src/utils/fullscreen.ts:143 | openclaude already defaults return false (line 143 "return false"); CCB changed from return true to ant-only
35bc4f39 | Merge pull request #153 | NOT_APPLICABLE | — | merge commit
33949ce5 | Merge pull request #156 | NOT_APPLICABLE | — | merge commit
3ea64eeb | docs: update contributors | NOT_APPLICABLE | — | docs-only
c445f43f | feat: 第一个可以用的 ink 组件抽象 (#158) | NOT_APPLICABLE | — | CCB-specific ink component library (packages/@ant/ink/) — not in openclaude
dfa7aa1d | docs: update contributors | NOT_APPLICABLE | — | docs-only
70baa6f7 | feat: add Grok (xAI) API adapter (#152) | NOT_APPLICABLE | — | CCB-specific provider adapter; openclaude uses openaiBridge for provider routing, no Grok
ca0c3265 | docs: update contributors | NOT_APPLICABLE | — | docs-only
88d4c3ba | Revert ink component (#175) | NOT_APPLICABLE | — | reverted CCB ink library
4b440479 | fix: prevent iTerm2 terminal response sequences from leaking into REPL input (#172) | GAP | src/utils/earlyInput.ts:104-117 | CCB rewrite handles CSI/DCS/OSC/SOS/PM per ECMA-48; OC only checks single-byte terminators (0x40-0x7E) — DCS (XTVERSION) and CSI parameters leak into input buffer
0c53796d | feat: restore daemon supervisor and remoteControlServer command (#170) | ALREADY_HAVE | — | openclaude has daemon mode + remoteControlServer command
dab07839 | docs: update contributors | NOT_APPLICABLE | — | docs-only
a7d9a220 | fix: 修复 main 文件及 "production" 的问题 | NOT_APPLICABLE | — | CCB auto-updater/DevBar fixes; openclaude uses different auto-updater (GitHub Releases API)
4e1e681a | fix: 删除 debug 限制 | ALREADY_HAVE | src/main.tsx:282-287 | OC has the same guard but Bun doesn't trigger node --inspect; USER_TYPE=ant check is harmless
e5782e73 | Revert "Revert ink" (#175) | NOT_APPLICABLE | — | CCB ink library re-revert
f268b16b | feat: 将 keybinding 纳入 ink 管辖 | NOT_APPLICABLE | — | CCB ink-specific keybinding integration
52a9cc04 | fix: 修复 ant 模式 | NOT_APPLICABLE | — | CCB-specific ExperimentEnrollmentNotice/GateOverridesWarning notices
5d7e5475 | fix: reorder tool and user messages for OpenAI API compatibility (#168) (#177) | NOT_APPLICABLE | — | CCB-specific openai/convertMessages.ts; OC uses different openaiBridge implementation (requestTranslator.ts/streamTranslator.ts)
0d8f494c | fix(computer-use): 修复权限检查和应用列表获取的问题 (#157) | NOT_APPLICABLE | — | macOS-specific JXA + mdls fixes; OC uses domdomegg computer-use-mcp package
042e186b | docs: update contributors | NOT_APPLICABLE | — | docs-only
91b9366f | refactor: 大规模迁移原有组件到 ink 包内 | NOT_APPLICABLE | — | CCB ink migration; OC has separate ink integration
d6bfc34b | fix: 修复 ant 模式 | NOT_APPLICABLE | — | same as 52a9cc04 — CCB notices
cf26c73e | docs: update contributors | NOT_APPLICABLE | — | docs-only
3e1c6bcc | Merge branch 'main' into refactor/ink-v2 | NOT_APPLICABLE | — | merge commit
e86573ac | fix: 修复 -r 模式下键盘输入无响应 | GAP | src/ink/components/App.tsx:231,274 | Two fixes missing: (1) no safety net to remove pre-existing readable listeners from stdin after stopCapturingEarlyInput() (line 231); (2) no React 19 layout-effect cleanup guard — when rawModeEnabledCount decrements to 0 (line 274) doesn't check active EventEmitter listeners before disabling raw mode. Impact limited: fullscreen defaults OFF in OC.
4e4111be | Merge branch 'refactor/ink-v2' | NOT_APPLICABLE | — | merge commit
3683f225 | 补全status界面里的信息 (#189) | NOT_APPLICABLE | — | CCB provider-specific status additions (Grok/OpenAI providers); OC uses different provider model
bdea5a26 | fix: Fix deferred tools handling in OpenAI compatibility layer (#193) | NOT_APPLICABLE | — | CCB-specific openai/ layer; OC uses different openaiBridge
79b472f9 | docs: update contributors | NOT_APPLICABLE | — | docs-only
d52300ff | 完善沙箱文档 (#195) | NOT_APPLICABLE | — | docs-only
91ee1428 | Fix bug OpenAI tooluse, improve error messaging (#199) | NOT_APPLICABLE | — | CCB-specific openai/ layer; OC uses different openaiBridge
ae6ae6cf | docs: update contributors | NOT_APPLICABLE | — | docs-only
73a18c30 | docs: 完善上下文工程核心定义与架构说明 (#204) | NOT_APPLICABLE | — | docs-only
a3505aee | feat: Add DeepSeek thinking mode support for OpenAI compatibility layer (#206) | NOT_APPLICABLE | — | CCB-specific openai/ layer; OC openaiBridge already handles DeepSeek properly via model detection + thinking params
7f694168 | docs: update contributors | NOT_APPLICABLE | — | docs-only
f17b7c71 | 修复使用/help 后再按左右键报错 (#212) | ALREADY_HAVE | src/components/HelpV2/Commands.tsx:6-8 | OC already has truncate/useTabHeaderFocus/Select imports; same fix present
2da65140 | feat: 支持自托管的 remote-control-server (#214) | NOT_APPLICABLE | — | CCB Docker/deployment CI for self-hosted RCS
8b2532a9 | docs: fix documentation deviations (#220) | NOT_APPLICABLE | — | docs-only
562e9daa | fix: Handle undefined command names in getCommandName function (#217) | GAP | src/types/command.ts:216 | OC returns `cmd.userFacingName?.() ?? cmd.name` directly; if both undefined (stub exporting {}), returns undefined instead of string. CCB fix: `return name || ''`
2b0d31aa | feat: 对齐构建时的目标 | NOT_APPLICABLE | — | CCB build system alignment
8c619a21 | build: 修复构建报错 | NOT_APPLICABLE | — | CCB build fix
87230cf3 | docs: update contributors | NOT_APPLICABLE | — | docs-only
bb078362 | fix: support CRLF SSE frame parsing (#223) | GAP | src/cli/transports/SSETransport.ts:67 | OC uses `buffer.indexOf('\n\n', pos)` + `pos = idx + 2` — doesn't handle CRLF (`\r\n\r\n`). CCB fix: regex `/\r?\n\r?\n/g` for frame delimiter + normalize trailing \r on split lines. Also affects streamTranslator.ts:468 which has same `\n\n` delimiter.
e6affc70 | 修复 fork command stub + fork.tsx (#221) | ALREADY_HAVE | src/commands/fork/ | OC has fork-impl.ts + index.ts with full AgentTool fork subagent integration
01cf45f4 | fix: 修复 permission 面板 | ALREADY_HAVE | src/components/permissions/rules/ | Both RecentDenialsTab.tsx and WorkspaceTab.tsx already import useTabHeaderFocus
dfce6d02 | docs: 更新私有部署文档 | NOT_APPLICABLE | — | docs-only
ab3d8ef8 | docs: update contributors | NOT_APPLICABLE | — | docs-only
a14d3dc8 | fix(types): clean type fixes across 92 files | NOT_APPLICABLE | — | massive TypeScript cleanup across 92 files; hard to apply, low priority
34bbc1d4 | fix(types): replace all as any with proper type assertions | NOT_APPLICABLE | — | type-system hardening; low priority for feature parity
637531f8 | fix(types): simplify bridge transport message type | NOT_APPLICABLE | — | type-level cleanup; low priority
609e9114 | docs: 尝试 docs 文档更新 | NOT_APPLICABLE | — | docs-only
e70319e8 | docs: 更新远程控制及 rg 下载 | NOT_APPLICABLE | — | docs-only
c82f5994 | fix(openai): fix stop_reason null, zero usage fields and max_tokens forwarding | NOT_APPLICABLE | — | CCB-specific openai/streamAdapter.ts; OC's streamTranslator.ts handles stop_reason + max_tokens correctly via different implementation
ff03fe7f | fix: 修复类型问题 | NOT_APPLICABLE | — | type fixes; low priority
81073135 | docs: 审校 Agent 文档术语与架构描述准确性 (#231) | NOT_APPLICABLE | — | docs-only
0b1e678f | fix: 修复 mintlify ignore, 修复侧边栏 | NOT_APPLICABLE | — | docs/build config
b681139b | docs: update contributors | NOT_APPLICABLE | — | docs-only
8137b66a | fix: 修复初次登陆的校验问题 | NOT_APPLICABLE | — | CCB onboarding flow; OC uses CLAUDE_AUTO_TRUST + bypassPermissions
9da7345f | Add Ultraplan Feature for Advanced Multi-Agent Planning (#232) | ALREADY_HAVE | src/commands/ultraplan.tsx | OC has ultraplan (refactored from CCR remote to local forked agent). CCB adds multi-mode support (simple/three_subagents/visual) which OC doesn't have — feature enhancement, not bug fix.
b060eabd | chore: 添加类型测试 | NOT_APPLICABLE | — | test-only
7088fe3c | Merge remote-tracking branch guunergooner/fix/openai-stop-reason-usage | NOT_APPLICABLE | — | merge commit
6a700569 | feat: 全部类型问题解决 | NOT_APPLICABLE | — | type fixes; low priority
eeb0f277 | docs: update contributors | NOT_APPLICABLE | — | docs-only
c676ac46 | docs: update contributors | NOT_APPLICABLE | — | docs-only
5beeebad | docs: 更新类型检查的 CLAUDE.md | NOT_APPLICABLE | — | docs-only
ffd1c366 | feat: 添加模型 1M 上下文切换 | NOT_APPLICABLE | — | CCB UI enhancement (ModelPicker 1M toggle); OC already has has1mContext() in context.ts but no picker UI
d27c6cbc | chore: remove prefetchOfficialMcpUrls call on startup | GAP | src/main.tsx:435 | OC still calls `void prefetchOfficialMcpUrls()` in startDeferredPrefetches — unnecessary Anthropic registry fetch on every startup. CCB removed it.
6a9da9d5 | docs: 添加 git commit 规范 | NOT_APPLICABLE | — | docs-only
2fea429d | feat: 添加对 langfuse 监控的支持 (#242) | NOT_APPLICABLE | — | CCB-specific Langfuse tracing; OC uses Observe
09fc515e | feat: 远程群控 (#243) | ALREADY_HAVE | src/utils/pipeTransport.ts src/utils/lanBeacon.ts src/utils/pipeRegistry.ts | OC has full LAN Pipes + UDS messaging already
c8a502f8 | chore: 删除重复 feature 定义 | NOT_APPLICABLE | — | CCB build system duplicate feature cleanup; OC uses different build system
423f114d | docs: 更新 langfuse 文档 | NOT_APPLICABLE | — | docs-only
e9861415 | fix: 修复穷鬼模式的写入问题 | NOT_APPLICABLE | — | CCB-specific "poor mode" feature (persist to settings.json); OC uses lowContextMode instead
e0e4ee41 | docs: add complete features guide (#246) | NOT_APPLICABLE | — | docs-only
14c46df8 | docs: 清理垃圾文档 | NOT_APPLICABLE | — | docs-only
227083d3 | fix: 修复截图 MIME 类型硬编码导致 API 拒绝的问题 | NOT_APPLICABLE | — | CCB computer-use MCP package fix; OC uses domdomegg computer-use-mcp which handles MIME types. OC fallback `'image/jpeg'` at wrapper.tsx:272 is safety net.
e770f1ef | feat: 完成第一个 mcp-chrome 接入版本 | ALREADY_HAVE | src/utils/claudeInChrome/ | OC has full claudeInChrome MCP (setup.ts, mcpServer.ts, toolRendering.tsx, etc.)
513ccc30 | fix: 修复需要鉴权的问题 | NOT_APPLICABLE | — | CCB chrome MCP auth header fix (127.0.0.1:12306); not in OC
8399d9ed | fix: 修复类型问题 | NOT_APPLICABLE | — | type fixes; low priority

## Summary

82 commits analyzed. 5 GAPs found:

1. **4b440479** (iTerm2 terminal response leak) — `src/utils/earlyInput.ts:104-117` — ESC sequence handling only checks 0x40-0x7E terminators; DCS/OSC/CSI param byte sequences leak into input buffer
2. **bb078362** (CRLF SSE frame parsing) — `src/cli/transports/SSETransport.ts:67` — frame delimiter uses `\n\n` only, doesn't handle `\r\n\r\n`; also affects `streamTranslator.ts:468`
3. **562e9daa** (undefined command names) — `src/types/command.ts:216` — `getCommandName` returns null/undefined for stub commands; no `|| ''` fallback
4. **d27c6cbc** (prefetchOfficialMcpUrls) — `src/main.tsx:435` — still calls prefetchOfficialMcpUrls() at startup making unnecessary Anthropic registry network call
5. **e86573ac** (-r mode keyboard input) — `src/ink/components/App.tsx:231,274` — (a) no safety net to remove stale readable listeners after stopCapturingEarlyInput(); (b) no React 19 layout-effect guard when rawModeEnabledCount decrements to 0. Impact limited: fullscreen defaults OFF.
