# website capability to skill 利用ガイド

[简体中文](./README.md) | [English](./README.en.md) |
[Español](./README.es.md) | [Français](./README.fr.md) |
[Deutsch](./README.de.md) | 日本語 | [한국어](./README.ko.md) |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

この skill は、Web サイトの URL を受け取り、ブラウザで機能を学習し、
その機能を API-first のローカル skill に変換します。

API の手動整理や認証復旧フローの設計は不要です。

## 作者

- 作者: `JasirVoriya`
- チーム: `Infrastructure Storage Team`
- メール: `jasirvoriya@gmail.com`
- GitHub: `https://github.com/JasirVoriya`

## コアルール（重要）

生成される skill を自動化可能にするため、次のルールを標準適用します。

- ブラウザ用途は機能学習と認証復旧の 2 つのみ。
- 業務処理は API 経由で実行し、Web ボタン操作に依存しない。
- 認証情報は `~/.<site>-auth.yaml` に保存。
- 各 API セッション前に認証ファイルを読み込む。
- 認証失効・失敗時はブラウザから再取得して書き戻す。
- 認証ファイル権限は `0600`。

## できること

- 対象サイトの可視機能を検出。
- UI 機能を API メソッド、リクエスト/レスポンス形にマッピング。
- 実行可能なサイト専用 skill スキャフォールドを生成。
- 認証ライフサイクル（読込、検証、復旧、再試行）を統合。
- 対応/非対応機能を含む検証レポートを出力。

## インストール（`npx skills add`）

`npx skills add openclaw/openclaw` と同様に、この skill も GitHub から
直接インストールできます。

### 1) リポジトリ内のインストール可能 skill を確認

```bash
npx -y skills add JasirVoriya/voriya-skills --list
```

### 2) Codex にインストール（グローバル）

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y
```

### 3) Cursor にインストール（グローバル）

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```

### 4) マルチ skill リポジトリ（任意）

```bash
npx -y skills add <owner>/<repo> --skill website-capability-to-skill -a codex -g -y
```

インストール後、AI クライアントを再起動してください。

## プロンプト例

### 1) 基本生成

```text
website-capability-to-skill で https://example.com を分析し、
サイト機能を API-first skill に変換して、
完全なディレクトリ構成を出力してください。
```

### 2) 範囲指定生成

```text
website-capability-to-skill で https://example.com を分析し、
「ログイン後管理画面 + 公開フロー」のみ対応し、
それ以外は unsupported-via-api として扱ってください。
```

### 3) 認証復旧を強制

```text
website-capability-to-skill で skill を生成し API を検証。
認証失敗時はブラウザから cookie/token を取得し、
~/.<site>-auth.yaml に保存して再試行してください。
```

### 4) 検証レポート出力

```text
website-capability-to-skill の生成後に、
対応機能、非対応機能、失敗原因、次の提案を含む
検証レポートを作成してください。
```

## クイックコマンド（スクリプト）

```bash
python3 scripts/bootstrap_site_skill.py --url <target-url> --output-root <skills-root>
python3 scripts/auth_cache.py path --url <target-url>
python3 scripts/auth_cache.py read --url <target-url>
python3 scripts/auth_cache.py is-valid --url <target-url>
```

## 生成物

最低限、次を含みます。

- サイト専用 `SKILL.md`
- `agents/openai.yaml`
- `scripts/auth_cache.py`
- `references/capability-map.md`
- 検証結果（対応/非対応/根拠）

## 前提条件

- 到達可能な対象サイト URL
- サイトにアクセスし操作できるブラウザセッション
- ローカルの Python 3 実行環境

ログインが必要なサイトでは、事前に有効なアカウントを用意してください。
