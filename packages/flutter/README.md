# flutter

Flutter / Dart 向け SKILL 集である。
コーディング規約、Layered Architecture、デバッグ、SDK 調査などをまとめる。
monolith L10n は `eaglesakura/flutter_monolith/skills` 側へ移行した。
workspace 構造把握、Usecase / Repository / Screen MVVM 設計
（`design-usecase` / `design-repository` / `design-screen-mvvm`）、および annotations / linter rule SKILL は
`eaglesakura/flutter_layered_architecture` 側へ移行した（またはそちらが正本である）。

## Quick Start

```yaml
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/flutter
```

## 依存APM Package

* `eaglesakura/agent-skills/packages/agentic-workspace`

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

### flutter-layered-architecture-design（移行済み）

* `eaglesakura/flutter_layered_architecture` の `flutter-layered-architecture-design-usecase` へ移行した。
* Usecase の切り出し・共通／画面固有・命名など設計判断は、そちらの APM パッケージを使う。
* レイヤー地図・依存方向は `resolve-package-layer` / architecture linter、構造は usecase linter が保証する。

### flutter-layered-architecture-design-patterns（移行済み）

* `eaglesakura/flutter_layered_architecture` の `flutter-layered-architecture-design-repository` へ移行した。
* Repository の窓口・状態・DataInjection・テスト差し替えは、そちらの APM パッケージを使う。

### flutter-layered-architecture-library-update

* Layered Architecture の推奨に沿って依存ライブラリの更新手順を規定する。
* `flutter pub outdated` で更新候補を確認し、ルート `pubspec.yaml` の `dependency_overrides` を更新する。
* `flutter pub get` 等で検証し、互換性の問題で上げられないバージョンはスキップする。

### flutter-layered-architecture-design-screen-mvvm（移行済み）

* `eaglesakura/flutter_layered_architecture` の `flutter-layered-architecture-design-screen-mvvm` へ移行した。
* Screen / ScreenImpl・State/Entity/Event の役割・`onXXXX` 設計判断は、そちらの APM パッケージを使う。
* `@viewModel` 等の構造保証は annotations / linter-rule が正本である。

### flutter-layered-architecture-screen-navigation

* Flutter-Layered-Architecture の画面遷移設計能力を提供する。
* `screen_navigation` に Request/Result を集約し、`{画面名}Factory` と DI で画面間を疎結合にする。
* `go_router` を推奨し、`Navigator` の直接利用を避けてナビゲーションライブラリを隠蔽する。

### flutter-layered-architecture-workspace（移行済み）

* `eaglesakura/flutter_layered_architecture`（`.apm/skills/flutter-layered-architecture-workspace`）へ移行した。
* dart workspace の package 一覧・アプリ入口の把握は、そちらの APM パッケージをインストールして使う。

### flutter-maintenance-check-latest-version

* Flutter SDK 自体の最新リリース調査手順を規定する（例: `gh api` で `flutter/flutter` の tags 取得）。
* `CHANGELOG.md` と `flutter --version` を照らし、採用候補バージョンの変更内容を把握する。

## Commands

なし。

## Sub Agents

なし。
