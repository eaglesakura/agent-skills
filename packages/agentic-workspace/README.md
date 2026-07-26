# agentic-workspace

AI Agent との協業に最適化したワークスペースを構築・運用するための SKILL 集である。
Markdown 整備、ワークスペース運用などをまとめる。
SKILL・slash-command・Sub Agent の作成手順は [`agent-creator`](../agent-creator) を参照する。
ローカルマシンのキャッシュ調査は [`machine`](../machine) を参照する。
GitHub Actions 依存のセキュリティは [`github`](../github) を参照する。
GitHub Pull Request 作成コマンドは [`ohitorisama`](../ohitorisama) を参照する（ブランチ命名ルール含む）。

## Quick Start

```yaml
# 一括導入
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/agentic-workspace
```

```yaml
# SKILL だけ導入（仮想サブディレクトリ）
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/agentic-workspace/.apm/skills/markdown-search
    - eaglesakura/agent-skills/packages/agentic-workspace/.apm/skills/markdown-format
```

## 推奨するワークスペース構造

`workspace-layout` / `workspace-agent-temporary` / `workspace-agent-memory-save` / `markdown-search` 等に基づく。
`.ai-agent/` はコミット対象外（ひな形は `workspace-layout` の `assets/.ai-agent/`）。
HQ 構成では `headquarters/.ai-agent/` をルートの `.ai-agent/` より優先する（`workspace-resolve-file-path`）。

```text
.
├── AGENTS.md                      # Agent 向けプロジェクト規約（常時 Context）
├── README.md
├── apm.yml                        # APM 依存定義（任意）
├── .ai-agent/                     # Agent 作業領域（gitignore・単数形のみ）
│   ├── .gitignore
│   ├── tmp/                       # 使い捨てスクリプト・ログ・下書き
│   ├── plan/                      # 実行中・レビュー中の計画 (*.md)
│   │   └── done/                  # 完了した計画
│   └── memory/                    # 調査結果・引き継ぎ Memory (*.md)
│       └── done/                  # 用済み Memory
├── docs/                          # 技術ドキュメント正本（markdown-*）
└── apm_modules/                   # APM 依存の展開先. AI Agentの固有アセットの探索先としても参照される.
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

* 一時ファイルが必要な作業で、`.ai-agent/` 配下の配置先（`tmp` / `plan` / `memory`）を提案する。
* 一時スクリプトや調査下書きは `.ai-agent/tmp/`、実行計画は `.ai-agent/plan/` に置く。
* `.ai-agent/` ひな形そのものは `workspace-layout` を参照する。

### workspace-count-tokens

* Cursor ワークスペースのデフォルト Context と、動的ロード時の SKILL.md / docs・references の最大トークンを概算する。

### workspace-layout

* AI Agent 協業向けの推奨ワークスペース・レイアウト（ルート構成）を伝える。
* `AGENTS.md` / `docs/` / `.ai-agent/` 等の配置推奨と、不足時の `.ai-agent/` ひな形導入を担う。
* 一時ファイルの置き場提案は `workspace-agent-temporary` に委譲する。

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
