# agent-creator

AI Agent 向けアセット作成 SKILL 集である。
SKILL・slash-command・Sub Agent の新規作成・改訂手順をまとめる。

## Quick Start

```yaml
# 一括導入
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/agent-creator
```

```yaml
# SKILL だけ導入（仮想サブディレクトリ）
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/agent-creator/.apm/skills/tool-command-creator
    - eaglesakura/agent-skills/packages/agent-creator/.apm/skills/tool-skill-creator-extension
    - eaglesakura/agent-skills/packages/agent-creator/.apm/skills/tool-sub-agent-creator
```

## SKILLS

※ `.apm/skills/` 配下（アルファベット順）。

### tool-command-creator

* Cursor の slash-command（`.cursor/commands/*.md` や `.apm/prompts/*.prompt.md`）を新規作成・改訂する。
* テンプレート準拠の Help 情報 / Example / 関連ファイル / アセット / 入出力 / 手順 / バリデーション / ガードレールを揃える。

### tool-skill-creator-extension

* SKILL 作成・改訂時のコマンド記述と共有アセット参照ルールを補足する。
* skill-creator で新規 SKILL を書く、既存 SKILL のコマンド例を直す、手順書に `dart` / `flutter` / `go` / `npm` 等を載せるときは使う。

### tool-sub-agent-creator

* Cursor のカスタム Sub Agent（`.cursor/agents/*.md`）を新規作成・改訂する。
* テンプレート準拠化・職能と実施タスクの切り分けに使う。

## Commands

なし。

## Sub Agents

なし。
