---
name: flutter.monolith.localization
description: CSVファイルを使用した文字列の外部リソース化・L10n対応と、利用方法について得るためのSKILL
license: MIT License
metadata:
  author: @eaglesakura
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

```dart
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

## 追加ドキュメント

実装の詳細について、下記のドキュメントをロードする

* [localization](./references/localization.md)

## 主な遵守事項

* [ ] リソース定義は `res/strings.csv` に配置し、ヘッダー `id,{言語コード},description` を遵守する
* [ ] `strings.csv` を変更・追加した場合は、 `dart run monolith_runner:localization` を実行してコード生成を行う
* [ ] 文字列リソースへのアクセスは `lib/src/strings.dart` を作成し、生成された `L10nStringsMixin` を使用する
* [ ] `strings.dart` は `export` せず、パッケージ内部 (`@internal`) で完結させる
* [ ] 他パッケージのリソースが必要な場合は、該当パッケージの `L10nStringsMixin` を必要な数だけmixinして対応する
