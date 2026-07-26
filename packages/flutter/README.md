# flutter

Flutter / Dart 向け SKILL 集である。
コーディング規約、Layered Architecture、デバッグ、L10n、SDK 調査などをまとめる。

## Quick Start

```yaml
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/flutter
```

## 依存APM Package

* `eaglesakura/agentic-workspace`

## SKILLS

※ `.apm/skills/` 配下（アルファベット順）。

### flutter-app-debug

* Flutter アプリの実機／エミュ起動・DTD アタッチ・ランタイムデバッグ用 SKILL。
* `launch.json` 読取、`flutter devices` / `flutter run --print-dtd`、Dart MCP（DTD）での検査・操作を規定する。
* Maestro の黒箱 UI テストとは役割を分け、VM Service（`http://`）と DTD（`ws://`）を混同しない。

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

## Commands

なし。

## Sub Agents

なし。
