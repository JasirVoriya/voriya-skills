# 仓库曝光增长执行模板

这个文档给你一套可以直接执行的仓库曝光方案，包含 GitHub topics
建议和一周发布节奏。目标是提升 GitHub 搜索命中、README 转化和
安装使用量。

## GitHub topics 清单

先设置 8 到 12 个高相关 topic，优先覆盖“能力词 + 场景词 + 工具词”。

建议 topic：

- `skills`
- `ai-agent`
- `agentic-workflow`
- `automation`
- `api`
- `developer-tools`
- `prompt-engineering`
- `chrome-devtools`
- `codex`
- `cursor`
- `website-automation`
- `python`

如果你使用 GitHub CLI，可以执行：

```bash
gh repo edit JasirVoriya/voriya-skills \
  --add-topic skills \
  --add-topic ai-agent \
  --add-topic agentic-workflow \
  --add-topic automation \
  --add-topic api \
  --add-topic developer-tools \
  --add-topic prompt-engineering \
  --add-topic chrome-devtools \
  --add-topic codex \
  --add-topic cursor \
  --add-topic website-automation \
  --add-topic python
```

## 一周发布节奏模板

按周循环发布，保持固定节奏。下面是一个可直接执行的 5 天模板。

1. 周一：收集上周反馈、Issue、失败样例，确定本周发布范围。
2. 周二：完成本周 skill 功能或文档改进，补齐触发词和示例。
3. 周三：做最小可行验证，确认安装命令、提示词、脚本可运行。
4. 周四：编写 Release 文案，整理“新增/修复/已知限制”。
5. 周五：发布 Release 并同步分发到社区渠道。

## Release 文案模板

每周 Release 建议使用统一结构，降低用户理解成本。

````markdown
## vX.Y.Z - YYYY-MM-DD

### Added
- 新增：`<skill-name>` 的 `<能力点>`。

### Improved
- 优化：`<skill-name>` 的 `<触发词/输出结构/文档示例>`。

### Fixed
- 修复：`<问题描述>`。

### Trigger phrases
- `用 <skill-name> 分析 <url> 并输出 API-first skill`。
- `只覆盖 <workflow-scope>，其他能力标记 unsupported-via-api`。

### Known limits
- `<暂未支持的能力或约束>`。

### Install
npx -y skills add JasirVoriya/voriya-skills --skill <skill-name> -a codex -g -y
````

## 分发清单

每次发布后，同步到以下渠道，保证同一条消息在 24 小时内完成分发。

- GitHub Releases
- GitHub Discussions
- X 或 Reddit 相关社区
- 中文渠道（掘金、知乎、少数派任一）
- 可提交的 Awesome List（如 AI Agent、Developer Tools 分类）

## 每周复盘指标

每周固定复盘这三个数字，并只优化一个环节。

- 仓库访问量（Views）
- README 到安装命令的转化（点击或复制行为）
- 安装后触发成功率（能否走通首个提示词）
