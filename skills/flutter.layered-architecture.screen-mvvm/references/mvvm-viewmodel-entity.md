# ViewModel レイヤー / ScreenEntity と State to Entity 変換

## 概要

ScreenEntity は、View（Screen）が直接消費する UI 表示専用の状態オブジェクトである。
ViewModel が保持する ScreenState（ビジネスロジック用の内部状態）は、View には公開せず、State→Entity 変換を経て ScreenEntity としてのみ View に提供する。
この変換は、専用の StateToEntityDelegate クラスに委譲するか、ViewModel の part ファイル内の private メソッドで行う。

## ScreenEntity

### ScreenEntity の補足

ScreenEntity は表示に必要なプロパティのみを持ち、ScreenState の内部構造やビジネス都合を View から隠蔽する。
Freezed により不変に保ち、State の型が sealed の場合は Entity も sealed で対応する場合がある。

### ScreenEntity の定義

* **名前**: `{画面名}ScreenEntity`
* **配置場所**: `lib/src/viewmodel/entity/{画面名}_screen_entity.dart`
* **特徴**:
  * Freezed Class で実装する（`abstract class` または `sealed class`）。
  * `ScreenState` から StateToEntityDelegate または ViewModel 内の変換メソッドを介して冪等に生成され、View が直接参照する。
  * 表示に必要なプロパティのみを持つ。必要に応じて `@internal` を付与する。
  * 重複・非正規化されたデータを許容する

### ScreenEntity の実装例

単一形（abstract class）の例:

```dart
// screen_feature_login2, login_screen_entity.dart
@freezed
@internal
abstract class LoginScreenEntity with _$LoginScreenEntity {
  const factory LoginScreenEntity({
    required String appName,
    required bool canClickSignInButton,
    required bool canClickSkipButton,
    required bool canClickEulaButton,
    required bool eulaAgreed,
  }) = _LoginScreenEntity;

  const LoginScreenEntity._();
}
```

状態が分岐する場合（sealed class）の例:

```dart
// screen_feature_eula, eula_screen_entity.dart
@internal
@freezed
sealed class EulaScreenEntity with _$EulaScreenEntity {
  const factory EulaScreenEntity.loading() = EulaScreenEntityLoading;
  const factory EulaScreenEntity.loaded({required String text}) = EulaScreenEntityLoaded;
  const factory EulaScreenEntity.error({required String message}) = EulaScreenEntityError;
  const EulaScreenEntity._();
}
```

## State→Entity 変換

**SKILL として、Delegate パターンによる分割（StateToEntityDelegate）を推奨する。** 配置は `delegate/` とする。

StateToEntityDelegate は、ScreenState を ScreenEntity に変換する責務のみを持つ。
ViewModel の外に切り出すことで、ViewModel の肥大化を防ぎ、変換ロジックを単体テストしやすくする。
副作用を持たない純粋な変換にし、画面固有のため同一パッケージ内では DI せずに直接インスタンスを生成する。

### StateToEntityDelegate の配置

* **配置場所**: `lib/src/viewmodel/delegate/`
* **特徴**: Delegate のベストプラクティスに従う。

### StateToEntityDelegate の実装例

シンプルな変換の例:

```dart
// screen_feature_kanji_kanamajiri, usecase/screen_state_to_entity_delegate.dart
/// 漢字仮名交じり文変換画面の State を Entity に変換する Delegate.
@internal
class ScreenStateToEntityDelegate {
  const ScreenStateToEntityDelegate();

  /// [state] を [KanjiKanamajiriScreenEntity] に変換する.
  KanjiKanamajiriScreenEntity execute(
    KanjiKanamajiriScreenState state,
  ) {
    return KanjiKanamajiriScreenEntity(
      resultSection: _buildResultSection(state),
      inputSection: _buildInputSection(state),
      userActionSection: _buildUserActionSection(state),
    );
  }
  // ...
}
```

複雑な変換（中間データ構造 TemporaryState を用いる）の例:

```dart
// screen_feature_school_grade, usecase/school_grade_screen_state_to_entity_delegate.dart
@internal
class SchoolGradeScreenStateToEntityDelegate {
  const SchoolGradeScreenStateToEntityDelegate();

  SchoolGradeScreenEntity execute(SchoolGradeScreenState state) {
    return switch (state) {
      SchoolGradeScreenStateLoading() =>
        const .loading(),
      SchoolGradeScreenStateLoaded loaded => _buildEntity(loaded),
    };
  }

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
  // ... TemporaryState を用いた段階的な変換 ...
}
```

## ViewModel からの Entity 公開

ViewModel は、View に生の ScreenState を公開せず、必ず ScreenEntity のストリームを提供する。

* **Entity の公開**: `StateStream<ScreenEntity> get entity => state.map(stateToEntityDelegate.execute);`

例:

```dart
// screen_feature_kanji_kanamajiri, kanji_kanamajiri_screen_view_model.dart
StateStream<KanjiKanamajiriScreenEntity> get entity =>
    state.map(stateToEntityDelegate.execute);
```

## ディレクトリ構成

```text
lib/src/viewmodel/
├── entity/
│   └── {画面名}_screen_entity.dart      # ScreenEntity
└── delegate/
    └── {画面名}_screen_state_to_entity_delegate.dart   # StateToEntityDelegate（任意）
```

## よくあるパターンとアンチパターン

### 推奨されるパターン

1. **View には必ず ScreenEntity を渡す**
   * ScreenState を View に直接公開しない。Entity に変換してから渡す。

2. **変換が複雑な場合は StateToEntityDelegate に切り出す**
   * ソート・フィルタ・中間データ構造を伴う変換は、Delegate クラスにまとめ、`execute` で一括してテストできるようにする。

3. **中間データ構造（TemporaryState）を用いた段階的変換**
   * ScreenState → TemporaryState → 並び替え/加工 → ScreenEntity のパイプラインにすると、各段階が明確になりデバッグやテストが容易になる。

4. **const コンストラクタの StateToEntityDelegate**
   * 副作用を持たない変換のため、Delegate は `const` コンストラクタで生成する。

### 避けるべきパターン

1. **ScreenState を View に直接公開する**
   * View にはビジネスロジック用の内部状態を露出させず、必ず ScreenEntity を介する。

2. **ViewModel に長大な変換ロジックを直接書く**
   * 1〜2 行でも、変換は肥大化しやすいため、Delegate または part 内の専用メソッドに分離する。

3. **Extension の private メソッドで State→Entity 変換する（非推奨）**
   * Extension の private メソッドは単体テストしづらく、ViewModel と密結合になりやすい。StateToEntityDelegate クラスまたは ViewModel の part 内メソッドを使う。
