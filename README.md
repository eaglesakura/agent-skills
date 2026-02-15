# ai-agent-headquarters

## このリポジトリについて

* @eaglesakura が個人開発時に使用するSKILLやSub Agent等のAI Agent設定集である
* 基本的に @eaglesakura 個人の開発者としての宗教観・設計・趣味に基づいている
* 基本的にCursorで使用することを想定している
* すべて日本語で記載されており、Token数の最適化については考慮されていない

## 収録SKILL一覧

### documentation.knowledge

* 技術ドキュメント作成・更新のための能力を提供する。
* Markdown形式を前提とし、`*.md` では必須のルール（文体・構造・実装例の形式など）を定める。
* 概要・原則・実装例・アンチパターンなどのセクション構成と記述ルールを規定する。

### markdown.fix

* Markdown（`*.md`）の Formatter と Lint を行う。
* `markdownlint-cli2` を用いて書式を統一し、可読性を確保する。
* 自動修正されない項目は Linter の警告に従い個別に対応する。

### flutter.monolith.localization

* CSV（`res/strings.csv`）による文字列の外部リソース化・L10n 対応と利用方法を規定する。
* `monolith` / `monolith_localization` を用い、`dart run monolith_runner:localization` でコード生成する。
* パッケージごとの `strings.dart` と `L10nStringsMixin` の使い方、他パッケージリソースの参照方法を定める。

### flutter.layered-architecture.software-librarian

* コードベースのドキュメントや既存コードの「場所」の詳細調査に特化する。
* 指定された機能・アーキテクチャ・パッケージ・ソースに対応するファイル・ツリーをレポートする。
* TODO/FIXME やコメントから推測される留意事項も出力に含める。

### flutter.layered-architecture.screen-navigation

* Flutter-Layered-Architecture の画面遷移設計能力を提供する。
* `screen_navigation` に Request/Result を集約し、`{画面名}Factory` と DI で画面間を疎結合にする。
* `go_router` を推奨し、`Navigator` の直接利用を避けてナビゲーションライブラリを隠蔽する。

### flutter.layered-architecture.screen-mvvm

* Screen 層の Model-View-ViewModel 設計 SKILL。画面の設計・開発時に必須とする。
* Riverpod / Hooks / StateStream / freezed 等を用いた View/ViewModel/State/Entity/Event の設計を規定する。
* 関連参照ドキュメント（ViewModel 設計・Entity・Usecase・State・Event・View・テスト）に従って実装する。

### flutter.layered-architecture.document-librarian

* コードレビューや要件定義のための「関連ドキュメント」を探し、Context に提示する。
* 計画・要件定義等の入力から、レビューに必要なドキュメントを `.cursor/skills/` や `docs/` から検索する。
* 発見したドキュメントのファイル名とレベル3までの要約を出力する。

### flutter.coding-rules

* Flutter / Dart のコーディング規約遵守用 SKILL。`*.dart` の実装・修正時に必ず従う。
* データオブジェクト・Delegate パターン・コメント・可視性・ファイルレイアウト・enum・例外処理などのルールを定める。
* 文脈に応じて `references/` の追加ドキュメントをロードして詳細を満たす。

### flutter.layered-architecture.design-patterns

* Flutter-Layered-Architecture 向けの汎用デザインパターン（Usecase・Repository 等）を規定する。
* Usecase は 1 インターフェース 1 機能と Request/Result パターン、Repository は Read/Write の抽象化として設計する。
* Repository と Usecase の依存関係と、循環参照を避けるための Riverpod `Provider.dependencies` の扱いを定める。

### flutter.layered-architecture.design

* Flutter-Layered-Architecture の全体設計（dart workspace によるモノリス・レイヤー構成）を規定する。
* app / screen / view / usecase / data / infra / domain / foundation 等のレイヤーと package プレフィックス・役割を定義する。
* DI（Riverpod）によるインターフェースと実装の分離、および「ビジネスロジック＝Usecase」の考え方を示す。
