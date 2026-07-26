# armyknife

汎用開発向けのユーティリティ SKILL 集である。
Markdown 整備、ワークスペース運用などをまとめる。
SKILL・slash-command・Sub Agent の作成手順は [`agent-creator`](../agent-creator) を参照する。
ローカルマシンのキャッシュ調査は [`machine`](../machine) を参照する。
GitHub Actions 依存のセキュリティは [`github`](../github) を参照する。
GitHub Pull Request 作成コマンドは [`ohitorisama`](../ohitorisama) を参照する。

## Quick Start

```yaml
# 一括導入
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/armyknife
```

```yaml
# SKILL だけ導入（仮想サブディレクトリ）
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/armyknife/.apm/skills/markdown-search
    - eaglesakura/agent-skills/packages/armyknife/.apm/skills/markdown-format
```

## SKILLS

※ `.apm/skills/` 配下（アルファベット順）。

### agent-call-sub-agent

* Sub Agent（Task tool）呼び出し時に、委任内容に必要な SKILL を選定し、子 Agent の prompt へ「SKILLサジェスト」ブロックとして明示追加する。

### markdown-documentation

* Markdown での技術ドキュメント作成・更新のための SKILL。`*.md` の差分提案時はロードする。
* 「である」調・必須セクション（概要・よくあるパターンとアンチパターン）・原則ごとの補足・実装例・アンチパターンを規定する。
* コード引用や見出しレベルなど、Markdown の具体的な記述ルールを SKILL 本文で詳述する。

### markdown-format

* Markdown（`*.md`）の Formatter と Lint を行う。
* `markdownlint-cli2` を用いて書式を統一し、可読性を確保する。
* 自動修正されない項目は Linter の警告に従い個別に対応する。

### markdown-search

* ワークスペース内ドキュメント（主に `**/docs/**/*.md` 等）の探索・把握手順を規定する。
* `README.md`・`.cursor/`・`.ai-agent/memory/` など優先パスと、grep による見出し一覧の切り方を示す。
* 構造把握後に本文を読む流れで、広いリポジトリでも迷わないようにする。

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

なし。

## Sub Agents

なし。
