# 网站能力转 Skill 使用指南

简体中文 | [English](./README.en.md) | [Español](./README.es.md) |
[Français](./README.fr.md) | [Deutsch](./README.de.md) |
[日本語](./README.ja.md) | [한국어](./README.ko.md) |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

这个 skill 的目标是：给你一个网站 URL，AI 先用浏览器学习网站能力，再把
这些能力转换成可通过 API 调用的本地 skill。

你不需要手动梳理接口，也不需要自己设计鉴权恢复流程。

## 作者

- 作者：`JasirVoriya`
- 团队：`基础架构存储小组`
- 邮箱：`jasirvoriya@gmail.com`
- GitHub：`https://github.com/JasirVoriya`

## 核心规则（重要）

为了确保生成后的 skill 可自动化复用，这个 skill 默认执行以下规则：

- 浏览器只用于两件事：学习网站能力、恢复鉴权数据。
- 业务执行必须走 API，不依赖网页按钮操作。
- 鉴权文件保存到用户主目录，格式为 `~/.<site>-auth.yaml`。
- 每次 API 会话前先读鉴权文件。
- 鉴权过期或失败时，自动从浏览器提取并回写鉴权文件。
- 鉴权文件权限固定为 `0600`。

## 你能让它做什么

从用户角度，这个 skill 可以完成这些事：

- 网站能力学习：识别网站可见功能和对应操作路径。
- 能力映射：把页面能力映射成接口方法、请求结构和响应结构。
- Skill 脚手架生成：生成可运行的站点专用 skill 目录。
- 鉴权生命周期接入：自动接入鉴权读取、校验、失效恢复、重试。
- 结果产出：给出已支持能力、未支持能力和验证报告。

## 安装方式（npx skills add）

如果你希望像 `npx skills add openclaw/openclaw` 一样安装这个 skill，可以直接
从 GitHub 仓库安装。

### 1) 查看仓库里可安装的 skill

```bash
npx -y skills add JasirVoriya/voriya-skills --list
```

### 2) 安装到 Codex（全局）

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y
```

### 3) 安装到 Cursor（全局）

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```

### 4) 多 skill 仓库场景（可选）

如果后续把多个 skill 放在同一个仓库中，可按名称安装指定 skill：

```bash
npx -y skills add <owner>/<repo> --skill website-capability-to-skill -a codex -g -y
```

安装完成后，重启对应 AI 客户端以加载新 skill。

## 怎么写提示词触发能力

下面这些提示词可以直接复制给 AI。

### 1) 基础生成

```text
用 website-capability-to-skill skill 分析 https://example.com，
把网站能力转换成 API-first skill，并输出完整目录。
```

### 2) 指定范围生成

```text
用 website-capability-to-skill skill 分析 https://example.com，
只覆盖“登录后管理台 + 发布流程”相关能力，其他能力标记 unsupported-via-api。
```

### 3) 强制鉴权恢复

```text
用 website-capability-to-skill skill 生成 skill 并验证接口。
如果鉴权失败，去浏览器抓取 cookie/token，写入 ~/.<site>-auth.yaml 后重试。
```

### 4) 产出验证报告

```text
用 website-capability-to-skill skill 完成生成后，
给我一个验证报告：已验证能力、未支持能力、失败原因和下一步建议。
```

## 快速命令（脚本）

你也可以直接使用内置脚本：

```bash
python3 scripts/bootstrap_site_skill.py --url <target-url> --output-root <skills-root>
python3 scripts/auth_cache.py path --url <target-url>
python3 scripts/auth_cache.py read --url <target-url>
python3 scripts/auth_cache.py is-valid --url <target-url>
```

## 产物清单

执行完成后，至少包含以下产物：

- 站点专用 `SKILL.md`
- `agents/openai.yaml`
- `scripts/auth_cache.py`
- `references/capability-map.md`
- 一份能力验证结论（支持/不支持/证据）

## 前置条件

你需要准备：

- 可访问的目标网站 URL
- 能打开目标网站并完成必要操作的浏览器会话
- 本地可执行 Python 3 环境

如果目标站点需要登录，建议先准备一个可用账号，便于鉴权恢复阶段提取数据。
