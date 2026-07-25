# ai-agent-headquarters

## このリポジトリについて

* @eaglesakura が個人開発時に使用するSKILLやSub Agent等のAI Agent設定集である
* 基本的に @eaglesakura 個人の開発者としての宗教観・設計・趣味に基づいている
* 基本的にCursorで使用することを想定している
* すべて日本語で記載されており、Token数の最適化については考慮されていない

## `.cursor/` 配下の構成

開発時のローカル配置用。公開する実体は `packages/*` の APM パッケージに集約する（このリポジトリの `.cursor/` は空でもよい）。

| パス（利用者ワークスペース） | 役割 |
| --- | --- |
| `.cursor/commands/` | `apm install` 後に展開される Slash Command |
| `.cursor/agents/` | `apm install` 後に展開される Sub Agent |
| `.agents/skills/` | `apm install` 後に展開される SKILL バンドル |
| `apm_modules/.../.apm/assets/` | パッケージ固有アセット（`{assets}/` 経由で参照） |

## APM Packages

SKILL / Prompt / Agent / 共有アセットは APM パッケージとして `packages/` 配下に置く。

| パッケージ | パス | 依存の書き方 |
| --- | --- | --- |
| `armyknife` | [`packages/armyknife`](packages/armyknife) | `eaglesakura/agent-skills/packages/armyknife` |
| `armyknife-cursor` | [`packages/armyknife-cursor`](packages/armyknife-cursor) | `eaglesakura/agent-skills/packages/armyknife-cursor` |
| `coding-xm3` | [`packages/coding-xm3`](packages/coding-xm3) | `eaglesakura/agent-skills/packages/coding-xm3` |
| `flutter` | [`packages/flutter`](packages/flutter) | `eaglesakura/agent-skills/packages/flutter` |
| `golang` | [`packages/golang`](packages/golang) | `eaglesakura/agent-skills/packages/golang` |

```yaml
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/armyknife
    - eaglesakura/agent-skills/packages/armyknife-cursor
    - eaglesakura/agent-skills/packages/coding-xm3
    - eaglesakura/agent-skills/packages/flutter
    - eaglesakura/agent-skills/packages/golang
```

## 収録Slash-Command

※ APM パッケージの `.apm/prompts/` が正本（アルファベット順）。

### coding.*（APM: `coding-xm3`）

* メインの3ステップ（要件 → 詳細設計 → 実施）の手順は [coding-command](docs/coding-command.md) を参照する。
* `coding.comment`・`coding.format-plan` は同系の補助コマンドである。
* 実体: [`packages/coding-xm3/.apm/prompts/`](packages/coding-xm3/.apm/prompts/)

#### coding.comment

* 指定スコープのコードコメント粒度をプロジェクト方針に合わせて適正化する。
* 言語に応じた SKILL・ドキュメントをロードし、コメントは原則として追記のみとし、関連コードとコメントの整合を確認する。
* Internal / Private でも Public と同等のコメント基準とし、関数・メソッドには言語の記法に沿った example を含める。

#### coding.design

* Coding-Commands のステップ2である（`/coding.requirement` → `/coding.design` → `/coding.execute`）。
* 要件を踏まえアーキテクチャを確認し、ジュニアエンジニアが実装可能な粒度の詳細設計を計画ファイルへ反映する。
* 出力フォーマットは `{assets}/coding/design.md`（`coding-xm3`）に準ずる。計画ファイルは `.ai-agent/plan/*.md` を上書き保存する。

#### coding.execute

* Coding-Commands のステップ3である。事前に構築された計画に基づき実装を反映する。
* 計画ファイルと作業範囲を読み、`coding-assistant.junior-engineer` 等の Sub Agent へテンプレートに沿った指示を渡す手順を規定する。

#### coding.format-plan

* `/coding.*` 用の補助コマンド。対象の計画ファイルを `{assets}/coding/requirements.md` または `{assets}/coding/design.md` の書式に沿って整理し、レビュアー・実装者の読解負荷を下げる。
* ガードレールとして、書式整理のみとし、要件・詳細設計・実施内容の意味を変えない。
* 詳細設計モードでは作業手順を `ステップ1` から始まるようインデックスを整える。

#### coding.requirement

* Coding-Commands のステップ1である。
* 要件の初期案から実装計画を `.ai-agent/plan/{計画名}.md` に保存する。出力フォーマットは `{assets}/coding/requirements.md` に準ずる。
* ガードレールとして、計画・レビュー関連ファイル以外の変更を行わない要件定義モードを規定する。

### github.create-pull-request（APM: `armyknife`）

* ブランチでの作業完了後に Pull Request を作成する、または既存 PR の本文を更新する。
* 実体: [`packages/armyknife/.apm/prompts/github.create-pull-request.prompt.md`](packages/armyknife/.apm/prompts/github.create-pull-request.prompt.md)
* 差分の整理・[Pull Request テンプレート](packages/armyknife/.apm/assets/github.create-pull-request/template.md) による本文作成・`gh pr create` / `gh pr edit` の利用を手順として規定する。
* 対象リポジトリ・base ブランチ・既存 Pull Request URL はオプションで指定できる。

### plan.init（APM: `coding-xm3`）

* Plan モード開始前に Agent の初期化ルールを適用する。ユーザーへの提案書式は `{assets}/plan/plan-mode.md` に従う。
* 計画の粒度はシニアエンジニアが作業可能な水準を目安とし、詳細化指示時はジュニアエンジニアが扱えるレベルまで落とす。
* 積極的に SKILL（例: `engineer-software-requirement`・`engineer-software-design`）と Sub Agent レビュー（例: `coding-assistant.plan-reviewer`・`coding-assistant.requirement-reviewer`）を利用する。

## 収録Sub-Agents

※ APM: `coding-xm3` の `.apm/agents/` が正本（アルファベット順）。

### coding.* 関連

#### coding-assistant.junior-engineer

* ジュニアエンジニア職能として、与えられた実装計画から逸脱しない範囲で実装を行う。
* `engineer-software-design` と `{assets}/coding/design.md` を参照する。
* 計画確認・宣誓・中断時は親 Agent へ報告する。

#### coding-assistant.plan-reviewer

* ジュニアエンジニア職能の前提で、実装計画の実現性可否を判断する（`readonly`・バックグラウンド実行想定）。
* `agent-job-description` 等の職能定義と照らし、計画逸脱なく実行可能かをチェックリスト形式で親 Agent に返す。

#### coding-assistant.requirement-reviewer

* 要件定義のレビュアー。不足・不明瞭な要件の洗い出しと判断材料の提示を行う（`readonly`・バックグラウンド実行想定）。
* `engineer-software-requirement` と `{assets}/coding/requirements.md` を参照する。

#### coding-assistant.senior-engineer

* シニアエンジニア職能として、要件達成に必要な最小限の計画逸脱を認めつつ計画範囲内で自律的にコーディングする。
* `engineer-software-design` と `{assets}/coding/design.md` を参照する。

#### coding-assistant.software-design-audit

* 詳細設計・実装の監査役。`markdown-search` で根拠を集め、シニア職能の物差しで評価する。
* `agent-job-description`・`engineer-software-design`・`{assets}/coding/design.md` を参照する。

#### coding-assistant.software-design-reviewer

* 詳細設計ドキュメントや実装のレビュアー。指摘は要約せず一覧で親 Agent に渡す（`readonly`・バックグラウンド実行想定）。
* `engineer-software-design` と `{assets}/coding/design.md` を参照する。

## 補助ファイル（テンプレート）

Slash Command または SKILL から `{assets}/...` で参照する。正本は各パッケージの `.apm/assets/`。解決は `workspace-resolve-agent-assets` に従う。

| ファイル | 参照元の例 |
| --- | --- |
| [assets/coding/design.md](packages/coding-xm3/.apm/assets/coding/design.md) | `/coding.design`、詳細設計レビュー・ジュニア／シニア Engineer Agent |
| [assets/coding/requirements.md](packages/coding-xm3/.apm/assets/coding/requirements.md) | `/coding.requirement`、要件レビュアー、`engineer-software-requirement` |
| [assets/coding.execute/work-orders.md](packages/coding-xm3/.apm/assets/coding.execute/work-orders.md) | `/coding.execute` |
| [assets/plan/plan-mode.md](packages/coding-xm3/.apm/assets/plan/plan-mode.md) | `/plan.init` |
| [assets/github.create-pull-request/template.md](packages/armyknife/.apm/assets/github.create-pull-request/template.md) | `/github.create-pull-request`（`armyknife`） |

## 収録SKILL一覧

※ APM パッケージの `.apm/skills/` 配下（アルファベット順）。パッケージ未収録の説明は省略し、主なものを列挙する。

### agent-job-description（APM: `coding-xm3`）

* ジュニア／シニア等の職能ごとの技能範囲を定義し、依頼内容をその前提に合わせる。
* 「ジュニアエンジニアが作業可能」などレベル指定時に、許容される作業・避けるべき抽象度を揃える。
* 計画書・コードコメントの粒度など、職能に応じた要件を SKILL 本文で規定する。

### engineer-software-design（APM: `coding-xm3`）

* 要件を満たす詳細設計を行い、変更内容を提案する。実装計画（プランニング）時はロードすることが前提となる。
* **コード変更は行わず**、要件確認・関連ドキュメント調査・設計出力に特化する。
* コードレビュー用途の SKILL と併用することが望ましい。

### engineer-software-requirement（APM: `coding-xm3`）

* 要件定義に特化し、適切な要件定義ドキュメントの出力を行う。
* **コード変更は行わず**、`{assets}/coding/requirements.md` に沿って整理する。
* 完了条件・前提・テスト観点・影響範囲などを SKILL の手順で確認する。

### workspace-agent-memory-save

* 調査結果や会話サマリを不揮発の Memory として保存する手順を規定する。
* 出力先は `.ai-agent/memory/{文脈内容}.md` とし、既存があれば更新する。
* テンプレートと見出しレベル単位の構造により、後続チャットでのロードしやすさを確保する。

### workspace-agent-temporary

* AI Agent が使ってよい一時領域（`.ai-agent/`）のルート・サブディレクトリ・Ignore を規定する。
* 一時スクリプトや調査メモは `.ai-agent/tmp/`、実行計画は `.ai-agent/plan/` に置く。
* `assets/` の構成を参考にディレクトリを用意し、コミット対象外とする。

### flutter-coding-rules

* Flutter / Dart のコーディング規約遵守用 SKILL。`*.dart` の実装・修正時に必ず従う。
* データオブジェクト・Delegate パターン・コメント・可視性・ファイルレイアウト・enum・例外処理などのルールを定める。
* 文脈に応じて `references/` の追加ドキュメントをロードして詳細を満たす。

### flutter-layered-architecture-code-search

* コードベースのドキュメントや既存コードの「場所」の詳細調査に特化する。
* 指定された機能・アーキテクチャ・パッケージ・ソースに対応するファイル・ツリーをレポートする。
* TODO/FIXME やコメントから推測される留意事項も出力に含める。

### flutter-layered-architecture-design

* Flutter-Layered-Architecture の全体設計（dart workspace によるモノリス・レイヤー構成）を規定する。
* app / screen / view / usecase / data / infra / domain / foundation 等のレイヤーと package プレフィックス・役割を定義する。
* DI（Riverpod）によるインターフェースと実装の分離、および「ビジネスロジック＝Usecase」の考え方を示す。

### flutter-layered-architecture-design-patterns

* Flutter-Layered-Architecture 向けの汎用デザインパターン（Usecase・Repository 等）を規定する。
* Usecase は 1 インターフェース 1 機能と Request/Result パターン、Repository は Read/Write の抽象化として設計する。
* Repository と Usecase の依存関係と、循環参照を避けるための Riverpod `Provider.dependencies` の扱いを定める。

### flutter-layered-architecture-library-update

* Layered Architecture の推奨に沿って依存ライブラリの更新手順を規定する。
* `flutter pub outdated` で更新候補を確認し、ルート `pubspec.yaml` の `dependency_overrides` を更新する。
* `flutter pub get` 等で検証し、互換性の問題で上げられないバージョンはスキップする。

### flutter-layered-architecture-screen-mvvm

* Screen 層の Model-View-ViewModel 設計 SKILL。画面の設計・開発時に必須とする。
* Riverpod / Hooks / StateStream / freezed 等を用いた View/ViewModel/State/Entity/Event の設計を規定する。
* 関連参照ドキュメント（ViewModel 設計・Entity・Usecase・State・Event・View・テスト）に従って実装する。

### flutter-layered-architecture-screen-navigation

* Flutter-Layered-Architecture の画面遷移設計能力を提供する。
* `screen_navigation` に Request/Result を集約し、`{画面名}Factory` と DI で画面間を疎結合にする。
* `go_router` を推奨し、`Navigator` の直接利用を避けてナビゲーションライブラリを隠蔽する。

### flutter-layered-architecture-workspace

* Dart workspace（ルート `pubspec.yaml` の `workspace:`）によるパッケージ一覧とレイアウトの把握手順を規定する。
* ルートの `dependency_overrides` による依存の一元管理と、`app/` でのビルド慣習を示す。
* レイヤードアーキテクチャ SKILL と併用し、変更対象パッケージの特定に使う。

### flutter-maintenance-check-latest-version

* Flutter SDK 自体の最新リリース調査手順を規定する（例: `gh api` で `flutter/flutter` の tags 取得）。
* `CHANGELOG.md` と `flutter --version` を照らし、採用候補バージョンの変更内容を把握する。

### flutter-monolith-localization

* CSV（`res/strings.csv`）による文字列の外部リソース化・L10n 対応と利用方法を規定する。
* `monolith` / `monolith_localization` を用い、`dart run monolith_runner:localization` でコード生成する。
* パッケージごとの `strings.dart` と `L10nStringsMixin` の使い方、他パッケージリソースの参照方法を定める。

### workspace-git-branch-rule

* `main`・`feature/id/...`・`release/...` などブランチ運用ルールを規定する。
* ブランチ名から Issue との対応や作業種別を推測する際の参照とする。
* `gh` でタスク内容を引くことと整合する命名規約を SKILL 本文で示す。

### github-actions-workflow-build

* GitHub Actions のワークフロー（`.github/**/*.yaml`）編集時に守るセキュリティ・運用ルールを規定する。
* 外部アクションは SHA ピン留めとし、`uses: org/action@tag` のような可変タグ指定を避ける。
* `gh api` 等でタグとコミット SHA を取得し、コメントで人間が追える形にする。

### golang-analyze

* Go のフォーマット・静的解析・テストなど、品質担保の実行タイミングとコマンドを規定する。
* `go fmt ./...`・`golangci-lint run ./...` 等をコーディング完了後に実行することを推奨する。
* `go.work` 起点のモジュール構成での実行場所にも言及する。

### golang-coding-rules

* `*.go` の実装・修正時に従うコーディング規約と実装パターンをまとめる。
* `references/general.md`・`data_object.md`・`code_comment.md` など文脈別ドキュメントを読み込む。
* データオブジェクト・公開 API のドキュメントコメントなど詳細ルールを参照で満たす。

### maintenance-measure-cache-size

* ローカル PC の開発ツールキャッシュ占有を調査し、大きなディレクトリを一覧する。
* パス・GiB・用途・復元可否・削除コマンドなどの出力フォーマットを規定する。
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

### workspace-resolve-url-metadata

* Issue URL 等からタスク ID・タイトルなど取得可能なメタデータを整理する。
* `gh issue view ... --json number,title` など CLI での取得例と JSON の読み方を示す。
* GitHub Issues の URL パターンごとのフィールド対応を SKILL 本文で規定する。
