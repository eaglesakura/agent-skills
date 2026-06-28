---
name: flutter.layered-architecture.screen-mvvm
description: Flutter-Layered-ArchitectureでのScreen層のModel-View-ViewModel設計SKILL。画面を設計・開発する際に必須となる。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# Flutter / Model-View-ViewModelによる画面構築

* Flutterアプリ開発で、Model-View-ViewModelのアーキテクチャを採用する場合に、このSKILLを適用する
* Flutterアプリ開発で画面設計時には必ず必要となる

## 依存する主なライブラリ

### View / ViewModel

* [flutter_riverpod](https://pub.dev/packages/flutter_riverpod) - Provider による状態管理
* [hooks_riverpod](https://pub.dev/packages/hooks_riverpod) - HookConsumerWidget
* [flutter_hooks](https://pub.dev/packages/flutter_hooks) - useEffect 等の React-style Hooks
* [state_stream](https://pub.dev/packages/state_stream) - MutableStateStream / StateStream
* [state_stream_riverpod](https://pub.dev/packages/state_stream_riverpod) - StateStreamProvider（Riverpod連携）
* [flutter_riverpod_watch_plus](https://pub.dev/packages/flutter_riverpod_watch_plus) - ref.watchBy（Collection の Deep Equals 対応）
* [freezed](https://pub.dev/packages/freezed) - 不変データクラス（ScreenState / ScreenEntity / ScreenEvent）

### テスト

* [riverpod_container_async_test](https://pub.dev/packages/riverpod_container_async_test) - ref.testReady による ViewModel テスト
* [armyknife_dartx](https://pub.dev/packages/armyknife_dartx) - テストユーティリティ

## 追加ドキュメント

文脈に応じて、下記のドキュメントを追加ロードする.
ドキュメント記載の内容を遵守し、ユーザーの指示と統合して出力を行う.

* [mvvm-viewmodel-design](./references/mvvm-viewmodel-design.md)
  * 例: MVVMのViewModel/Modelレイヤー、ViewModel の基本設計（1画面1ViewModel、provider、ファイルレイアウト等）を行う場合
* [mvvm-viewmodel-design-action](./references/mvvm-viewmodel-design-action.md)
  * 例: ViewModel アクション（`onXXXX()`）の設計、Delegate 分離、`.action.dart` の実装を行う場合
* [mvvm-viewmodel-entity](./references/mvvm-viewmodel-entity.md)
  * 例: ScreenEntity の設計、State→Entity 変換（StateToEntityDelegate）を行う場合
* [mvvm-viewmodel-usecase](./references/mvvm-viewmodel-usecase.md)
  * 例: 画面固有のビジネスロジック（ViewModel 文脈の Usecase）の切り出し・設計を行う場合
* [mvvm-viewmodel-state](./references/mvvm-viewmodel-state.md)
  * 例: ScreenStateの型選択（abstract / sealed）、重複情報の排除、単一ステート等の設計を行う場合
  * 例: ScreenStateの設計、実装修正
* [mvvm-viewmodel-event](./references/mvvm-viewmodel-event.md)
  * 例: ViewModelからViewへワンショットイベント（画面遷移・Snackbar等）を伝える設計を行う場合
* [mvvm-view-design](./references/mvvm-view-design.md)
  * 例: MVVMのViewレイヤー、Widget実装を行う場合
  * 例: Riverpodの利用（ref.watch/read、select、watchBy、Providerスコープ等）を行う場合
  * 例: ViewModelの初期化処理を記述する場合
  * 例: Dependency Injectionの注入を行う場合
* [mvvm-widget](./references/mvvm-widget.md)
  * 例: `{画面名}Screen` / `{画面名}ScreenImpl` の分割、ルート Widget の責務、Entity の watch 方針を設計する場合
* [mvvm-viewmodel-test](./references/mvvm-viewmodel-test.md)
  * 例: ViewModelのUnitTestを行う場合
