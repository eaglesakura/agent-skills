# ViewModel レイヤー / 基本設計

## 概要

本ドキュメントは、ViewModel レイヤーの**基本設計事項**を定義する。
1 画面 1 ViewModel のスコープ、Riverpod の役割、状態・Entity・イベントの公開方法、ライフサイクル、ファイルレイアウトを定め、実装の一貫性を保つために参照する。
責務（状態管理・ビジネスロジック統合・UI状態提供・イベント通知）と構成（ViewModel, ScreenState, ScreenEntity, ScreenEvent, StateToEntityDelegate, Usecase/Delegate）は本ドキュメントの基本設計・ファイルレイアウトおよび [mvvm-viewmodel-state.md](./mvvm-viewmodel-state.md)・[mvvm-viewmodel-entity.md](./mvvm-viewmodel-entity.md)・[mvvm-viewmodel-event.md](./mvvm-viewmodel-event.md)・[mvvm-viewmodel-usecase.md](./mvvm-viewmodel-usecase.md) を参照する。

## 基本設計

* **1画面 = 1ViewModel**: 1 画面につき 1 つの専用設計された ViewModel を持つことを基本とする。適切にスコープを切り出し、互いに素であるならば柔軟に対応する（タブの親子構造など）。
* **internal 属性**: ViewModel クラスは `@internal` を付与し、パッケージ外から直接参照されないようにする。
* **Riverpod の役割**: Riverpod への依存は、**DI によるインターフェースの解決**と**ライフサイクル解決**に限る。`@riverpod` は用いず、`static final provider = Provider.autoDispose<...>(...)` を ViewModel に定義する。
* **ViewModel.provider**: 各 ViewModel は `ViewModel.provider`（`Provider.autoDispose<ViewModel>`）を持ち、画面破棄時にインスタンスが破棄される。
* **private コンストラクタ**: ViewModel は private コンストラクタ（`ViewModel._(...)`）を持ち、インスタンスは Provider のコールバック内からのみ作成する。
* **単一ステート**: 単一ステートの原則に従い、`MutableStateStream<ScreenState> state`（または `data` など一貫した名前）で状態を管理する。詳細は [mvvm-viewmodel-state.md](./mvvm-viewmodel-state.md) に従う。
* **表示状態の公開**: 表示状態は `StateStream<ScreenEntity> get entity` で公開する。State→Entity 変換は StateToEntityDelegate に委譲する。詳細は [mvvm-viewmodel-entity.md](./mvvm-viewmodel-entity.md) に従う。
* **イベントの公開**: イベントを持つ必要がある場合は `Stream<ScreenEvent> get event` で公開する。詳細は [mvvm-viewmodel-event.md](./mvvm-viewmodel-event.md) に従う。
* **リソース解放**: `_close()` メソッドを実装し、Provider の解放コールバック（`ref.onDisposeAsync(result._close)`）で実行する。主に `MutableStateStream` の `close()` を呼ぶ。

## DI

* **Riverpod による DI を推奨する**: 外部レイヤー（Repository・Usecase・Infra など）のインターフェースは `ref.watch(...)` で取得し、ViewModel のコンストラクタに渡す。`dependencies` に依存 Provider を明記する。
* 画面固有の Delegate や同一パッケージ内の Usecase は、同一パッケージ内のため DI せず直接インスタンスを作成してよい（[mvvm-viewmodel-usecase.md](./mvvm-viewmodel-usecase.md) 参照）。

## ファイルレイアウト

### ファイルレイアウトの補足

ViewModel および関連型は、画面パッケージの `lib/src/viewmodel/` 以下に配置する。
本体・アクション・必要に応じて factory / ui を part で分割し、state / entity / delegate / usecase はサブディレクトリで整理する。

### 標準ディレクトリ構成

```text
lib/src/viewmodel/
├── {画面名}_screen_view_model.dart           # ViewModel 本体（provider, state, entity, event, _close）
├── {画面名}_screen_view_model.action.dart    # アクション処理（part）
├── delegate/                                 # StateToEntityDelegate およびアクション用 Delegate（推奨配置）
│   ├── {画面名}_screen_state_to_entity_delegate.dart
│   └── {アクション名}_delegate.dart
├── entity/
│   └── {画面名}_screen_entity.dart
├── state/
│   ├── {画面名}_screen_state.dart
│   ├── {画面名}_screen_state.modifier.dart   # 必要に応じて
│   └── {画面名}_screen_event.dart            # イベントがある場合
├── usecase/                                  # 画面固有 Usecase（Optional）
│   └── {ユースケース名}_usecase.dart
└── model/                                    # 画面固有の型（Optional）
    └── {型名}.dart
```

画面によっては、ViewModel を factory / ui に分割する場合がある。

* **factory**: 初期状態の構築や Provider の依存解決を分離した part ファイル（例: `settings_screen_view_model.factory.dart`）。
* **ui**: Entity 変換など UI 用の変換メソッドを分離した part ファイル（例: `settings_screen_view_model.ui.dart`）。

### ファイルレイアウトの実装例（ワークスペース）

#### シンプルな構成（school_grade）

StateToEntityDelegate は `delegate/` への配置を推奨する（[mvvm-viewmodel-entity.md](./mvvm-viewmodel-entity.md) 参照）。以下はワークスペースの一例であり、StateToEntityDelegate が `usecase/` に配置されている場合もある。

```text
app_packages/screen/feature/school_grade/lib/src/viewmodel/
├── school_grade_screen_view_model.dart
├── school_grade_screen_view_model.action.dart
├── entity/
│   ├── school_grade_screen_entity.dart
│   └── school_grade_screen_section.dart
├── state/
│   ├── school_grade_screen_state.dart
│   └── school_grade_screen_state.modifier.dart
├── usecase/
│   ├── school_grade_screen_state_to_entity_delegate.dart
│   ├── school_grade_sort_load_usecase.dart
│   └── school_grade_sort_save_usecase.dart
└── model/
    └── school_grade_sort_type.dart
```

#### factory / ui 分割あり（settings2）

```text
app_packages/screen/feature/settings2/lib/src/viewmodel/
├── settings_screen_view_model.dart
├── settings_screen_view_model.factory.dart
├── settings_screen_view_model.ui.dart
├── entity/
│   ├── settings_screen_entity.dart
│   ├── account_group_entity.dart
│   ├── ai_quota_entity.dart
│   └── debug_group_entity.dart
├── state/
│   ├── settings_screen_state.dart
│   ├── settings_screen_state.modifier.dart
│   ├── settings_screen_event.dart
│   ├── ai_quota_state.dart
│   └── debug_setting_state.dart
└── usecase/
    └── settings_sync_usecase.dart
```

### 実装例（ViewModel 本体の骨格）

```dart
/// 学年ごとの習う漢字画面のViewModel.
@internal
final class SchoolGradeScreenViewModel {
  static final provider = Provider.autoDispose<SchoolGradeScreenViewModel>(
    (ref) {
      final kanjiListBySchoolGradeUsecase = ref.watch(
        KanjiListBySchoolGradeUsecase.provider,
      );
      const schoolGradeSectionSortDelegate =
          SchoolGradeScreenStateToEntityDelegate();
      final result = SchoolGradeScreenViewModel._(
        state: MutableStateStream(
          SchoolGradeScreenState.loading(
            context: FutureContext(tag: "$SchoolGradeScreenViewModel.initial"),
          ),
        ),
        kanjiListBySchoolGradeUsecase: kanjiListBySchoolGradeUsecase,
        schoolGradeScreenStateToEntityDelegate: schoolGradeSectionSortDelegate,
      );
      ref.onDisposeAsync(result._close);
      return result;
    },
    dependencies: [KanjiListBySchoolGradeUsecase.provider],
  );

  @visibleForTesting
  final MutableStateStream<SchoolGradeScreenState> state;

  @visibleForTesting
  final KanjiListBySchoolGradeUsecase kanjiListBySchoolGradeUsecase;

  @visibleForTesting
  final SchoolGradeScreenStateToEntityDelegate
      schoolGradeScreenStateToEntityDelegate;

  const SchoolGradeScreenViewModel._({
    required this.state,
    required this.kanjiListBySchoolGradeUsecase,
    required this.schoolGradeScreenStateToEntityDelegate,
  });

  /// Delegate の public メソッドは execute（[delegate-pattern](../../flutter.coding-rules/references/delegate-pattern.md) に従う）.
  StateStream<SchoolGradeScreenEntity> get entity =>
      state.map(schoolGradeScreenStateToEntityDelegate.execute);

  Future<void> _close() async => state.close();
}
```

## 関連文書

* [mvvm-viewmodel-state.md](./mvvm-viewmodel-state.md): ScreenState の型・単一ステート・初期状態
* [mvvm-viewmodel-entity.md](./mvvm-viewmodel-entity.md): ScreenEntity と StateToEntityDelegate
* [mvvm-viewmodel-event.md](./mvvm-viewmodel-event.md): ScreenEvent と event ストリーム
* [mvvm-viewmodel-usecase.md](./mvvm-viewmodel-usecase.md): 画面固有 Usecase

## よくあるパターンとアンチパターン

### 推奨されるパターン

* 1 画面 1 ViewModel を守り、スコープが重ならないようにする。タブなどで親子がある場合は、それぞれ専用 ViewModel を用意するか、スコープを明示する。
* `ref.onDisposeAsync(result._close)` で必ず解放コールバックを登録する。
* 外部依存は `ref.watch` で取得し、`dependencies` に列挙する。画面内の Delegate は const または通常コンストラクタで直接生成してよい。
* 状態のプロパティ名は `state` または `data` のいずれかに統一する（パッケージ内で一貫させる）。

### 避けるべきパターン

* ViewModel をパッケージ外に公開する。`@internal` を付与する。
* Provider を介さずに ViewModel を new する。インスタンスは Provider のコールバック内でのみ作成する。
* `_close()` を登録せずに `MutableStateStream` などリソースを保持したままにすること。メモリリークの原因となる。
* 複数画面で 1 つの ViewModel を共有する。スコープが「1 画面」と明確でない設計は避ける。
