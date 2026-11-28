# flutter

Flutter / Dart 向け SKILL 集である。
コーディング規約、Layered Architecture、デバッグ、SDK 調査などをまとめる。
monolith L10n は `eaglesakura/flutter_monolith/skills` 側へ移行した。
workspace 構造把握、コーディング規約（`coding-rules`）、外部依存管理（`dependencies`）、
Usecase / Repository / Screen MVVM / 画面遷移設計
（`design-usecase` / `design-repository` / `design-screen-mvvm` / `design-screen-navigation`）、
および annotations / linter rule SKILL は
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

### flutter-layered-architecture-coding-rules（移行済み）

* `eaglesakura/flutter_layered_architecture` の `flutter-layered-architecture-coding-rules` へ移行した。
* コメント・DTO・enum・例外・Delegate 切り出し判断などは、そちらの APM パッケージを使う。
* `@delegate` / `@state` / `@entity` 等の構造保証は annotations / linter-rule が正本である。

### flutter-layered-architecture-code-search（削除）

* 廃止した。機能・package の所在調査は `eaglesakura/flutter_layered_architecture` の
  `flutter-layered-architecture-workspace`（＋必要なら `resolve-package-layer`）で足りる。

### flutter-layered-architecture-design（移行済み）

* `eaglesakura/flutter_layered_architecture` の `flutter-layered-architecture-design-usecase` へ移行した。
* Usecase の切り出し・共通／画面固有・命名など設計判断は、そちらの APM パッケージを使う。
* レイヤー地図・依存方向は `resolve-package-layer` / architecture linter、構造は usecase linter が保証する。

### flutter-layered-architecture-design-patterns（移行済み）

* `eaglesakura/flutter_layered_architecture` の `flutter-layered-architecture-design-repository` へ移行した。
* Repository の窓口・状態・DataInjection・テスト差し替えは、そちらの APM パッケージを使う。

### flutter-layered-architecture-dependencies（移行済み）

* 旧 `flutter-layered-architecture-library-update`。
* `eaglesakura/flutter_layered_architecture` の `flutter-layered-architecture-dependencies` へ移行した。
* 外部 pub はルートに実効版・worktree は `any`、追加・outdated・検証はそちらを使う。

### flutter-layered-architecture-design-screen-mvvm（移行済み）

* `eaglesakura/flutter_layered_architecture` の `flutter-layered-architecture-design-screen-mvvm` へ移行した。
* Screen / ScreenImpl・State/Entity/Event の役割・`onXXXX` 設計判断は、そちらの APM パッケージを使う。
* `@viewModel` 等の構造保証は annotations / linter-rule が正本である。

### flutter-layered-architecture-design-screen-navigation（移行済み）

* `eaglesakura/flutter_layered_architecture` の `flutter-layered-architecture-design-screen-navigation` へ移行した。
* Factory / Launcher / Finisher / Proxy・Request/Result・go_router の置き場所は、そちらの APM パッケージを使う。

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
