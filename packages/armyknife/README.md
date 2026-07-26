# armyknife

汎用開発向けのユーティリティ SKILL / Prompt 集である。
Markdown 整備、ワークスペース運用、ツール作成、キャッシュ調査、GitHub Pull Request 作成コマンドなどをまとめる。

## Quick Start

```yaml
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/armyknife
```

## SKILLS

※ `.apm/skills/` 配下（アルファベット順）。

### agent-call-sub-agent

* Sub Agent（Task tool）呼び出し時に、委任内容に必要な SKILL を選定し、子 Agent の prompt へ「SKILLサジェスト」ブロックとして明示追加する。

### github-actions-workflow-build

* GitHub Actions のワークフロー（`.github/**/*.yaml`）編集時に守るセキュリティ・運用ルールを規定する。
* 外部アクションは SHA ピン留めとし、`uses: org/action@tag` のような可変タグ指定を避ける。
* `gh api` 等でタグとコミット SHA を取得し、コメントで人間が追える形にする。

### maintenance-measure-cache-size

* ローカル PC の開発ツールキャッシュ占有を調査し、大きなディレクトリを一覧する。
* パス・GiB・用途・復元不足・削除コマンドなどの出力フォーマットを規定する。
* OS ごとの探索対象ディレクトリとしきい値（例: 10GiB 超で深掘り）を SKILL 本文で示す。

### markdown-documentation

* Markdown での技術ドキュメント作成・更新のための SKILL。`*.md` の差分提案時はロードする。
* 「である」調・必須セクション（概要・よくあるパターンとアンチパターン）・原則ごとの補足・実装例・アンチパターンを規定する。
* コード引用や見出しレベルなど、Markdown の具体的な記述ルールを SKILL 本文で詳述する。

### markdown-fix

* Markdown（`*.md`）の Formatter と Lint を行う。
* `markdownlint-cli2` を用いて書式を統一し、可読性を確保する。
* 自動修正されない項目は Linter の警告に従い個別に対応する。

### markdown-search

* ワークスペース内ドキュメント（主に `**/docs/**/*.md` 等）の探索・把握手順を規定する。
* `README.md`・`.cursor/`・`.ai-agent/memory/` など優先パスと、grep による見出し一覧の切り方を示す。
* 構造把握後に本文を読む流れで、広いリポジトリでも迷わないようにする。

### tool-command-creator

* Cursor の slash-command（`.cursor/commands/*.md` や `.apm/prompts/*.prompt.md`）を新規作成・改訂する。
* テンプレート準拠の Help 情報 / Example / 関連ファイル / アセット / 入出力 / 手順 / バリデーション / ガードレールを揃える。

### tool-skill-creator-extension

* SKILL 作成・改訂時のコマンド記述と共有アセット参照ルールを補足する。
* skill-creator で新規 SKILL を書く、既存 SKILL のコマンド例を直す、手順書に `dart` / `flutter` / `go` / `npm` 等を載せるときは使う。

### tool-sub-agent-creator

* Cursor のカスタム Sub Agent（`.cursor/agents/*.md`）を新規作成・改訂する。
* テンプレート準拠化・職能と実施タスクの切り分けに使う。

### workspace-agent-memory-save

* 調査結果や会話サマリを不揮発の Memory として保存する手順を規定する。
* 出力先は `.ai-agent/memory/{文脈内容}.md` とし、既存があれば更新する。
* テンプレートと見出しレベル単位の構造により、後続チャットでのロードしやすさを確保する。

### workspace-agent-temporary

* AI Agent が使ってよい一時領域（`.ai-agent/`）のルート・サブディレクトリ・Ignore を規定する。
* 一時スクリプトや調査メモは `.ai-agent/tmp/`、実行計画は `.ai-agent/plan/` に置く。
* `assets/` の構成を参考にディレクトリを用意し、コミット対象外とする。

### workspace-count-tokens

* Cursor ワークスペースのデフォルト Context と、動的ロード時の SKILL.md / docs・references の最大トークンを概算する。

### workspace-git-branch-rule

* `main`・`feature/id/...`・`release/...` などブランチ運用ルールを規定する。
* ブランチ名から Issue との対応や作業種別を推測する際の参照とする。
* `gh` でタスク内容を引くことと整合する命名規約を SKILL 本文で示す。

### workspace-resolve-agent-assets

* ドキュメント内の `{assets}/...` メタ変数だけを実ファイルパスへ解決する。
* 本文のアセットディレクトリ記述と互換の `metadata.assets` から候補を集め、文書相対とリポジトリルート相対の両方で解決する。

### workspace-resolve-file-path

* ドキュメントの通常パス表記を実ファイルへ解決する。
* クォート path、Markdown リンク、`.ai-agent/` 候補順などを扱う。

### workspace-resolve-url-metadata

* Issue URL 等からタスク ID・タイトルなど取得可能なメタデータを整理する。
* `gh issue view ... --json number,title` など CLI での取得例と JSON の読み方を示す。
* GitHub Issues の URL パターンごとのフィールド対応を SKILL 本文で規定する。

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

Slash Command または SKILL から `{assets}/...` で参照する。正本は `.apm/assets/`。解決は `workspace-resolve-agent-assets` に従う。

| ファイル | 参照元の例 |
| --- | --- |
| [assets/github.create-pull-request/template.md](.apm/assets/github.create-pull-request/template.md) | `/github.create-pull-request` |
