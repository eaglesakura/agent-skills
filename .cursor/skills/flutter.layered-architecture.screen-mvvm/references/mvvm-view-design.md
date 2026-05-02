# MVVM-Viewレイヤー / Widget設計

## 概要

View レイヤーは、ViewModel から提供される状態（Entity）に基づいて UI を構築し、ユーザーからの操作を受け付けて ViewModel に伝達する役割を持つ。
`UI=f(State)` の原則に従い、宣言的 UI として実装される。
本ドキュメントでは、View の責務・構成に加え、View および Provider まわりで **Riverpod** を利用する際の原則（const・ref.watch/read・select・Provider スコープ・sealed class entity など）をまとめる。

## 責務

* **UI の構築**: ViewModel の `entity` ストリームを監視し、画面を描画する。
* **ユーザー操作の受付**: タップや入力などのユーザー操作を検知し、ViewModel のアクションメソッドを呼び出す。
* **イベントのハンドリング**: ViewModel からのイベント（画面遷移、スナックバー表示など）を監視し、処理する。
* **ビジネスロジックを持たない**: 状態管理や複雑なロジックは ViewModel に委譲し、View は表示に専念する。

## 構成コンポーネント

### 1. Screen (`{画面名}Screen`)

実際の画面 UI を構築する Widget。`HookConsumerWidget` を継承して実装する。

* **配置場所**: `lib/src/view/{画面名}_screen.dart`
* **特徴**:
  * `ref.watch` で ViewModel を取得する。
  * `useEffect` で画面表示時の初期化処理（必要な場合）を行う。

### 2. ScreenProviders (`ScreenProviders`)

画面固有の派生プロバイダを集約したクラス。

* **配置場所**: `lib/src/view/{画面名}_screen_providers.dart`
* **特徴**:
  * ViewModel の `entity` を `StateStreamProvider.autoDispose.stateBy` で公開する。
  * 必要に応じて、Entity から特定の値を切り出した `Provider` や、sealed な状態ごとの `Provider` を定義する。
  * `@internal` でパッケージ外への公開を抑える。

#### 実装例（entity のみ）

ViewModel の entity ストリームをそのまま公開する場合。

```dart
// screen_feature_login2, login_screen_providers.dart
import "package:meta/meta.dart";
import "package:screen_feature_login2/src/viewmodel/login_screen_view_model.dart";
import "package:state_stream_riverpod/state_stream_riverpod.dart";

@internal
final class LoginScreenProviders {
  /// UiStateを取得するプロバイダー.
  static final entity = StateStreamProvider.autoDispose.stateBy(
    LoginScreenViewModel.provider,
    (vm) => vm.entity,
  );
}
```

#### 実装例（sealed class Entity の状態分割）

Entity が sealed class のとき、状態型ごとに Provider を分割すると、Widget 側で型安全に参照できる。

```dart
// screen_feature_eula, eula_screen_providers.dart
import "package:flutter_riverpod/flutter_riverpod.dart";
import "package:meta/meta.dart";
import "package:screen_feature_eula/src/viewmodel/entity/eula_screen_entity.dart";
import "package:screen_feature_eula/src/viewmodel/eula_screen_view_model.dart";
import "package:state_stream_riverpod/state_stream_riverpod.dart";

/// EULA画面のプロバイダー.
@internal
final class EulaScreenProviders {
  /// Entityストリーム.
  static final entity = StateStreamProvider.autoDispose.stateBy(
    EulaScreenViewModel.provider,
    (viewModel) => viewModel.entity,
  );

  /// Loading 状態.
  static final loading = Provider.autoDispose(
    (ref) => ref.watch(
      entity.select((e) => e as EulaScreenEntityLoading),
    ),
    dependencies: [entity],
  );

  /// Loaded 状態.
  static final loaded = Provider.autoDispose(
    (ref) => ref.watch(
      entity.select((e) => e as EulaScreenEntityLoaded),
    ),
    dependencies: [entity],
  );

  /// Error 状態.
  static final error = Provider.autoDispose(
    (ref) => ref.watch(
      entity.select((e) => e as EulaScreenEntityError),
    ),
    dependencies: [entity],
  );

  const EulaScreenProviders._();
}
```

## 実装パターン

### 基本的な実装構造

```dart
@internal
class KanjiPracticeScreen extends HookConsumerWidget {
  const KanjiPracticeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final viewModel = ref.watch(KanjiPracticeScreenViewModel.provider);

    useEffect(() {
      viewModel.onInitialize();
      return null;
    }, [viewModel]);

    useEffect(() {
      final subscription = viewModel.event.listen((event) {
        _onEvent(context, event);
      });
      return subscription.cancel;
    }, [viewModel]);

    return const SafeArea(
      child: Column(
        children: [
          Flexible(
            fit: FlexFit.tight,
            child: PassageView(),
          ),
          Padding(
            padding: EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 8,
            ),
            child: PassageInputField(),
          ),
        ],
      ),
    );
  }

  Future<void> _onEvent(
    BuildContext context,
    KanjiPracticeScreenEvent event,
  ) async {
    switch (event) {
      case KanjiPracticeScreenEventNothing():
        break;
    }
  }
}
```

### イベント監視

ViewModel から通知されるワンショットのイベント（画面遷移、エラーダイアログ、スナックバーなど）を処理するために、`useEffect` フックを使用する。
`useEffect` は dispose 時に `StreamSubscription` をキャンセルするように実装する。

```dart
useEffect(() {
  final subscription = viewModel.event.listen((event) {
    _onEvent(context, event);
  });
  return subscription.cancel;
}, [viewModel]);
```

## Widget の基本設計

View レイヤーで Widget を構築する際の基本方針である。状態管理ライブラリに依存しない、Widget そのものの設計原則とする。

### const の原則

* Widget のコンストラクタは可能な限り `const` として定義する。
* `const` Widget はリビルド時に再生成されないため、パフォーマンスが向上する。
* 子 Widget を `const` として配置することで、親のリビルドが子に伝播しない。

```dart
@internal
class KanjiPracticeScreen extends HookConsumerWidget {
  const KanjiPracticeScreen({super.key});
  // ...
}
```

```dart
children: [
  const SizedBox(height: 24),
  const LoginGuideArea(),
  const Spacer(),
  _buildSignInButtons(context),
],
```

## Riverpod の利用原則

本プロジェクトでは状態管理に **Riverpod** を採用している。View および Provider を記述する際は以下の原則に従う。

**Riverpod のコード生成（`@riverpod` や `@Riverpod(keepAlive: true)` 等）は非推奨である。** Provider はクラスの `static final` メンバーとして `Provider.autoDispose<...>(...)` を明示的に定義し、`dependencies` で依存を列挙する。

### ref.watch() と ref.read()

* **build() 内では ref.watch() を使用する**: Provider から取得する値は可能な限り `ref.watch()` とし、値の変更時に自動でリビルドされるようにする。
* **build() 外では ref.read() を使用する**: コールバック内・イベントハンドラ内など、build() 以外のタイミングでのみ `ref.read()` を使う。build() 内で `ref.read()` を使うと、状態変更時にリビルドされず UI が古いままになる。

```dart
Widget build(BuildContext context, WidgetRef ref) {
  final viewModel = ref.watch(HomeScreenViewModel.provider);
  // ...
}
```

```dart
onPageChanged: (index) {
  ref.read(KanjiPracticeScreenViewModel.provider).onPageChanged(index);
}
```

### select と watchBy

* **select で監視範囲を絞る**: 大きな状態オブジェクトから必要なプロパティのみを監視し、該当プロパティが変わったときだけリビルドする。
* **Collection の場合は ref.watchBy() を使う**: Riverpod の `select` は List/Set/Map 等を参照比較するため、内容が同じでも別インスタンスだとリビルドされる。`flutter_riverpod_watch_plus` の `ref.watchBy()` で Deep Equals 比較し、不要なリビルドを防ぐ。

```dart
final eulaAgreed = ref.watch(
  LoginScreenProviders.entity.select((value) => value.eulaAgreed),
);
```

```dart
final selectableTabs = ref.watchBy(
  HomeScreenProviders.entity,
  (vp) => vp.selectableTabs,
);
```

### Provider スコープ

* **グローバルスコープの Provider は非推奨**: トップレベルの `final` 変数として定義するグローバル Provider は使わない。依存の追跡とテスタビリティを保つため、関連クラスの `static final` メンバーとして定義する。
* **dependencies を明示する**: `Provider.autoDispose` 等では `dependencies` パラメータで依存 Provider を列挙する。

```dart
@internal
final class KanjiPracticeScreenViewModel {
  static final provider = Provider.autoDispose<KanjiPracticeScreenViewModel>(
    (ref) {
      final passageParseUsecase = ref.watch(PassageParseUsecase.provider);
      final result = KanjiPracticeScreenViewModel._(
        state: MutableStateStream(KanjiPracticeScreenState.initial()),
        passageParseUsecase: passageParseUsecase,
      );
      ref.onDisposeAsync(result._close);
      return result;
    },
    dependencies: [PassageParseUsecase.provider],
  );
  // ...
}
```

### sealed class Entity と ScreenProviders

Entity が sealed class の場合は、状態ごとに派生 Provider を分割すると型安全に扱える。

* 各状態型（Loading / Loaded / Error など）ごとに `Provider.autoDispose` を定義し、`entity.select((e) => e as EulaScreenEntityLoaded)` のようにキャストして利用する。
* これにより、特定の状態のときだけ有効な UI コンポーネントをコンパイル時に保証できる。

```dart
@internal
final class EulaScreenProviders {
  static final entity = StateStreamProvider.autoDispose.stateBy(
    EulaScreenViewModel.provider,
    (viewModel) => viewModel.entity,
  );

  static final loading = Provider.autoDispose(
    (ref) => ref.watch(entity.select((e) => e as EulaScreenEntityLoading)),
    dependencies: [entity],
  );

  static final loaded = Provider.autoDispose(
    (ref) => ref.watch(entity.select((e) => e as EulaScreenEntityLoaded)),
    dependencies: [entity],
  );

  const EulaScreenProviders._();
}
```

## テスタビリティ

* **Widget（View）のテスト**: UI の複雑さや外部依存の多さからコストが高く、必須ではない。Widget はテストしづらいことを受け入れる。
* **ViewModel / Model**: Provider で依存を注入するため、テスト時にモックを差し替えやすく、単体テストを重視する。ビジネスロジックは ViewModel・Usecase・StateModifier に分離し、Fake や Mock でテストする。

## ベストプラクティス

* **ロジックの排除**: `build` 内に複雑な条件分岐や計算ロジックを書かず、ViewModel の `entity` として事前に計算された値を使う。
* **コンポーネント分割**: 画面が複雑な場合は `body/` 配下に部品 Widget を分割する。
* **HookConsumerWidget の使用**: Riverpod と Flutter Hooks を組み合わせて、簡潔に実装する。Widget 構築には [flutter_riverpod](https://pub.dev/packages/flutter_riverpod) を推奨する。
* **const Widget の活用**: 子 Widget を可能な限り `const` で配置し、不要なリビルドを防ぐ。
* **select / watchBy の活用**: 監視する範囲を絞り、Collection は `ref.watchBy()` で Deep Equals 比較する。
* **クラススコープの Provider**: Provider は関連クラスの `static final` で定義し、`dependencies` を明示する。

## よくあるパターンとアンチパターン

### 推奨されるパターン

1. **const Widget**: Widget コンストラクタと子配置を可能な限り `const` にする。
2. **ref.watch() の優先**: build() 内では Provider の取得に `ref.watch()` を使い、状態変更を監視する。
3. **select によるスコープ限定**: 必要なプロパティのみを監視し、リビルドを最小限にする。
4. **Collection には ref.watchBy()**: List/Set/Map を監視する場合は `ref.watchBy()` で Deep Equals を行う。
5. **クラススコープの Provider**: `ExampleClass.provider` のように所有者を明確にし、`dependencies` を記述する。
6. **sealed class Entity の状態分割**: 状態ごとに Provider を分割し、型安全にアクセスする。
7. **ビジネスロジックの分離**: 複雑なロジックは ViewModel・Usecase・Delegate に寄せ、View は表示に専念する。

### 避けるべきパターン

1. **Riverpod のコード生成（@riverpod 等）**: `@riverpod` や `@Riverpod(keepAlive: true)` 等のコード生成は非推奨。`static final provider = Provider.autoDispose<...>(...)` を明示的に定義する。
2. **build() 内での ref.read()**: 状態変更時にリビルドされず、UI が古いままになる。
3. **グローバルスコープの Provider**: トップレベルの `final` Provider は依存追跡とテスタビリティを損なう。
4. **select なしの大きな状態監視**: 関係ないプロパティの変更でもリビルドが走り、パフォーマンスが落ちる。
5. **Collection の select 使用**: 参照比較のため意図しないリビルドが起きる。`ref.watchBy()` を使う。
6. **Widget 内のビジネスロジック**: 条件分岐・計算は ViewModel 側に寄せる。
7. **dependencies の省略**: 依存関係が不明確になり、テストやリファクタリングで問題になりやすい。

## 参考リンク

* [flutter_riverpod](https://pub.dev/packages/flutter_riverpod) - 状態管理
* [flutter_riverpod_watch_plus](https://pub.dev/packages/flutter_riverpod_watch_plus) - Collection の Deep Equals 対応
* [Riverpod 公式ドキュメント](https://riverpod.dev/)
