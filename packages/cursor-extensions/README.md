# cursor-extensions

Cursor 向け専用 SKILL 集である。
Claude Code CLI 提案を Cursor Agent CLI へ置き換えるなど、Cursor 固有の運用をまとめる。

## Quick Start

```yaml
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/cursor-extensions
```

## SKILLS

※ `.apm/skills/` 配下（アルファベット順）。

### claude-alias-cursor

* Claude Code CLI（`claude` / `claude -p` 等）の提案・記述・スクリプトを、未契約環境向けに Cursor Agent CLI（`agent` または `cursor agent`）へ置き換える。
* 他 SKILL・ドキュメント・eval・CI・skill-creator の `run_loop` / `run_eval` が `claude` を出したらロードし、実行前にバインディングへ変換する。
* IDE 起動だけの `cursor`（agent サブコマンドなし）、純粋な Cursor SDK 実装のみ、Claude 契約済みで本物の `claude` を使う明示指示がある場合は使わない。

## Commands

なし。

## Sub Agents

なし。
