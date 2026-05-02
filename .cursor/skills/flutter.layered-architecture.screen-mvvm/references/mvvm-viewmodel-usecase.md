# ViewModel レイヤー / ViewModel文脈のUsecase

## 概要

ViewModel 文脈の **Usecase** は、**その画面固有のビジネスロジック** を担当するコンポーネントである。Usecase レイヤー（アプリ横断のユースケース）よりも **画面固有の事情を反映したもの** であり、同一画面の ViewModel からだけ利用されることを前提とする。

複雑なビジネスロジックを ViewModel から切り出し、単体テストや Delegate との組み合わせを容易にするために用いる。配置は `lib/src/viewmodel/usecase/` とする。

## Delegate や Usecase レイヤーとの違い

* **ViewModel 文脈の Usecase** は「その画面固有のビジネスロジック」であり、「Usecase レイヤーよりも画面固有の事情を反映したもの」である。アプリ横断の Usecase レイヤーとは役割が異なる。
* **すべて `@internal` が基本** である。パッケージ外に公開しない。
* **Delegate** は「メソッドの外部化」である。一方、**Usecase への切り出し** は次の目的で行う。
  * **ビジネスロジックの切り出し**: 複雑な判断・計算・フローを ViewModel から分離する。
  * **Delegate と組み合わせて Mock を用意することによる Unit Test のカバレッジ向上**: 画面固有 Usecase を差し替えることで、ViewModel や Delegate のテストがしやすくなる。
  * **Delegate 間のロジック共通化**: 複数の Delegate が参照する共通ロジックを Usecase に集約する。
* **1 クラス 1 機能** とする。単一責務を守る。
* **冪等性は問わない**。内部で `StateStream` の操作を行ってもよいし、冪等な結果を返却してもよい。画面固有の都合に合わせて設計する。
* **Internal 専用** であるため、**Provider による DI は不要** であり、**直接インスタンスを作成してよい**。ただし、**外部レイヤー（Data 層・Usecase 層・Infra 層など）のインターフェースを利用する場合** には、従来通り DI（`ref.watch` 等）を使用する。

## 責務と配置

* **責務**: 画面固有のビジネスロジック（複数 Delegate で共有するロジック、テストで切り出したい判断・計算など）を 1 クラスで担当する。
* **配置場所**: `lib/src/viewmodel/usecase/`。ファイル名は `{機能名}_usecase.dart` など、責務が分かる名前にする。
* **可視性**: `@internal` を付与し、同一パッケージ内からのみ利用する。

## 実装のポイント

* **1 クラス 1 機能**: 一つの Usecase クラスは一つの責務のみ持つ。
* **外部レイヤーを使う場合のみ DI**: 画面外の Repository・Usecase・Infra のインターフェースを参照する場合は、ViewModel の provider で `ref.watch` し、コンストラクタで受け取る。画面内の Delegate や他の画面固有 Usecase だけを使う場合は、呼び出し元で直接 `const` または通常コンストラクタでインスタンス化してよい。
* **冪等性**: 必須としない。StateStream の更新を行っても、純粋に値を返すだけでもよい。
* **public メソッド**: Delegate と同様に `execute` を 1 つ持つ形を推奨するが、StateStream の購読開始など「開始メソッド」が必要な場合は `start` など別名でもよい（1 クラス 1 機能の範囲で）。

## 実装例（ワークスペース）

### パターン1: 値を返す Usecase（外部 Repository を DI で受け取る）

画面のアクション内で都度 Usecase を生成し、ViewModel が DI で保持する Repository を渡して `execute` を呼ぶ。

```dart
// screen_feature_school_grade, usecase/school_grade_sort_load_usecase.dart
/// ソート順をPreferencesから読み込むUsecase.
@internal
class SchoolGradeSortLoadUsecase {
  final PreferencesRepository preferencesRepository;

  const SchoolGradeSortLoadUsecase({
    required this.preferencesRepository,
  });

  /// Preferencesからソート順を読み込む.
  Future<SchoolGradeSortType> execute() async {
    // ...
  }
}
```

ViewModel のアクションからの利用（呼び出しごとに Usecase を生成）:

```dart
// screen_feature_school_grade, school_grade_screen_view_model.action.dart
Future<void> initialize() async {
  await state.updateWithLock((oldState, emitter) async {
    final usecase = SchoolGradeSortLoadUsecase(
      preferencesRepository: preferencesRepository,
    );
    final savedSortType = await usecase.execute();
    // ...
  });
}
```

同様に、`SchoolGradeSortSaveUsecase` は `execute(SchoolGradeSortType)` で Preferences に保存する。ViewModel は `preferencesRepository` を `ref.watch` で受け取り、アクション内で Usecase に渡す。

### パターン2: StateStream を操作する Usecase（冪等でない）

認証状態や他リポジトリのストリームを購読し、ViewModel の `MutableStateStream` を更新する。外部 Repository は ViewModel の provider で `ref.watch` し、Usecase のコンストラクタで渡す。

```dart
// screen_feature_home2, usecase/data_sync_usecase.dart
/// データ同期用のUsecase.
@internal
final class DataSyncUsecase {
  final AuthenticationRepository authenticationRepository;

  const DataSyncUsecase({
    required this.authenticationRepository,
  });

  /// 認証状態の変更を監視する.
  void startAuthentication(
    MutableStateStream<HomeScreenState> dataStream,
  ) {
    dataStream.withSubscription(
      authenticationRepository.authenticationStream.listen((e) {
        _onAuthenticationStateChanged(dataStream, e);
      }),
    );
  }
  // ...
}
```

ViewModel の provider での生成（外部依存を DI で渡す）:

```dart
// screen_feature_home2, home_screen_view_model.dart
static final provider = Provider.autoDispose<HomeScreenViewModel>(
  (ref) {
    final authenticationRepository = ref.watch(
      AuthenticationRepository.provider,
    );
    return HomeScreenViewModel._(
      state: MutableStateStream(HomeScreenState.initial(...)),
      dataSyncUsecase: DataSyncUsecase(
        authenticationRepository: authenticationRepository,
      ),
      // ...
    );
  },
  dependencies: [AuthenticationRepository.provider, ...],
);
```

`SettingsSyncUsecase` も同様に、`AuthenticationRepository` と `AiQuotaRepository` をコンストラクタで受け取り、`start(MutableStateStream<SettingsScreenState>)` でストリーム購読を開始する。ViewModel のコンストラクタ内で `SettingsSyncUsecase(...).start(data)` として即座に生成・実行している。

### ディレクトリ構成（ワークスペース）

```text
app_packages/screen/feature/school_grade/lib/src/viewmodel/
├── school_grade_screen_view_model.dart
├── school_grade_screen_view_model.action.dart
├── usecase/
│   ├── school_grade_sort_load_usecase.dart   # ソート順の読み込み
│   ├── school_grade_sort_save_usecase.dart   # ソート順の保存
│   └── school_grade_screen_state_to_entity_delegate.dart
├── delegate/
│   └── ...
└── ...
```

```text
app_packages/screen/feature/home2/lib/src/viewmodel/
├── home_screen_view_model.dart
└── usecase/
    └── data_sync_usecase.dart   # 認証状態の監視・State 更新
```

```text
app_packages/screen/feature/settings2/lib/src/viewmodel/
├── settings_screen_view_model.dart
└── usecase/
    └── settings_sync_usecase.dart   # 認証・AIチケットの監視・State 更新
```

## 関連文書

* ViewModel の基本設計・構成は [mvvm-viewmodel-design.md](mvvm-viewmodel-design.md) を参照する。
* Delegate の設計・配置は Delegate パターン（および [mvvm-viewmodel-entity.md](mvvm-viewmodel-entity.md) の StateToEntityDelegate）を参照する。

## よくあるパターンとアンチパターン

### 推奨されるパターン

* 複雑なビジネスロジックは ViewModel に書かず、画面固有 Usecase に切り出す。
* 複数の Delegate で同じロジックが必要な場合は、その部分を Usecase にまとめ、Delegate のコンストラクタで Usecase を受け取る。テストでは Mock と実物を切り替えやすくなる。
* **インスタンスの作成を柔軟に取り扱う**。次のいずれも許容し、テストや差し替えのしやすさで選ぶ。
  * **都度 new**: アクション内で `Usecase(依存)` を生成し `execute` を呼ぶ。依存は ViewModel が DI で保持する。
  * **ViewModel のフィールドで保持**: provider 内で 1 回生成し、ViewModel に渡す。外部依存は provider で `ref.watch` し、Usecase のコンストラクタに渡す。
  * **Usecase 自体を Provider にする**: 画面固有 Usecase を `Provider` や `Provider.autoDispose` で提供する。テストでは `container.override` で Mock Usecase に差し替えられる。
* **Delegate のコンストラクタで Usecase を渡す**: Delegate が画面固有 Usecase に依存する場合、コンストラクタ引数で受け取る。本番では実装を、テストでは Mock を渡すことで、Delegate 単体のテストや ViewModel のテストのカバレッジを上げやすい。

### 避けるべきパターン

* 画面固有 Usecase をパッケージ外に公開する。
  * 対応: `@internal` を付ける。
* 1 クラスに複数の無関係な機能を持たせる。
  * 対応: 1 クラス 1 機能を守る。
* 外部レイヤーのインターフェースを直接 new せず、DI で受け取る。
  * 対応: プロジェクトのDI設計を遵守する
