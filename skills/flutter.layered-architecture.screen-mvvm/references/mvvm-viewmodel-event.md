# ViewModel レイヤー / Eventパターン

## 概要

Eventパターンは、ViewModelからView（または任意のWidget）へ「ワンショットのイベント」を伝えるための仕組みである。
状態（State）に `event` プロパティを設け、**nothing → 指定バリアント（イベント）→ nothing** という一過性の変化として表現することで、画面遷移・Snackbar表示・BuildContextを要する処理などをViewModelから安全にトリガーできる。
設計者は「いつEventを使うか」「State/ViewModel/Viewの役割」を把握し、一貫した実装方針を取るために本ドキュメントを参照する。

## 構成と役割

* **ScreenState**: `event` プロパティで `ScreenEvent` 型を保持する。通常は `.nothing()` であり、イベント発火時のみ一時的に別バリアントになる。
* **ScreenEvent**: freezed の sealed class で定義し、必ず `.nothing` バリアントを持つ。その他のバリアントが「発火したいイベント」に対応する。
* **ViewModel**: `Stream<{画面}ScreenEvent> event` を公開し、State の `event` の変化を `distinct()` でストリームとして流す。
* **View（任意Widget）**: `useEffect()` で `viewModel.event` を購読し、イベントに応じて画面遷移・Snackbar・ダイアログなどを行う。

## いつ使うべきか

ViewModelから**外部にイベントを伝えたい場合**に Event パターンを用いる。

* **画面遷移**: ログイン成功後に前画面へ戻す、保存完了後に一覧へ戻すなど。
* **Snackbar / トースト**: 保存完了メッセージ、エラー通知など、BuildContext が必要な表示。
* **ダイアログ / ボトムシート**: 確認ダイアログの表示タイミングを ViewModel が決め、View が実際に表示する場合。
* **その他 BuildContext 操作**: `ScaffoldMessenger`、`Navigator`、Theme など、View 層でしか実行できない処理を「いつ実行するか」を ViewModel が指示する場合。

逆に、**純粋にUIの表示内容（テキスト・表示/非表示・ローディング）だけを変えたい場合は State/Entity の更新で足りる**ため、Event は不要である。

## Event の検出の仕組み

Event は「状態の一過性の変化」として検出する。

1. 通常時: `ScreenState.event` は `ScreenEvent.nothing()`。
2. イベント発火時: ViewModel（または Delegate）が `state.copyWith(event: ScreenEvent.xxx(...))` で一度だけ emit する。
3. 直後に: 同じ state を `event: ScreenEvent.nothing()` に戻して再度 emit する。
4. View 側: `state.stream.map((s) => s.event).distinct()` により、`nothing` 以外の値が流れたタイミングだけがストリームに乗り、ハンドラが呼ばれる。

この **nothing → イベント → nothing** のサイクルにより、同じイベントを「一度だけ」検知でき、状態にイベントが残り続けることを防ぐ。

## ScreenEvent の定義

### ScreenEvent の補足

ScreenEvent は freezed の **sealed class** で定義する。必ず `.nothing()` バリアントを持ち、それ以外のバリアントが「発火したいイベント」の種類ごとに定義される。`@internal` でパッケージ外への露出を抑える場合がある。

### ScreenEvent の実装例

```dart
// screen_feature_settings2, settings_screen_event.dart
@freezed
@internal
sealed class SettingsScreenEvent with _$SettingsScreenEvent {
  /// 何もしない
  const factory SettingsScreenEvent.nothing() = SettingsScreenEventNothing;

  /// SnackBarを表示
  const factory SettingsScreenEvent.showSnackBar({
    required String message,
  }) = SettingsScreenEventShowSnackBar;
}
```

```dart
// screen_feature_login2, login_screen_event.dart
sealed class LoginScreenEvent with _$LoginScreenEvent {
  const factory LoginScreenEvent.nothing() = LoginScreenEventNothing;

  const factory LoginScreenEvent.navigateToPreviousScreen({
    required LoginScreenNavigationResult result,
  }) = LoginScreenEventNavigateToPreviousScreen;

  const LoginScreenEvent._();
}
```

## ScreenState の event プロパティ

### event プロパティの補足

ScreenState に `event` フィールドを追加し、初期値および通常時は `ScreenEvent.nothing()` にする。Freezed の `@Default(ScreenEvent.nothing())` を使うと、`copyWith` で他フィールドだけ更新する際に event を省略しても nothing のままになる。

### event プロパティの実装例

```dart
// screen_feature_settings2, settings_screen_state.dart
@freezed
class SettingsScreenState with _$SettingsScreenState {
  const factory SettingsScreenState({
    // ... 他のフィールド
    @Default(SettingsScreenEvent.nothing()) SettingsScreenEvent event,
  }) = _SettingsScreenState;
}
```

## イベント発火（emitEvent）

### emitEvent の補足

「指定イベントを一度 emit したあと、すぐに nothing に戻す」処理は、状態更新のたびに同じパターンになるため、**State の modifier 拡張**（`{画面名}_screen_state.modifier.dart`）に `emitEvent` として切り出す。これにより、ViewModel や Delegate から「イベントを発火する」意図が明確になり、nothing への戻し忘れを防げる。

### emitEvent の実装例

```dart
// screen_feature_settings2, settings_screen_state.modifier.dart
@internal
extension SettingsScreenStateMutableStateStreamEmitterExtensions
    on MutableStateStreamEmitter<SettingsScreenState> {
  /// イベントを発火
  Future<SettingsScreenState> emitEvent(
    SettingsScreenState state, {
    required SettingsScreenEvent event,
  }) async {
    final newState = await emit(
      state.copyWith(
        event: event,
      ),
    );

    return emit(
      newState.copyWith(
        event: const SettingsScreenEvent.nothing(),
      ),
    );
  }
}
```

```dart
// screen_feature_login2, login_screen_state.modifier.dart
@internal
extension LoginScreenDataMutableStateStreamExtensions
    on MutableStateStreamEmitter<LoginScreenState> {
  /// イベントを発火
  Future<LoginScreenState> emitEvent(
    LoginScreenState state,
    MutableStateStreamEmitter<LoginScreenState> emitter, {
    required LoginScreenEvent event,
  }) async {
    var newEvent = await emitter.emit(
      state.copyWith(
        event: event,
      ),
    );
    return emitter.emit(
      newEvent.copyWith(
        event: const LoginScreenEvent.nothing(),
      ),
    );
  }
}
```

## ViewModel の event ストリーム

### event ストリームの補足

ViewModel は `MutableStateStream<ScreenState>` を保持している。`event` プロパティでは、`state.stream` から「現在の state の event フィールド」を取り出し、`distinct()` で連続する同じ値（主に nothing）を潰す。その結果、**nothing 以外のイベントが流れたタイミングだけ**が View に届く。

### event ストリームの実装例

```dart
// screen_feature_settings2, settings_screen_view_model.dart
/// イベント通知
Stream<SettingsScreenEvent> get event =>
    data.stream.map((e) => e.event).distinct();
```

```dart
// screen_feature_login2, login_screen_view_model.dart
/// イベントストリーム
Stream<LoginScreenEvent> get event =>
    data.stream.map((e) => e.event).distinct();
```

## View でのイベント監視

### イベント監視の補足

View（Screen）では、ViewModel の `event` ストリームを購読し、イベント種別に応じて画面遷移・Snackbar・ダイアログなどを行う。**useEffect()** 内で `viewModel.event.listen(...)` を呼び、クリーンアップで `subscription.cancel` を返す形で、dispose 時に購読を解除する。

### イベント監視の実装例

```dart
// 一般的なパターン: useEffect で event を購読する
@override
Widget build(BuildContext context, WidgetRef ref) {
  final viewModel = ref.watch(SettingsScreenViewModel.provider);

  useEffect(() {
    final subscription = viewModel.event.listen((event) {
      _onEvent(context, viewModel, event);
    });
    return subscription.cancel;
  }, [viewModel]);

  return Scaffold(
    // ...
  );
}

Future<void> _onEvent(
  BuildContext context,
  SettingsScreenViewModel viewModel,
  SettingsScreenEvent event,
) async {
  switch (event) {
    case SettingsScreenEventNothing():
      break;
    case SettingsScreenEventShowSnackBar():
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(event.message),
        ),
      );
      break;
  }
}
```

## アクションからのイベント発火

### アクションからの発火の補足

ViewModel のアクション（または Delegate）内で、状態更新の一環としてイベントを発火する。`updateWithLock` で emitter を取得し、State 用の `emitEvent` 拡張を呼ぶ。Delegate から発火する場合は、同じく `emitter.emitEvent(...)` を使用する。

### アクションからの発火の実装例

```dart
// screen_feature_login2, login_screen_view_model.action.dart
Future<void> onSkipLogin() async {
  await data.updateWithLock((oldState, emitter) async {
    await emitter.emitEvent(
      oldState,
      emitter,
      event: const LoginScreenEvent.navigateToPreviousScreen(
        result: LoginScreenNavigationResult.canceled(),
      ),
    );
  });
}
```

```dart
// screen_feature_login2, sign_in_delegate.dart（抜粋）
await emitter.emitEvent(
  newState,
  emitter,
  event: LoginScreenEvent.navigateToPreviousScreen(
    result: LoginScreenNavigationResult.authenticated(
      account: authenticationResult.account,
    ),
  ),
);
```

## ディレクトリ・ファイル配置

Event を利用する画面では、次のファイルが関わる。

```text
lib/src/viewmodel/
├── {画面名}_screen_view_model.dart      # event ゲッターを定義
├── {画面名}_screen_view_model.action.dart  # 必要に応じて emitEvent を呼ぶ
├── state/
│   ├── {画面名}_screen_state.dart       # event フィールドを持つ
│   ├── {画面名}_screen_state.modifier.dart  # emitEvent 拡張
│   └── {画面名}_screen_event.dart       # ScreenEvent sealed class
└── delegate/                            # 必要に応じて Delegate から emitEvent
lib/src/view/
└── {画面名}_screen.dart                 # useEffect と _onEvent
```

## よくあるパターンとアンチパターン

### 推奨されるパターン

1. **イベントは nothing → バリアント → nothing の一過性に限定する**
   * 発火したら必ず modifier の `emitEvent` で nothing に戻す。状態にイベントが残ると、同じイベントが何度も検知される。

2. **emitEvent は State の modifier に集約する**
   * 各画面の `*_screen_state.modifier.dart` に `emitEvent` を定義し、ViewModel/Delegate はそこだけを呼ぶ。戻し忘れや emit 順序のばらつきを防げる。

3. **ScreenEvent は sealed class で .nothing を必ず持つ**
   * freezed の sealed class で定義し、`.nothing()` を必ず含める。switch で網羅性チェックが効き、View 側のハンドリングが明確になる。

4. **View では useEffect で event を購読する**
   * `viewModel.event.listen(...)` で購読し、useEffect の戻り値で `subscription.cancel` を返して dispose 時に解除する。BuildContext が必要な処理はすべて `_onEvent` のようなハンドラにまとめる。

### 避けるべきパターン

1. **イベントを State に残したままにしない**
   * 発火後に `event: ScreenEvent.nothing()` へ戻さないと、`distinct()` の後でも同じイベントが再度流れたとみなされず、再発火時に検知されない、あるいは逆に同じイベントが繰り返し検知されるなどの不整合の原因になる。

2. **BuildContext を ViewModel に渡さない**
   * 画面遷移や Snackbar は View（Widget）で行い、ViewModel は「いつ・どの種類のイベントを発火するか」だけを担当する。ViewModel に context を渡すとライフサイクルやテスト性が悪化する。

3. **表示内容の切り替えに Event を使いすぎない**
   * ローディング表示・エラーメッセージの表示・リストの出し分けなど、純粋に State/Entity の値で表現できるものは State で扱い、Event は「ワンショットで View に副作用を起こしたいとき」に限定する。
