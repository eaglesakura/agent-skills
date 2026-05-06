---
name: flutter.layered-architecture.screen-navigation
description: Flutter-Layered-Architecture アプリの画面遷移設計能力を得るSKILL。コード調査についても、アーキテクチャを知ることで精度を高めることができる。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# Flutter-Layered-Architecture / ナビゲーション

* レイヤードアーキテクチャの `screen層` では、画面間が疎結合になるように設計・実装される
* Dependency Injectionを活用し、画面遷移ライブラリを隠蔽したうえで画面遷移を実装する

## 依存する重要なライブラリ

* [go_router](https://pub.dev/packages/go_router)
  * 推奨されるルーティングライブラリ

### 画面間の分離

* 各画面同士の循環参照を避けるため、 `screen_navigation` に画面遷移の引数（Request）と戻り値（Result）を集約する
* 各画面（スクリーン層のpackage）は `{画面名}Factory` インターフェースの実装を提供し、DIを行うことで画面のpackageを疎結合とする
* Flutter標準の `Navigator` の直接利用を避けることで、ナビゲーションライブラリ自体への依存を最小限とする

## ドキュメント

下記のドキュメントを追加ロードする.
ドキュメント記載の内容を遵守し、ユーザーの指示と統合して出力を行う.

* [navigation](./references/navigation.md)
