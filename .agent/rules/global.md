---
trigger: always_on
---

# Antigravity Agent Execution Rules

## 1. 规划优先 (Planning First)
- 在执行任何跨文件修改或复杂逻辑变更前，必须先进入 "Planning Mode"。
- 优先检索项目根目录下的 `TODO.md` 或 `PLAN.md`。如果存在，请严格遵守其中的架构设计。
- 在未输出“执行计划（Execution Plan）”并获得确认前，禁止修改源码。

## 2. 资源优化 (Resource Optimization)
- 默认优先使用 Gemini 3 Flash 进行简单的文件读取和代码补全。
- 仅在涉及深层逻辑推理、算法重构或复杂 Bug 调试时，请求切换至 Claude 3.5/4.6 Sonnet。
- 尽量通过单次批量修改完成任务，避免碎片化的往复对话。

## 3. 自动化与测试 (Automation & Testing)
- 修改完成后，自动搜索项目中的测试脚本。
- 在内置终端运行相关测试，并根据报错信息自行迭代，直至测试通过。
- 若涉及 UI 改动，请提示查看内置的 Web Preview。

## 4. 环境感知 (Context Awareness)
- 始终关注项目的 Dockerfile 和 docker-compose.yml 约束，确保新代码在容器环境下兼容。
- 保持代码风格与现有项目一致，避免引入冗余的依赖库。