# ViewModel レイヤー / State設計

## 概要

ScreenState は、画面の状態を表す不変オブジェクトである。
ViewModel は単一の `MutableStateStream<ScreenState>` を持ち、View はその状態（または StateToEntityDelegate を介した Entity）を購読して UI を描画する。
設計者は「State に何を含め、何を含めないか」「abstract class と sealed class の使い分け」を把握し、一貫した状態設計を行うために本ドキュメントを参照する。

* **ScreenState の型**: freezed の **abstract class** または **sealed class** のいずれかを選択して使用する。
* **重複・派生情報**: 重複した情報や冪等に計算可能な情報は State に持たせない（例: リスト表示用のグルーピングヘッダをリスト要素として State に持たせない）。
* **単一ステート**: ViewModel ごとに単一ステートの原則に従い、1 画面 1 つの ScreenState 型で状態を表現する。
* **処理用インターフェース**: Repository や Usecase など、処理を行うためのインターフェースは、動的に変化しない限り State に含めず、ViewModel の依存として注入する。
* **画面固有の型**: 必要に応じて画面固有のクラス（Model, enum）を定義してよい（例: タブ識別用の enum、ソート種別の enum）。
* **プロパティはすべて required**: `@Default` は使用しない。設定ミス・設定忘れを誘発するため、nullable を含めすべてのプロパティに `required` を付ける。
* **初期状態は ViewModel の初期化時で指定する**: 初期状態を返す factory は State に持たせず、**ViewModel.provider** の内部（概ね Provider のコールバック内）で初期状態を構築する。ViewModel の定義方法は [mvvm-viewmodel-design.md](./mvvm-viewmodel-design.md) を参照する。このアーキテクチャでは `@riverpod` は非推奨である。
* **const プライベートコンストラクタ**: ScreenState には `const {型名}._();` を定義することがベストプラクティスである。

## ScreenState の型選択（abstract class / sealed class）

### 型選択の補足

ScreenState は freezed を用いて定義する際、**abstract class** と **sealed class** のどちらかを選ぶ。

* **abstract class**: 単一の「形」で、プロパティの組み合わせによって状態を表現する場合に用いる。1 つの factory コンストラクタで、すべてのプロパティを並列に持つ。ローディング・エラーなどを「プロパティの有無や値」で表現する画面に向く。
* **sealed class**: 状態が「ローディング / 読み込み完了 / エラー」のように**バリアントで明確に分岐**する場合に用いる。複数の factory（`.loading()`, `.loaded(...)`, `.error(...)`）を持ち、switch で網羅的に扱える。状態の種類が有限で分岐がはっきりしている画面に向く。

どちらを選んでも、不変・単一ステート・重複情報を持たない、という原則は共通である。

### 型選択の実装例

abstract class の例: 単一の状態形で、プロパティで表現する。

```dart
// screen_feature_settings2, settings_screen_state.dart
@freezed
@internal
abstract class SettingsScreenState with _$SettingsScreenState {
  const factory SettingsScreenState({
    /// 現在のイベント
    required SettingsScreenEvent event,

    /// 現在リンクされているアカウント.
    required PkAccount? account,

    /// デバッグ設定の状態
    required DebugSettingState debugSettingState,

    /// AIチケット表示の状態. nullは非表示を意味する.
    required AiQuotaState? aiQuotaState,
  }) = _SettingsScreenState;

  const SettingsScreenState._();
}
```

初期状態は ViewModel の初期化時（概ね Provider の内部）で構築する。State に `.initial()` のような factory は持たせない。

sealed class の例: ローディング / 読み込み完了 / エラーをバリアントで分岐する。

```dart
// screen_feature_school_grade, school_grade_screen_state.dart
@internal
@freezed
sealed class SchoolGradeScreenState with _$SchoolGradeScreenState {
  /// データ読み込み完了.
  const factory SchoolGradeScreenState.loaded({
    required FutureContext context,
    required List<KanjiEntry> grade1Entries,
    required List<KanjiEntry> grade2Entries,
    // ... 他学年
    required SchoolGradeSortType sortType,
  }) = SchoolGradeScreenStateLoaded;

  /// データ読み込み中.
  const factory SchoolGradeScreenState.loading({
    required FutureContext context,
  }) = SchoolGradeScreenStateLoading;

  const SchoolGradeScreenState._();
}
```

```dart
// screen_feature_eula, eula_screen_state.dart
@internal
@freezed
sealed class EulaScreenState with _$EulaScreenState {
  const factory EulaScreenState.error({
    required FutureContext context,
    required String message,
  }) = EulaScreenStateError;

  const factory EulaScreenState.loaded({
    required FutureContext context,
    required EndUserLicenseAgreementVersion eulaVersion,
    required EndUserLicenseAgreementBody eulaBody,
  }) = EulaScreenStateLoaded;

  const factory EulaScreenState.loading({
    required FutureContext context,
  }) = EulaScreenStateLoading;

  const EulaScreenState._();
}
```

## 重複・冪等に計算可能な情報を State に持たせない

### 重複情報の補足

State には、**重複した情報**や**冪等に計算できる情報**を持たせない。
例えば「リストを表示するときにグルーピング用のヘッダを挟んだリスト」が必要な場合、State のリストにヘッダ用の要素を混ぜて持つのではなく、State には「元データ（学年ごとのリストなど）」だけを持ち、**表示用の整形（グルーピング・ソート・ヘッダ付きリストの生成）は StateToEntityDelegate で行う**。
これにより、State は単一の情報源（Single Source of Truth）となり、同じデータから複数の表示形を一貫して導出できる。

### 重複情報の実装例

State には生データ（学年ごとのエントリとソート種別）のみを持ち、セクション・ヘッダ・ソート済みリストは Delegate で Entity に変換する。

```dart
// screen_feature_school_grade, school_grade_screen_state.dart（抜粋）
sealed class SchoolGradeScreenState with _$SchoolGradeScreenState {
  const factory SchoolGradeScreenState.loaded({
    required List<KanjiEntry> grade1Entries,
    // ...
    required List<KanjiEntry> grade6Entries,
    required SchoolGradeSortType sortType,
  }) = SchoolGradeScreenStateLoaded;
  // ...
}
```

```dart
// screen_feature_school_grade, school_grade_screen_state_to_entity_delegate.dart（抜粋）
/// ScreenStateからTemporaryStateのリストを生成し、ソート後にセクション（ヘッダ+entries）を組み立ててEntityを返す.
SchoolGradeScreenEntity _buildEntity(SchoolGradeScreenStateLoaded loaded) {
  final temporaryStates = _buildTemporaryStates(loaded);
  final sortedTemporaryStates = _sortTemporaryStates(
    sortType: loaded.sortType,
    temporaryStates: temporaryStates,
  );
  return _buildEntityFromTemporaryStates(
    sortedTemporaryStates: sortedTemporaryStates,
    sortType: loaded.sortType,
  );
}
```

アンチパターン: State のリストに「ヘッダ用のダミー要素」や「表示順に並べ替えたリスト」を直接持たせる。これらは State と重複・派生関係になり、更新漏れや不整合の原因になる。

## ViewModel ごとの単一ステート

### 単一ステートの補足

1 つの ViewModel が扱う状態は、**1 つの ScreenState 型に集約する**。
ViewModel は `MutableStateStream<ScreenState>` を 1 つだけ持ち、すべての状態変化はその Stream への emit で表現する。複数の独立した Stream で画面状態を分離しない。これにより、状態の遷移が追いやすく、テストやデバッグも容易になる。

### 単一ステートの実装例

ViewModel は 1 つの `data: MutableStateStream<ScreenState>` のみを持つ。初期状態は **ViewModel.provider** の内部で明示的に構築する。このアーキテクチャでは `@riverpod` は非推奨であり、`ViewModel.provider`（`Provider.autoDispose`）を用いる。ViewModel の定義・provider の書き方の詳細は [mvvm-viewmodel-design.md](./mvvm-viewmodel-design.md) を参照する。

```dart
// 典型的な ViewModel のイメージ（ViewModel.provider の内部で初期状態を構築）
// screen_feature_settings2, settings_screen_view_model.dart のパターンに準拠
final class SettingsScreenViewModel {
  static final provider = Provider.autoDispose<SettingsScreenViewModel>(
    (ref) {
      // 依存の取得
      final authenticationRepository = ref.watch(
        AuthenticationRepository.provider,
      );
      // 初期状態は Provider のコールバック内で明示的に構築する（State に .initial() は持たせない）
      final stateStream = MutableStateStream<SettingsScreenState>(
        SettingsScreenState(
          event: const SettingsScreenEvent.nothing(),
          account: null,
          debugSettingState: DebugSettingState(
            enabled: !kReleaseMode,
            showClearTutorialFlags: true,
          ),
          aiQuotaState: null,
        ),
      );

      final result = SettingsScreenViewModel._(data: stateStream, ...);
      ref.onDisposeAsync(result._close);
      return result;
    },
    dependencies: [AuthenticationRepository.provider, ...],
  );

  final MutableStateStream<SettingsScreenState> data;

  const SettingsScreenViewModel._({required this.data, ...});
}
```

## Repository / Usecase を State に含めない

### 処理用インターフェースの補足

Repository や Usecase など、**処理を行うためのインターフェース（依存）**は、実行時に動的に切り替えない限り、State のプロパティに含めない。
これらは ViewModel のコンストラクタや Provider の ref 経由で注入し、ViewModel のフィールドとして持つ。State は「画面に表示するために必要なデータ」と「イベント」に限定し、処理の入り口（どの Repository を使うか）は State の外に置く。動的に変化する場合（例: テスト用と本番用で差し替える）も、Provider のオーバーライドで対応し、State には含めない。

### 処理用インターフェースの実装例

コードベースでは、ScreenState の定義に Repository や Usecase 型のフィールドは存在しない。ViewModel がそれらを保持し、アクション時に呼び出す。

```dart
// screen_feature_settings2, settings_screen_state.dart
// account, debugSettingState, aiQuotaState, event のみ。Repository 等は含まない。全フィールド required。
abstract class SettingsScreenState with _$SettingsScreenState {
  const factory SettingsScreenState({
    required SettingsScreenEvent event,
    required PkAccount? account,
    required DebugSettingState debugSettingState,
    required AiQuotaState? aiQuotaState,
  }) = _SettingsScreenState;

  const SettingsScreenState._();
}
```

## 画面固有のクラス（Model / enum）の定義

### 画面固有型の補足

必要に応じて、**画面固有のクラス（Model, enum）**を定義してよい。
タブを識別する enum、ソート種別を表す enum、画面内でだけ使う小さな状態クラス（例: DebugSettingState, AiQuotaState）などは、その画面の state または model 配下に置く。Domain や共通レイヤーに置くほどではないが、State の可読性や型安全性を高める場合に利用する。

### 画面固有型の実装例

ソート種別を表す画面固有の enum。

```dart
// screen_feature_school_grade, school_grade_sort_type.dart
@internal
enum SchoolGradeSortType {
  gradeAscending._(prefValue: 1),
  gradeDescending._(prefValue: 2),
  ;

  final int prefValue;
  const SchoolGradeSortType._({required this.prefValue});
}
```

画面内でだけ使う状態のクラス（freezed の abstract class）。

```dart
// screen_feature_settings2, debug_setting_state.dart
@internal
@freezed
abstract class DebugSettingState with _$DebugSettingState {
  factory DebugSettingState({
    required bool enabled,
    required bool showClearTutorialFlags,
  }) = _DebugSettingState;
}
```

## ディレクトリ・ファイル配置

State および画面固有の型は、次のような配置とする。

```text
lib/src/viewmodel/
├── state/
│   ├── {画面名}_screen_state.dart       # ScreenState（abstract / sealed）
│   ├── {画面名}_screen_state.modifier.dart  # 必要に応じて（emitEvent 等）
│   ├── {画面名}_screen_event.dart       # Event を使う場合
│   └── {画面名}_xxx_state.dart          # 画面固有の状態クラス（任意）
└── model/
    └── {画面名}_xxx_type.dart           # 画面固有の enum / 型（任意）
```

## よくあるパターンとアンチパターン

### 推奨されるパターン

1. **状態の形に応じて abstract class と sealed class を使い分ける**
   * プロパティの組み合わせで表現するなら abstract class、ローディング/ loaded/ error などのバリアントで分岐するなら sealed class とする。

2. **State には重複・冪等計算可能な情報を持たせない**
   * グルーピングヘッダやソート済みリストなどは StateToEntityDelegate で State から Entity へ変換する段階で生成し、State のリスト要素として持たない。

3. **ViewModel は単一の `MutableStateStream<ScreenState>` のみ持つ**
   * 画面の状態は 1 つの ScreenState 型に集約し、すべての更新をその Stream に emit する。

4. **Repository / Usecase は ViewModel の依存として注入し、State に含めない**
   * 動的に切り替えない限り、State のフィールドにしない。ViewModel のコンストラクタや ref で保持する。

5. **画面固有の識別子やオプションは enum / Model で型付けする**
   * タブ、ソート種別、画面内のサブ状態などは、必要に応じて画面の model/ state 配下に型を定義する。

6. **全プロパティに required を付け、const プライベートコンストラクタを定義する**
   * `@Default` は使わず、nullable を含めすべて required にする。abstract / sealed いずれも `const {型名}._();` を定義する。

### 避けるべきパターン

1. **リスト表示用のヘッダを State のリスト要素として持つ**
   * ヘッダは State の生データから StateToEntityDelegate で導出する。State に「ヘッダ＋データ」を混在させると、重複と不整合の原因になる。

2. **ViewModel で複数の独立した State Stream を持つ**
   * 画面状態は 1 つの ScreenState にまとめ、単一ステートの原則に従う。

3. **Repository や Usecase を ScreenState のプロパティにする**
   * 処理の入り口は ViewModel の依存として扱い、State は「表示に必要なデータ」と「イベント」に限定する。

4. **状態の形がバリアントで明確なのに abstract class で null だらけにする**
   * ローディング/ loaded/ error のように分岐がはっきりしている場合は、sealed class でバリアントにすると switch で網羅でき、可読性が上がる。

5. **@Default でプロパティの初期値を省略する**
   * 設定ミス・設定忘れを招くため、ScreenState では `@Default` を使わず、すべて required とする。初期値は ViewModel の初期化時（概ね Provider の内部）で明示的に渡す。

6. **State に .initial() などの初期状態用 factory を定義する**
   * 初期状態は ViewModel.provider の内部で構築するのがベストプラクティスである。State は「形」だけを定義し、最初の値を誰がどう作るかは ViewModel に委ねる。

7. **@riverpod で ViewModel を提供する**
   * このアーキテクチャでは `@riverpod` は非推奨である。ViewModel は `static final provider = Provider.autoDispose<...>(...)` で提供する（[mvvm-viewmodel-design.md](./mvvm-viewmodel-design.md) 参照）。
