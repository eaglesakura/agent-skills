---
name: flutter-xcodegen-ios-firebase-crashlytics
description: >-
  Flutter iOS XcodeGen 構成に Firebase Crashlytics（SPM product と dSYM アップロード Build Phase）を
  組み込む SKILL。「Crashlytics を xcodegen に」「Crashlytics Upload Symbols」「FirebaseCrashlytics product」
  では必ず使う。前提は flutter-xcodegen-ios-firebase（GoogleService-Info と firebase-ios-sdk）済み。
  Dart シンボルの別アップロード手順や Android 側は対象外。
---
# Flutter iOS / XcodeGen + Firebase Crashlytics

`flutter-xcodegen-ios-firebase` 済みの `project.yml` に、Crashlytics のリンクとシンボルアップロード Phase を足す。

## 前提

* `firebase-ios-sdk` が `packages` にある
* 各 Configuration に `GoogleService-Info.plist` があり、pre-build でバンドルへ入る
* Upload Phase の input にバンドル内 plist と dSYM が含まれる（テンプレどおり）

## 作業手順

1. [assets/project.yml.crashlytics-fragment.yml](./assets/project.yml.crashlytics-fragment.yml) を読む
2. `targets.Runner.dependencies` に `FirebaseCrashlytics` product を追加する
3. `postBuildScripts` に Crashlytics `run` スクリプトを追加する（Thin Binary の後でよい）
4. `xcodegen` を再実行する

## 注意

* `basedOnDependencyAnalysis: false` を付け、入力ファイル一覧をテンプレから落とさない
* GoogleService-Info がバンドルに無いとアップロードが失敗しやすい → firebase SKILL 側を先に直す

## 関連

* `flutter-xcodegen-ios-firebase`
* `flutter-xcodegen-ios`
