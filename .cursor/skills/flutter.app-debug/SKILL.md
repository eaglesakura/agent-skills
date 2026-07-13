---
name: flutter.app-debug
description: `launch.json` をベースにアプリの起動やデバッグを行うためのSKILL. MCPを経由して自律的にアプリを制御し、実装の妥当性検証やデバッグを行う. AI Agentからの起動と、DTDによるアタッチをサポートする.
license: MIT License
metadata:
  author: "@eaglesakura"
---

# Flutter / アプリデバッグ・起動、アタッチ

## Flutterの起動構成の把握

* `.vscode/launch.json` を読み込む
* `type` が `dart` かつ `request` が `launch` の構成を、起動構成として認識する
  * `flutterMode` がある場合は、その値（`debug` / `profile` / `release`）を実行モードとする
  * `flutterMode` が無い場合は、`debug` として扱う
* 起動時は、構成の `cwd` / `program` / `args` / `deviceId` を引き継ぐ
  * `args` に含まれる `--flavor` や `--dart-define-from-file` 等も省略しない

## 起動対象の把握

* flutterコマンドを使用し、接続されているデバイスを列挙する

```bash
flutter devices
```

* プロンプトや文脈から、起動対象のデバイスを判断する
  * デバイスが1つのみの場合は、暗黙的に決定する
  * launch構成に `deviceId` がある場合は、それを優先する
* 対象は、常に1つである
  * 対象を判別できない場合、下記のようなテキストを出力して処理を中断する

  ```markdown
  起動対象のデバイスを確定できませんでした。
  対象デバイスを指定してください。
  ```

## 実行

### アプリを起動する

* 既定の Dart MCP にはアプリ起動ツール（`launch_app` 等）が無効化されている
  * そのため、起動はシェルの `flutter run` で行う
* launch構成と選択デバイスから、次の形で起動する
  * `--print-dtd` は必須とする（後続の MCP 接続に使う）
  * `cwd` を作業ディレクトリとし、`program` と `args` を引き継ぐ
  * `flutterMode` が `profile` / `release` の場合は、それぞれ `--profile` / `--release` を付与する

```bash
flutter run -d ${deviceId} --print-dtd ${modeFlags} ${program} ${args}
```

* 起動ログに出力される `DTD URI`（`ws://...`）を控える
  * `http://...` 形式の VM Service URI は DTD URI ではない。混同しない

### 起動中のアプリにアタッチする

#### DTD URIを取得する

* 次の順で DTD URI を確定する
  1. 直前の `flutter run --print-dtd` 出力
  2. プロンプトやユーザー指示
  3. Dart MCP の `dtd` ツール（`listDtdUris`）
     * working dir がホームディレクトリに見える DTD は、IDE 起動アプリの候補として優先する
* DTD URIが認識できない場合、次のようなテキストを出力して終了する

```markdown
DTD URIが認識できませんでした。
DTD URIを指定してください。

例: `ws://127.0.0.1:63514/...`
```

#### DTDに接続する

* Dart MCP の `dtd` ツールで接続する
  * `connect` に確定した DTD URI を渡す
  * 必要に応じて `listConnectedApps` で接続済みアプリを確認する
* 複数アプリが接続されている場合は、操作対象の `appUri` を明示する

#### アプリを制御・検証する

* DTD 接続後、目的に応じて次の Dart MCP ツールを使う
  * `get_runtime_errors` … ランタイムエラーの確認
  * `widget_inspector` … Widget ツリーの取得・選択状態の確認
  * `flutter_driver_command` … タップ、テキスト入力、スクショ等の操作
    * 操作前に `widget_inspector`（`get_widget_tree`）で実在する Widget を確認し、推測でセレクタを作らない
  * `hot_reload` / `hot_restart` … コード変更の反映
* UI 自動操作（Maestro MCP）が必要な場合は、本SKILLの Dart MCP 制御と用途を混同しない
  * Flutter 内部の状態・エラー・Widget 検査は Dart MCP
  * 端末上の黒箱 UI 操作は Maestro MCP

## ナレッジベース

### DO: `mise exec --` 等のプロジェクト規定prefixが存在する場合は、prefixを付与する

* `fvm` や `mise` 等、プロジェクト固有の管理ツールがある場合は、そのルールに従う
