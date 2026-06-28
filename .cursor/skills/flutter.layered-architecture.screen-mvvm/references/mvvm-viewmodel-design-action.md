# ViewModel レイヤー / アクションメソッドと Delegate 分離

## 概要

本ドキュメントは、Widget から呼び出す **ViewModel アクション** の設計方針を定義する。
アクションは拡張メソッド `onXXXX()` として公開し、処理本体は **Delegate クラス** に分離する。ViewModel 本体は provider・状態・Entity・イベントの公開に専念し、アクションは `part` ファイルと `delegate/` 配下に整理する。

Delegate の基本構造（`execute` メソッド、コンストラクタ設計、命名）は **Delegate パターン** に従う。本ドキュメントは ViewModel アクションに特化した **必須ルール** を定める。

## 必須ルール

以下は ViewModel アクション実装における **必須** 事項である。例外は認めない。

| # | ルール | 理由 |
| - | -- | -- |
| 1 | Widget から呼び出すアクションは、すべて `onXXXX()` の **拡張メソッド** とする | View 層からの入口を命名で統一し、ViewModel 本体を肥大化させない |
| 2 | すべてのアクションは `{画面名}_screen_view_model.action.dart` に **part で分離** する | ViewModel 本体とアクションの責務をファイル単位で分離する |
| 3 | すべてのアクションは **Delegate パターン** に従い、`OnXxxxxDelegate` クラスとして分離する | 単一責務・テスト容易性・見通しの良さ |
| 4 | Delegate が必要とする State・Usecase・Repository 等は、**コンストラクタ引数** で受け取る | Unit Test で Mock 注入を容易にする |
| 4a | 画面固有 Usecase は **Delegate 内で `new` しない**。**`onXXXX()` 内**（Delegate を `new` するタイミング）で事前生成し、コンストラクタ注入する | 依存の明示とテスト容易性（無駄なインスタンス化のコストは受け入れる） |
| 5 | Delegate は **`execute` メソッドを 1 つ** 持ち、引数は対応する `onXXXX()` と **同一** とする | 呼び出し元メソッドと Delegate の対応を明確にする |
| 6 | Delegate は `onXXXX()` 内で **都度生成し、使い捨てる** | Delegate がフィールドを保持して Stateful になることを防ぐ |

### ルール 1: `onXXXX()` 拡張メソッド

* アクションは ViewModel クラス本体に直接書かず、`part` ファイル内の **extension** に定義する。
* extension 名は `{画面名}ScreenViewModelActions` とする（例: `KanjiKanamajiriScreenViewModelActions`）。
* メソッド名は `on` + 動詞句（PascalCase）とする。例: `onInitialize`, `onInputTextChanged`, `onTapConvertButton`, `onChangeSortType`。
* 初期化処理も `initialize()` ではなく **`onInitialize()`** とする。

```dart
// screen_feature_kanji_kanamajiri, kanji_kanamajiri_screen_view_model.action.dart
part of "kanji_kanamajiri_screen_view_model.dart";

@internal
extension KanjiKanamajiriScreenViewModelActions
    on KanjiKanamajiriScreenViewModel {
  Future<void> onInitialize() async { /* ... */ }
  Future<void> onInputTextChanged(String text) async { /* ... */ }
  Future<void> onTapConvertButton(FutureContext cancelContext) async { /* ... */ }
}
```

View 層からの呼び出し例:

```dart
// screen_feature_kanji_kanamajiri, kanji_kanamajiri_screen.dart
useEffect(() {
  viewModel.onInitialize();
  return null;
}, [viewModel]);
```

### ルール 2: `part` ファイルへの分離

* ViewModel 本体（`{画面名}_screen_view_model.dart`）に `part "{画面名}_screen_view_model.action.dart";` を宣言する。
* アクションファイル先頭は `part of "{画面名}_screen_view_model.dart";` とする。
* アクションファイル内では ViewModel の `@visibleForTesting` フィールド（`state`, Usecase 等）にアクセスできる。

```dart
// screen_feature_kanji_kanamajiri, kanji_kanamajiri_screen_view_model.dart
part "kanji_kanamajiri_screen_view_model.action.dart";
```

### ルール 3〜6: Delegate 分離と使い捨てインスタンス

各 `onXXXX()` は **オーケストレーションのみ** を担当する。処理本体は対応する `OnXxxxxDelegate` に委譲する。

```dart
// screen_feature_kanji_kanamajiri, kanji_kanamajiri_screen_view_model.action.dart
Future<void> onTapConvertButton(FutureContext cancelContext) async {
  final delegate = OnTapConvertButtonDelegate(
    state: state,
    extractAllowedKanjiUsecase: extractAllowedKanjiUsecase,
    translateKanjiKanamajiriUsecase: translateKanjiKanamajiriUsecase,
    queryErrorUsecase: queryErrorUsecase,
  );
  await delegate.execute(cancelContext: cancelContext);
}
```

* Delegate クラスは `lib/src/viewmodel/delegate/on_{動詞句}_delegate.dart` に配置する。
* クラス名は `On` + 動詞句（PascalCase）+ `Delegate` とする。例: `OnTapConvertButtonDelegate`, `OnInitializeDelegate`。
* `onXXXX()` 内で `final delegate = OnXxxxxDelegate(...)` として生成し、`delegate.execute(...)` を呼ぶ。**ViewModel のフィールドとして Delegate を保持しない。**

## 処理フロー

```text
View (Widget)
  │  viewModel.onXXXX(args)
  ▼
Extension ({Screen}ViewModelActions)     ← part .action.dart
  │  final delegate = OnXxxxxDelegate(dependencies...)
  │  await delegate.execute(args)
  ▼
OnXxxxxDelegate                          ← delegate/on_xxxx_delegate.dart
  │  execute(args) { ビジネスロジック }
  ▼
StateStream / Usecase / Repository
```

## ファイルレイアウト

```text
lib/src/viewmodel/
├── {画面名}_screen_view_model.dart           # 本体（provider, state, entity, event, part 宣言）
├── {画面名}_screen_view_model.action.dart    # アクション拡張メソッド（part）【必須】
└── delegate/
    ├── on_initialize_delegate.dart           # OnInitializeDelegate
    ├── on_input_text_changed_delegate.dart   # OnInputTextChangedDelegate
    └── on_tap_convert_button_delegate.dart   # OnTapConvertButtonDelegate
```

**StateToEntityDelegate**（`entity` 変換用）と **アクション Delegate**（`onXXXX` 用）は責務が異なる。前者は State→Entity 変換の設計に従い ViewModel フィールドとして保持してよい。後者は本ドキュメントのルール 6 に従い、**都度生成・使い捨て** とする。

## Delegate クラスの実装

### 基本構造

```dart
// screen_feature_kanji_kanamajiri, delegate/on_input_text_changed_delegate.dart
@internal
class OnInputTextChangedDelegate {
  @internal
  final MutableStateStream<KanjiKanamajiriScreenState> state;

  const OnInputTextChangedDelegate({
    required this.state,
  });

  Future<void> execute(String text) async {
    await state.updateWithLock((oldState, emitter) async {
      // 処理ロジック
    });
  }
}
```

### 依存が多いアクション

ViewModel が `ref.watch` で保持する外部依存は、`onXXXX()` から Delegate のコンストラクタへ渡す。

```dart
// screen_feature_kanji_kanamajiri, delegate/on_tap_convert_button_delegate.dart
@internal
class OnTapConvertButtonDelegate {
  @internal
  final MutableStateStream<KanjiKanamajiriScreenState> state;
  @internal
  final ExtractAllowedKanjiUsecase extractAllowedKanjiUsecase;
  @internal
  final TranslateKanjiKanamajiriUsecase translateKanjiKanamajiriUsecase;
  @internal
  final QueryErrorUsecase queryErrorUsecase;

  const OnTapConvertButtonDelegate({
    required this.state,
    required this.extractAllowedKanjiUsecase,
    required this.translateKanjiKanamajiriUsecase,
    required this.queryErrorUsecase,
  });

  Future<bool> execute({required FutureContext cancelContext}) async {
    // 変換処理
  }
}
```

* コンストラクタ引数は、その Delegate が **実際に使用する** 依存のサブセットとする。画面固有 Usecase も含め、すべて **`onXXXX()` 内で事前にインスタンス化したもの** を渡す。
* Delegate の `execute` 内で `Usecase(...)` を `new` してはならない（ViewModel 文脈の Usecase 設計に従う）。

### `execute` の戻り値

* 原則として `onXXXX()` と `execute` の戻り値型は同一とする。
* `Future<void>` が一般的だが、処理の成否を呼び出し元に返す必要がある場合は `Future<bool>` 等もよい（例: `OnTapConvertButtonDelegate.execute`）。

## Unit Test

アクション Delegate は ViewModel 全体を経由せず、**Delegate 単体** でテストする。

```dart
// screen_feature_kanji_kanamajiri, test/viewmodel/delegate/on_input_text_changed_delegate_test.dart
late OnInputTextChangedDelegate delegate;
late MutableStateStream<KanjiKanamajiriScreenState> stateStream;

setUp(() {
  stateStream = MutableStateStream(/* 初期 State */);
  delegate = OnInputTextChangedDelegate(state: stateStream);
});

test("入力テキストが更新される", () async {
  await delegate.execute("テスト文章");
  expect(stateStream.state.inputText, "テスト文章");
});
```

* Usecase を Mock する場合は、コンストラクタに Mock インスタンスを渡す。
* テスト配置は `test/viewmodel/delegate/{delegate名}_test.dart` を推奨する。
* 詳細は ViewModel レイヤーの Unit Test 設計に従う。

## よくあるパターンとアンチパターン

### 推奨されるパターン

* すべての Widget 呼び出し口を `onXXXX()` に統一する。
* `onXXXX()` は Delegate の生成と `execute` 呼び出しのみに留める。
* 複数 Delegate で共有するロジックは、`@internal` 属性の画面固有 Usecase として独立化する（ViewModel 文脈の Usecase 設計に従う）。
* `@internal` を ViewModel・extension・Delegate に付与し、パッケージ外に露出しない。

### Delegate 間の共通処理

* **DO**: Delegate 間で共通処理が必要な場合は、`@internal` 属性を付与した画面固有 Usecase として独立化する。`onXXXX()` 内で Usecase を生成し、各 Delegate のコンストラクタへ注入する。共通ロジックは Usecase 単体の Unit Test で検証する。
* **DO NOT**: Delegate 間の共通処理をコールバック（関数型引数・クロージャ等）で共通化してはならない。コールバックはテスタビリティが低く、Mock 注入や Unit Test が困難になるため禁止する。共通処理は Usecase に切り出し、Usecase 単体テストで検証する。

```dart
// screen_feature_example, usecase/validate_input_usecase.dart
@internal
class ValidateInputUsecase {
  const ValidateInputUsecase();

  Future<bool> execute(String text) async {
    // 複数 Delegate で共有する検証ロジック
  }
}

// screen_feature_example, example_screen_view_model.action.dart
Future<void> onInputTextChanged(String text) async {
  final validateInputUsecase = const ValidateInputUsecase();
  final delegate = OnInputTextChangedDelegate(
    state: state,
    validateInputUsecase: validateInputUsecase,
  );
  await delegate.execute(text);
}

Future<void> onTapSubmitButton() async {
  final validateInputUsecase = const ValidateInputUsecase();
  final delegate = OnTapSubmitButtonDelegate(
    state: state,
    validateInputUsecase: validateInputUsecase,
  );
  await delegate.execute();
}
```

### 避けるべきパターン

| アンチパターン | 問題 | 正しい対応 |
| -- | -- | -- |
| ViewModel 本体にアクションメソッドを直接書く | 本体が肥大化し、責務が混在する | `part .action.dart` の extension に移す |
| `initialize()` 等、`on` 接頭辞のないメソッド名 | View 層の呼び出し口が不統一 | `onInitialize()` 等にリネーム |
| `.action.dart` 内にビジネスロジックを直書き | Delegate 分離の目的が達成できない | `OnXxxxxDelegate` に移す |
| Delegate を ViewModel のフィールドとして保持 | Delegate が状態を持ち、テスト・再利用が困難になる | `onXXXX()` 内で都度生成する |
| 1 つの Delegate に複数の public メソッド | 単一責務に反する | アクションごとに Delegate を分割 |
| Delegate の `execute` 内で Usecase を `new` する | 依存が隠蔽され、Mock 注入が困難になる | `onXXXX()` 内で事前生成し、コンストラクタ注入する |
| ViewModel の provider で画面固有 Usecase を保持する | Delegate 未使用の Usecase が ViewModel に残る | `onXXXX()` 内で `new` し、Delegate に注入する |
| Delegate のコンストラクタで `ref.watch` する | DI の責務が Delegate に漏れる | ViewModel が解決した依存を引数で渡す |
| Delegate 間の共通処理をコールバックで共通化する | テスタビリティが低く、Mock 注入・Unit Test が困難 | `@internal` 画面固有 Usecase に切り出し、Usecase 単体テストで検証する |
