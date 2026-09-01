# eaglesakura/ohitorisama

個人開発（お一人様）向けの Slash Command / SKILL / アセット集である。
GitHub Pull Request 作成・分割方針・巨大 PR の Stacked 再分割、ブランチ命名ルールなどをまとめる。

## Quick Start

```yaml
# 一括導入
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/ohitorisama
```

```yaml
# SKILL / Command だけ導入（仮想サブディレクトリ / 仮想ファイル）
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/ohitorisama/.apm/skills/workspace-git-branch-rule
    - eaglesakura/agent-skills/packages/ohitorisama/.apm/skills/git-commit-comment-rule
    - eaglesakura/agent-skills/packages/ohitorisama/.apm/skills/github-comment-rule
    - eaglesakura/agent-skills/packages/ohitorisama/.apm/skills/split-pull-request-rule
    - eaglesakura/agent-skills/packages/ohitorisama/.apm/skills/decompose-fat-pr-to-stacked-prs
    - eaglesakura/agent-skills/packages/ohitorisama/.apm/prompts/github.create-pull-request.prompt.md
```

## 依存APM Package

* `eaglesakura/agentic-workspace`

## SKILLS

※ `.apm/skills/` 配下（アルファベット順）。

### git-commit-comment-rule

* AI Agent が `git commit` 等でコミットメッセージを書くときの**文案規約**。
* 1 行目は `add:` / `chg:` / `fix:` / `mod:` / `del:` のいずれか + 日本語要約。
* 2 行目以降は「何を・なぜ」の箇条書き。`refs #` は hook が付けるため Agent は書かない。
* Agent 起草時は末尾に `Co-authored-by: Cursor Agent` を付ける。

### github-comment-rule

* AI Agent が **既存 Pull Request** 上にコメントを書くときの**文案規約**。
* インライン review comment、スレッド返信、一般 discussion、`gh pr comment` / `gh pr review` などが対象。
* 日本語・丁寧語・端的な文体。末尾に `---` と `*Cursor Agent*` の署名ブロックを付ける。
* git commit メッセージや Cursor チャット内返答には使わない（`git-commit-comment-rule` と役割分担）。

### decompose-fat-pr-to-stacked-prs

* 既存の巨大 PR を、依存ありは Stacked PR・なしは独立 PR として再分割・作成する**実行系**。
* 方針は `split-pull-request-rule` と `/split-to-prs`、本文は `/github.create-pull-request`、Stack 操作は `gh stack`。
* 既定は分割案の承認後に実行。`/loop` 併用や決定権移譲時は自律確定可。元の巨大 PR は close/edit しない。
* 各分割 PR の CI Success のための最小差分は、元 PR に無くても許容する。

### split-pull-request-rule

* 大きな変更をレビューしやすい粒度の Pull Request 群へ分ける**方針**を規定する（実行はしない）。
* 10 分レビュー・レイヤー順・interface / 実装+Test / UI 境界・前提整備の先行切り出しなどを示す。
* 分割後ブランチ名は `{元のブランチ名}-{通し番号}-{内容}`。Stacked PR では blocking / non-blocking を明示する。
* `/split-to-prs` 等の実行系と組み合わせて使う。単純な 1 本 PR 作成だけでは使わない。

### workspace-git-branch-rule

* `main`・`feature/id/...`・`release/...` などブランチ運用ルールを規定する。
* ブランチ名から Issue との対応や作業種別を推測する際の参照とする。
* `gh` でタスク内容を引くことと整合する命名規約を SKILL 本文で示す。

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

Slash Command または SKILL から `{assets}/...` で参照する。正本は `.apm/assets/`。解決は `workspace-resolve-agent-assets`（`agentic-workspace`）に従う。

| ファイル | 参照元の例 |
| --- | --- |
| [assets/github.create-pull-request/template.md](.apm/assets/github.create-pull-request/template.md) | `/github.create-pull-request` |
