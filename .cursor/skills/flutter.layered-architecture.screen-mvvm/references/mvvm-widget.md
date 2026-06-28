# View レイヤー / Widget 実装

## 概要

本ドキュメントは、MVVM における **View（Widget）層の実装方針** を定義する。
画面のルート Widget（`*Screen`）が ViewModel のライフサイクルとイベント購読を担い、見た目の構築は `*ScreenImpl` 以下に分離する。子 Widget は Entity のみを watch し、ユーザー操作時に `ref.read()` で依存を取得する。

Riverpod の利用原則（`ref.watch` / `ref.read`、`ScreenProviders`、sealed Entity の分割など）は View レイヤーの Widget 設計ドキュメントを参照する。

## 基本設計

| # | ルール | 理由 |
| - | -- | -- |
| 1 | 画面のルート Widget は `{画面名}Screen` とし、**public** とする | 画面 Factory やナビゲーションからの入口を明確にする |
| 2 | `{画面名}Screen` で `ref.watch(ViewModel.provider)` し、ViewModel の初期化・ライフサイクル管理を行う | Provider による DI と autoDispose のスコープを画面ルートに集約する |
| 3 | 非同期初期化が必要なときは `{画面名}Screen` の `useEffect()` で `viewModel.onInitialize()` を呼ぶ | 初期化タイミングをルートに限定する |
| 4 | イベント購読が必要なときは `{画面名}Screen` の `useEffect()` または `useEventStream()` 等で開始する | ワンショットイベントの処理をルートに集約する |
| 5 | ルートレベルは初期化と購読のみとし、見た目の構築は `{画面名}ScreenImpl` に分離する | 責務分離と Golden Test のしやすさ |
| 6 | `{画面名}ScreenImpl` 配下では **Entity のみ** を watch する | UI を表示状態（Entity）への純粋な関数として保つ |
| 7 | タップ等のハンドリングでは `onTap()` コールバック内で `ref.read()` して依存を取得する | build 時に ViewModel を watch せず、見た目テスト（Golden Test）を容易にする |

## 構成コンポーネント

### `{画面名}Screen`（ルート Widget）

* **継承**: `HookConsumerWidget`
* **可視性**: **public**（`@internal` を付与しない）
* **配置**: `lib/src/view/{画面名}_screen.dart`
* **責務**:
  * `ref.watch({画面名}ScreenViewModel.provider)` による ViewModel の生成・保持
  * 必要に応じた `useEffect()` による `onInitialize()` 呼び出し
  * `useEventStream()` 等による `event` ストリームの購読とハンドリング
  * `const {画面名}ScreenImpl()` の返却

```dart
// screen_feature_settings2, settings_screen.dart
class SettingsScreen extends HookConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final viewModel = ref.watch(SettingsScreenViewModel.provider);

    useEventStream(() => viewModel.event, (event) async {
      await _onEvent(context, ref, event);
    });

    return const SettingsScreenImpl();
  }
}
```

```dart
// screen_feature_kanji_kanamajiri, kanji_kanamajiri_screen.dart
class KanjiKanamajiriScreen extends HookConsumerWidget {
  const KanjiKanamajiriScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final viewModel = ref.watch(KanjiKanamajiriScreenViewModel.provider);

    useEffect(() {
      viewModel.onInitialize();
      return null;
    }, [viewModel]);

    useEventStream(() => viewModel.event, (event) async {
      await _onEvent(context, ref, event);
    });

    return const KanjiKanamajiriScreenImpl();
  }
}
```

### `{画面名}ScreenImpl`（UI 実装 Widget）

* **継承**: `StatelessWidget` または `HookConsumerWidget`（子 Widget へ Entity を渡す場合）
* **可視性**: `@internal`
* **配置**: `lib/src/view/{画面名}_screen_impl.dart`（1クラス1ファイル）
* **責務**: Scaffold 等の画面骨格と、Body 等の子 Widget への委譲。**ViewModel を watch しない。**

```dart
// screen_feature_settings2, settings_screen_impl.dart
@internal
class SettingsScreenImpl extends StatelessWidget {
  const SettingsScreenImpl({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(strings.foundation_resources_settings),
      ),
      body: const AppSettingsBody(),
    );
  }
}
```

### `{画面名}ScreenProviders`（Entity 公開）

* ViewModel の `entity` を `StateStreamProvider` 経由で公開する。
* `{画面名}ScreenImpl` 配下の Widget は、原則として `{画面名}ScreenProviders.entity` のみを `ref.watch` する。

```dart
// screen_feature_settings2, settings_screen_providers.dart
@internal
class SettingsScreenProviders {
  static final entity = StateStreamProvider.autoDispose.stateBy(
    SettingsScreenViewModel.provider,
    (viewModel) => viewModel.entity,
  );

  const SettingsScreenProviders._();
}
```

### 子 Widget（Body / Section 等）

* **配置**: `lib/src/view/body/` 等
* **責務**: Entity を watch して UI を構築する。ユーザー操作はコールバック内で `ref.read()` する。

```dart
// screen_feature_settings2, app_settings_body.dart
class AppSettingsBody extends HookConsumerWidget {
  const AppSettingsBody({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final entity = ref.watch(SettingsScreenProviders.entity);
    // entity に基づき UI を構築
  }
}

// タップハンドラ内で ref.read()
onPressed: (context) async {
  final viewModel = ref.read(SettingsScreenViewModel.provider);
  await viewModel.onRequestLogout();
},
```

## 処理フロー

```text
ScreenFactory
  │  const SettingsScreen()   ← public ルート
  ▼
{画面名}Screen (HookConsumerWidget)
  │  ref.watch(ViewModel.provider)     … ライフサイクル管理
  │  useEffect → onInitialize()       … 非同期初期化（必要時）
  │  useEventStream → event ハンドラ   … ワンショットイベント（必要時）
  ▼
{画面名}ScreenImpl (@internal)
  │  Scaffold 等の骨格のみ（Entity / ViewModel を watch しない）
  ▼
Body / Section 等
  │  ref.watch(ScreenProviders.entity) … 表示状態のみ監視
  │  onTap 内 ref.read(ViewModel)      … 操作時のみ依存取得
  ▼
viewModel.onXXXX()
```

## ファイルレイアウト

```text
lib/src/view/
├── {画面名}_screen.dart              # {画面名}Screen（public・ルート）
├── {画面名}_screen_impl.dart         # {画面名}ScreenImpl（@internal）
├── {画面名}_screen_providers.dart    # Entity 用 Provider 群（@internal）
└── body/
    └── {部位名}.dart                 # Entity のみ watch する子 Widget
```

## 初期化とイベント購読

### 非同期初期化（`onInitialize`）

画面表示時にデータ取得等が必要な場合、`{画面名}Screen` の `useEffect()` で一度だけ呼ぶ。

```dart
useEffect(() {
  viewModel.onInitialize();
  return null;
}, [viewModel]);
```

`onInitialize()` は ViewModel アクション設計に従う（`onXXXX()` 拡張メソッド）。

### イベント購読

Snackbar 表示・画面遷移等のワンショットイベントは、`{画面名}Screen` で購読する。`useEventStream()` の利用を推奨する。

```dart
useEventStream(() => viewModel.event, (event) async {
  await _onEvent(context, ref, event);
});
```

`useEffect()` + `stream.listen` でもよいが、購読の開始・解除をルート Widget に閉じる。

## Golden Test 向けの `ref.read()` 原則

子 Widget の `build()` では **Entity のみ** を `ref.watch` する。ViewModel や Launcher 等は `build()` 時に watch しない。

| タイミング | 操作 | 用途 |
| -- | -- | -- |
| `build()` | `ref.watch(ScreenProviders.entity)` | 表示状態の反映 |
| `onTap()` / `onPressed()` 等 | `ref.read(ViewModel.provider)` | アクション呼び出し |
| `onTap()` / `onPressed()` 等 | `ref.read(Launcher.provider)` 等 | 画面遷移・ダイアログ表示 |

これにより、Entity を固定注入した Golden Test で見た目を検証しやすくなる。操作の結合テストは Widget Test または統合テストで行う。

## よくあるパターンとアンチパターン

### 推奨されるパターン

* `{画面名}Screen` を public とし、Factory から `const {画面名}Screen()` を返す。
* ルート Widget で `ref.watch(ViewModel.provider)` する。
* 見た目は `{画面名}ScreenImpl` と子 Widget に分離する（1クラス1ファイル）。
* 子 Widget は `ScreenProviders.entity` のみ watch する。
* ユーザー操作は `onTap()` 内で `ref.read()` してから `viewModel.onXXXX()` を呼ぶ。

### 避けるべきパターン

| アンチパターン | 問題 | 正しい対応 |
| -- | -- | -- |
| `{画面名}Screen` に `@internal` を付与する | 画面入口が不明確になる | public とする |
| `{画面名}Screen` で Scaffold 等の UI を直接構築する | ルートが肥大化し、テストが困難になる | `{画面名}ScreenImpl` に分離する |
| 子 Widget の `build()` で `ref.watch(ViewModel.provider)` する | Entity 以外への依存が増え、Golden Test が困難になる | Entity のみ watch し、操作時は `ref.read()` |
| 子 Widget の `build()` で `viewModel.onXXXX()` を直接呼ぶ | build 副作用となり、再描画で意図しない呼び出しが起きうる | `onTap()` 等のコールバック内で呼ぶ |
| イベント購読を Body 等の子 Widget で行う | 購読のライフサイクルが分散する | `{画面名}Screen` で購読する |
| `initialize()` 等、`on` 接頭辞のないアクションを呼ぶ | ViewModel アクションの命名が不統一 | `onInitialize()` 等を呼ぶ |
