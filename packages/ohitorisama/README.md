# eaglesakura/ohitorisama

個人開発（お一人様）向けの Slash Command / アセット集である。
GitHub Pull Request 作成コマンドなどをまとめる。

## Quick Start

```yaml
# 一括導入
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/ohitorisama
```

```yaml
# Command だけ導入（仮想ファイル）
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/ohitorisama/.apm/prompts/github.create-pull-request.prompt.md
```

## SKILLS

なし。

## Commands

※ `.apm/prompts/` が正本。

### github.create-pull-request

* ブランチでの作業完了後に Pull Request を作成する、または既存 PR の本文を更新する。
* 実体: [`.apm/prompts/github.create-pull-request.prompt.md`](.apm/prompts/github.create-pull-request.prompt.md)
* 差分の整理・[Pull Request テンプレート](.apm/assets/github.create-pull-request/template.md) による本文作成・`gh pr create` / `gh pr edit` の利用を手順として規定する。
* 対象リポジトリ・base ブランチ・既存 Pull Request URL はオプションで指定できる。

```text
/github.create-pull-request
```

```text
/github.create-pull-request
repo: app
base: feature/id/123/example
```

```text
/github.create-pull-request base は develop
```

```text
/github.create-pull-request https://github.com/OWNER/REPO/pull/123 の本文を更新
```

## Sub Agents

なし。

## 補助ファイル（テンプレート）

Slash Command または SKILL から `{assets}/...` で参照する。正本は `.apm/assets/`。解決は `workspace-resolve-agent-assets`（`armyknife`）に従う。

| ファイル | 参照元の例 |
| --- | --- |
| [assets/github.create-pull-request/template.md](.apm/assets/github.create-pull-request/template.md) | `/github.create-pull-request` |
