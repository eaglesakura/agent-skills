# Swift Package Manager（SPM）前提

本 SKILL ファミリーは **CocoaPods を使わない**。Flutter プラグインのネイティブ依存は SPM（`FlutterGeneratedPluginSwiftPackage`）で解決する。

Flutter 3.44 以降は SPM が既定。それより前では `flutter config --enable-swift-package-manager` が必要な場合がある。プロジェクトで SPM を無効化している場合は、先に有効化してから本手順に進む。

## project.yml の packages

```yaml
packages:
  FlutterGeneratedPluginSwiftPackage:
    path: Flutter/ephemeral/Packages/FlutterGeneratedPluginSwiftPackage
```

* path は `ios/`（xcodegen 実行ディレクトリ）からの相対パス
* 実体は Flutter が生成する。リポジトリにコミットしない（通常は `.gitignore`）

Runner の `dependencies` に同じパッケージをリンクする。

```yaml
dependencies:
  - sdk: CoreGraphics.framework
  - package: FlutterGeneratedPluginSwiftPackage
```

## CoreGraphics を残す理由

`packages` に SPM を足したあと、実質の package / product 依存が空に近いと Xcode の SPM 解決が失敗することがある。無害な SDK framework（`CoreGraphics.framework`）を `dependencies` に残す。外さない。

## Scheme の prepare preAction

Flutter SPM ビルドでは、ビルド前に `xcode_backend.sh prepare` が必要。`xcodegen/base.yml` の `schemeTemplates.FlutterFlavorSchema` が担う。

```yaml
schemeTemplates:
  FlutterFlavorSchema:
    build:
      preActions:
        - name: "[Flutter] Run Prepare Flutter Framework Script"
          settingsTarget: Runner
          script: '"$FLUTTER_ROOT/packages/flutter_tools/bin/xcode_backend.sh" prepare'
```

`settingsTarget: Runner` を省略すると、`FLUTTER_ROOT` 等のビルド設定が preAction に渡らず失敗しやすい。各 Flavor（または default）の scheme は、このテンプレートを参照する。

## ephemeral と xcodegen の順序

1. `flutter pub get`
2. `flutter build ios --config-only`（Flavor ありなら `--flavor <name>`）で  
   `Flutter/ephemeral/Packages/FlutterGeneratedPluginSwiftPackage/Package.swift` を生成する
3. `ios/` で `xcodegen` を実行する

`postGenCommand.sh` は `Package.swift` の存在を検証し、無い場合は失敗する。クリーン後や CI 初回で ephemeral が無いときは、手順 2 を先にやり直す。

## Pods なし workspace

`postGenCommand.sh` は `Runner.xcodeproj` のみを含む workspace を `xcodegen/Runner.xcworkspace/contents.xcworkspacedata` からコピーする。`Pods.xcodeproj` を workspace に足さない。

## Flutter 自動マイグレーションに頼らない

Flutter CLI は `project.pbxproj` / `.xcscheme` を直接書き換えることがある。XcodeGen 利用時は次回の `xcodegen` で上書きされるため、**SPM・preAction・依存は必ず `project.yml` / `xcodegen/*.yml` に書く**。

## CocoaPods からの移行（削除リスト）

次は **追加しない**。既存にあれば **削除する**。

* `Podfile` / `Podfile.lock` / `Pods/`
* `Pods_Runner.framework` 依存
* `[CP] Check Pods Manifest.lock` Build Phase およびそのスクリプト
* CocoaPods 用の `post_install` や `pod install` を前提にした postGen

`Flutter/Debug.xcconfig` 等に残る `#include? "Pods/..."` は optional include なので、ファイルが無くてもビルドできる。再導入はしない。残してもよいが、Pods を復活させる合図にはしない。
