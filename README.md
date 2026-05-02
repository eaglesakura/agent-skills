# ai-agent-headquarters

## このリポジトリについて

* @eaglesakura が個人開発時に使用するSKILLやSub Agent等のAI Agent設定集である
* 基本的に @eaglesakura 個人の開発者としての宗教観・設計・趣味に基づいている
* 基本的にCursorで使用することを想定している
* すべて日本語で記載されており、Token数の最適化については考慮されていない

## `.cursor/` 配下の構成

| パス | 役割 |
| --- | --- |
| `.cursor/command/` | Slash Command 本体（`/コマンド名` で起動する Markdown） |
| `.cursor/agents/` | Sub Agent 定義（職能・レビュアーなどのハーネス） |
| `.cursor/extra/` | コマンド・SKILL から参照するテンプレート・補助原稿 |
| `.cursor/skills/` | Cursor Agent Skills（ディレクトリ名が SKILL 識別子に対応） |

## 収録Slash-Command

※ `.cursor/command/` 直下の Markdown ファイルと対応する（アルファベット順）。サブディレクトリ内はテンプレート等であり、Slash Command 本体ではない。

### coding.*

* 詳細は [coding-command](docs/coding-command.md)

#### coding.requirement

* Coding-Commands のステップ1である。
* 要件の初期案から実装計画を `.ai-agent/plan/{計画名}.md` に保存する。出力フォーマットは [extra/coding/requirements.md](.cursor/extra/coding/requirements.md) に準ずる。
* ガードレールとして、計画・レビュー関連ファイル以外の変更を行わない要件定義モードを規定する。

#### coding.design

* Coding-Commands のステップ2である（`/coding.requirement` → `/coding.design` → `/coding.execute`）。
* 要件を踏まえアーキテクチャを確認し、ジュニアエンジニアが実装可能な粒度の詳細設計を計画ファイルへ反映する。
* 出力フォーマットは [extra/coding/design.md](.cursor/extra/coding/design.md) に準ずる。計画ファイルは `.ai-agent/plan/*.md` を上書き保存する。

#### coding.execute

* Coding-Commands のステップ3である。事前に構築された計画に基づき実装を反映する。
* 計画ファイルと作業範囲を読み、`coding-assistant.junior-engineer` 等の Sub Agent へテンプレートに沿った指示を渡す手順を規定する。

### github.create-pull-request

* ブランチでの作業完了後に Pull Request を作成する、または既存 PR の本文を更新する。
* 差分の整理・[Pull Request テンプレート](.cursor/extra/github.create-pull-request/template.md) による本文作成・`gh pr create` / `gh pr edit` の利用を手順として規定する。
* 対象リポジトリ・base ブランチ・既存 Pull Request URL はオプションで指定できる。

## 収録Sub-Agents

※ `.cursor/agents/` 直下の Markdown と対応する（アルファベット順）。

### coding-assistant.junior-engineer

* ジュニアエンジニア職能として、与えられた実装計画から逸脱しない範囲で実装を行う。
* [engineer.software-design](.cursor/skills/engineer.software-design/SKILL.md) と [詳細設計テンプレート](.cursor/extra/coding/design.md) を参照する。
* 計画確認・宣誓・中断時は親 Agent へ報告する。

### coding-assistant.requirement-reviewer

* 要件定義のレビュアー。不足・不明瞭な要件の洗い出しと判断材料の提示を行う（`readonly`・バックグラウンド実行想定）。
* [engineer.software-requirement](.cursor/skills/engineer.software-requirement/SKILL.md) と [要件定義フォーマット](.cursor/extra/coding/requirements.md) を参照する。

### coding-assistant.senior-engineer

* シニアエンジニア職能として、要件達成に必要な最小限の計画逸脱を認めつつ計画範囲内で自律的にコーディングする。
* [engineer.software-design](.cursor/skills/engineer.software-design/SKILL.md) と [詳細設計テンプレート](.cursor/extra/coding/design.md) を参照する。

### coding-assistant.software-design-reviewer

* 詳細設計ドキュメントや実装のレビュアー。指摘は要約せず一覧で親 Agent に渡す（`readonly`・バックグラウンド実行想定）。
* [engineer.software-design](.cursor/skills/engineer.software-design/SKILL.md) と [詳細設計テンプレート](.cursor/extra/coding/design.md) を参照する。

## `.cursor/extra/` 補助ファイル

Slash Command または SKILL からパス参照されるテンプレートである。

| ファイル | 参照元の例 |
| --- | --- |
| [extra/coding/design.md](.cursor/extra/coding/design.md) | `/coding.design`、詳細設計レビュー・ジュニア／シニア Engineer Agent |
| [extra/coding/requirements.md](.cursor/extra/coding/requirements.md) | `/coding.requirement`、要件レビュアー Agent、[engineer.software-requirement](.cursor/skills/engineer.software-requirement/SKILL.md) |
| [extra/github.create-pull-request/template.md](.cursor/extra/github.create-pull-request/template.md) | `/github.create-pull-request` |

## 収録SKILL一覧

※ `.cursor/skills/` 配下のディレクトリ名と対応する（アルファベット順）。

### agent.job-description

* ジュニア／シニア等の職能ごとの技能範囲を定義し、依頼内容をその前提に合わせる。
* 「ジュニアエンジニアが作業可能」などレベル指定時に、許容される作業・避けるべき抽象度を揃える。
* 計画書・コードコメントの粒度など、職能に応じた要件を SKILL 本文で規定する。

### agent.memory.save

* 調査結果や会話サマリを不揮発の Memory として保存する手順を規定する。
* 出力先は `.ai-agent/memory/{文脈内容}.md` とし、既存があれば更新する。
* テンプレートと見出しレベル単位の構造により、後続チャットでのロードしやすさを確保する。

### agent.temporary

* AI Agent が使ってよい一時領域（`.ai-agent/`）のルート・サブディレクトリ・Ignore を規定する。
* 一時スクリプトや調査メモは `.ai-agent/tmp/`、実行計画は `.ai-agent/plan/` に置く。
* `assets/` の構成を参考にディレクトリを用意し、コミット対象外とする。

### engineer.software-design

* 要件を満たす詳細設計を行い、変更内容を提案する。実装計画（プランニング）時はロードすることが前提となる。
* **コード変更は行わず**、要件確認・関連ドキュメント調査・設計出力に特化する。
* コードレビュー用途の SKILL と併用することが望ましい。

### engineer.software-requirement

* 要件定義に特化し、適切な要件定義ドキュメントの出力を行う。
* **コード変更は行わず**、[要件定義フォーマット](.cursor/extra/coding/requirements.md) に沿って整理する。
* 完了条件・前提・テスト観点・影響範囲などを SKILL の手順で確認する。

### flutter.coding-rules

* Flutter / Dart のコーディング規約遵守用 SKILL。`*.dart` の実装・修正時に必ず従う。
* データオブジェクト・Delegate パターン・コメント・可視性・ファイルレイアウト・enum・例外処理などのルールを定める。
* 文脈に応じて `references/` の追加ドキュメントをロードして詳細を満たす。

### flutter.layered-architecture.code-search

* コードベースのドキュメントや既存コードの「場所」の詳細調査に特化する。
* 指定された機能・アーキテクチャ・パッケージ・ソースに対応するファイル・ツリーをレポートする。
* TODO/FIXME やコメントから推測される留意事項も出力に含める。

### flutter.layered-architecture.design

* Flutter-Layered-Architecture の全体設計（dart workspace によるモノリス・レイヤー構成）を規定する。
* app / screen / view / usecase / data / infra / domain / foundation 等のレイヤーと package プレフィックス・役割を定義する。
* DI（Riverpod）によるインターフェースと実装の分離、および「ビジネスロジック＝Usecase」の考え方を示す。

### flutter.layered-architecture.design-patterns

* Flutter-Layered-Architecture 向けの汎用デザインパターン（Usecase・Repository 等）を規定する。
* Usecase は 1 インターフェース 1 機能と Request/Result パターン、Repository は Read/Write の抽象化として設計する。
* Repository と Usecase の依存関係と、循環参照を避けるための Riverpod `Provider.dependencies` の扱いを定める。

### flutter.layered-architecture.screen-mvvm

* Screen 層の Model-View-ViewModel 設計 SKILL。画面の設計・開発時に必須とする。
* Riverpod / Hooks / StateStream / freezed 等を用いた View/ViewModel/State/Entity/Event の設計を規定する。
* 関連参照ドキュメント（ViewModel 設計・Entity・Usecase・State・Event・View・テスト）に従って実装する。

### flutter.layered-architecture.screen-navigation

* Flutter-Layered-Architecture の画面遷移設計能力を提供する。
* `screen_navigation` に Request/Result を集約し、`{画面名}Factory` と DI で画面間を疎結合にする。
* `go_router` を推奨し、`Navigator` の直接利用を避けてナビゲーションライブラリを隠蔽する。

### flutter.monolith.localization

* CSV（`res/strings.csv`）による文字列の外部リソース化・L10n 対応と利用方法を規定する。
* `monolith` / `monolith_localization` を用い、`dart run monolith_runner:localization` でコード生成する。
* パッケージごとの `strings.dart` と `L10nStringsMixin` の使い方、他パッケージリソースの参照方法を定める。

### git.branch-rule

* `main`・`feature/id/...`・`release/...` などブランチ運用ルールを規定する。
* ブランチ名から Issue との対応や作業種別を推測する際の参照とする。
* `gh` でタスク内容を引くことと整合する命名規約を SKILL 本文で示す。

### golang.analyze

* Go のフォーマット・静的解析・テストなど、品質担保の実行タイミングとコマンドを規定する。
* `go fmt ./...`・`golangci-lint run ./...` 等をコーディング完了後に実行することを推奨する。
* `go.work` 起点のモジュール構成での実行場所にも言及する。

### golang.coding-rules

* `*.go` の実装・修正時に従うコーディング規約と実装パターンをまとめる。
* `references/general.md`・`data_object.md`・`code_comment.md` など文脈別ドキュメントを読み込む。
* データオブジェクト・公開 API のドキュメントコメントなど詳細ルールを参照で満たす。

### maintenance.measure-cache-size

* ローカル PC の開発ツールキャッシュ占有を調査し、大きなディレクトリを一覧する。
* パス・GiB・用途・復元可否・削除コマンドなどの出力フォーマットを規定する。
* OS ごとの探索対象ディレクトリとしきい値（例: 10GiB 超で深掘り）を SKILL 本文で示す。

### markdown.documentation

* Markdown での技術ドキュメント作成・更新のための SKILL。`*.md` の差分提案時はロードする。
* 「である」調・必須セクション（概要・よくあるパターンとアンチパターン）・原則ごとの補足・実装例・アンチパターンを規定する。
* コード引用や見出しレベルなど、Markdown の具体的な記述ルールを SKILL 本文で詳述する。

### markdown.fix

* Markdown（`*.md`）の Formatter と Lint を行う。
* `markdownlint-cli2` を用いて書式を統一し、可読性を確保する。
* 自動修正されない項目は Linter の警告に従い個別に対応する。

### markdown.search

* ワークスペース内ドキュメント（主に `**/docs/**/*.md` 等）の探索・把握手順を規定する。
* `README.md`・`.cursor/`・`.ai-agent/memory/` など優先パスと、grep による見出し一覧の切り方を示す。
* 構造把握後に本文を読む流れで、広いリポジトリでも迷わないようにする。

### parse.url-to-metadata

* Issue URL 等からタスク ID・タイトルなど取得可能なメタデータを整理する。
* `gh issue view ... --json number,title` など CLI での取得例と JSON の読み方を示す。
* GitHub Issues の URL パターンごとのフィールド対応を SKILL 本文で規定する。
