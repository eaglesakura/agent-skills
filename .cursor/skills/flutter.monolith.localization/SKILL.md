---
name: flutter.monolith.localization
description: CSVファイルを使用した文字列の外部リソース化・L10n対応と、利用方法について得るためのSKILL
license: MIT License
metadata:
  author: "@eaglesakura"
---
# monolith / L10n対応

* Flutterアプリ開発で、ローカライゼーションや文字列の外部リソース化を行う場合はこのSKILLを適用する

## 基本的なデータレイアウト

* 各packageごとに、次のようなファイルを用意する

```text
path/to/package
├── lib
│   ├── domain_school.dart
│   ├── gen
│   │   └── strings.dart # monolith: 自動生成される
│   └── src
│       └── strings.dart # 各packageごとに必要に応じて作成する
├── pubspec.yaml
├── res
│   └── strings.csv      # 各packageごとに必要に応じて作成する
└── test
```

## 基本的な実行コマンド

```bash
# localization関連ファイルを生成する
dart run monolith_runner:localization
```

## 依存する主なライブラリ

* [monolith](https://pub.dev/packages/monolith)
  * dart workspaceを用いている場合は、ルートのpackageの `dev_dependencies` に追加する
  * 個別のpackageでは不要
* [monolith_localization](https://pub.dev/packages/monolith_localization)
  * dart workspaceを用いている場合は、ルートのpackageの `dev_dependencies` に追加する
  * 個別のpackageでは不要
* [monolith_localization_runtime](https://pub.dev/packages/monolith_localization_runtime)
  * 個別のpackageに必要

## Unit Test / Widget Preview / Golden Test 用 StringsTestHelper

Unit Test・Widget Preview・Golden Test では、生成された ARB をファイル I/O なしで注入できる。

### monolith.yaml の設定

`localization.test_helper` は省略可能である。省略時はヘルパーを生成しない。

```yaml
localization:
  languages:
    - ja
  # ...
  # optional, default: omit
  test_helper:
    package_name: foundation_resources          # required: 出力先パッケージ
    test_helper_class_name: StringsTestHelper   # optional, default: StringsTestHelper
    test_helper_path: lib/gen/strings_test_helper.dart  # optional, default: lib/gen/strings_test_helper.dart
```

### 出力

`dart run monolith_runner:localization` 実行時、ARB 生成後に次が出力される。

```text
${package_name}/${test_helper_path}
# 例: foundation_resources/lib/gen/strings_test_helper.dart
```

* 言語コードごとに `static String get ${lang}` が生成される（例: `StringsTestHelper.ja`）
* ARB 本文は Base64 埋め込みであり、getter 内で decode する
* リリースモード（`dart.vm.product`）では getter 呼び出し時に `UnsupportedError` を投げる

### 利用例

Widget Preview や Golden Test では、`LocalizeStringDelegate.injectDelegateForTest` に `StringsTestHelper` の getter を渡すことで、本番相当の文言注入状態を再現できる。

```dart
// view_designkit, widget_preview_functions.dart
LocalizeStringDelegate.injectDelegateForTest(
  arbJson: StringsTestHelper.ja,
);
```

```dart
// testing_golden, golden_localization.dart
Future<void> injectGoldenTestLocalization() async {
  return LocalizeStringDelegate.injectDelegateForTest(
    arbJson: StringsTestHelper.ja,
  );
}
```

```dart
// Unit Test 例
setUpAll(() async {
  await LocalizeStringDelegate.injectDelegateForTest(
    arbJson: StringsTestHelper.ja,
  );
});

tearDownAll(() async {
  await LocalizeStringDelegate.resetDelegateForTest();
});
```

* 利用側パッケージは、生成先パッケージ（例: `foundation_resources`）と `monolith_localization_runtime` に依存する
* 生成ファイルは `export` せず、`package:foundation_resources/gen/strings_test_helper.dart` を直接 import する

## 追加ドキュメント

実装の詳細について、下記のドキュメントをロードする

* [localization](./references/localization.md)

## 主な遵守事項

* [ ] リソース定義は `res/strings.csv` に配置し、ヘッダー `id,{言語コード},description` を遵守する
* [ ] `strings.csv` を変更・追加した場合は、 `dart run monolith_runner:localization` を実行してコード生成を行う
* [ ] 文字列リソースへのアクセスは `lib/src/strings.dart` を作成し、生成された `L10nStringsMixin` を使用する
* [ ] `strings.dart` は `export` せず、パッケージ内部 (`@internal`) で完結させる
* [ ] 他パッケージのリソースが必要な場合は、該当パッケージの `L10nStringsMixin` を必要な数だけmixinして対応する
* [ ] Unit Test / Widget Preview / Golden Test で文言が必要な場合は、`StringsTestHelper` + `LocalizeStringDelegate.injectDelegateForTest` を使用する
* [ ] `StringsTestHelper` をリリースビルドから呼び出さない（リリースモードでは例外となる）
