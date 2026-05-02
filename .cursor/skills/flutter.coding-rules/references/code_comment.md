# コードコメント規約

## 概要

本ドキュメントは、プロジェクト内の Dart コードに付与する**ドキュメントコメント**の規約を定義する。

* すべてのクラス名・プロパティ名・関数名には、**必ず日本語のドキュメントコメント**を付与する。
* クラスインターフェース・メソッド・関数には、**利用時の Example を記載する**（特に AI Agent がインターフェースを提案する場合は必須）。
* コメントでは**意図・前提・副作用・注意点**に焦点を当て、自明な記述は避ける。
* ワークスペースの静的解析では `comment_references` が有効であり、ドキュメント内の参照（`[symbol]` 等）が正しく解決される必要がある。

## 必須付与対象

以下のクラス・プロパティ・関数・メソッドには、必ず日本語のドキュメントコメントを付与する。

* **クラス**: 役割の説明、必要に応じて NOTE や Example
* **プロパティ**: 意味・制約・注意点
* **関数・メソッド**: 役割、パラメータ・戻り値の説明、Example（利用例）
* **コンストラクタ**: パラメータの制約（例: 「1文字である必要がある」）

## コードコメントの補足

ドキュメントコメントは、API の意図と使用方法を明確にするために必要である。日本語で記述することで、チーム内での理解が容易になる。

* **自明なコメントは避ける**（例:「値を取得する」は getter 名から自明）。
* **意図・前提条件**を簡潔に記述する。
* **副作用・注意点**がある場合は必ず明記する。
* **パラメータ・戻り値**は `[param]` 形式でドキュメント内から参照できる。
* **AI Agent がインターフェースを提案するとき**は、コメントに**利用時の Example コード**を必ず含める。

## コードコメントの実装例

### クラス・型の説明

```dart
// domain_japanese, japanese_character.dart
/// ひらがな1文字を示す.
class Hiragana implements JapaneseCharacter {
  @override
  final String character;

  const Hiragana(this.character)
    : assert(character.length == 1, "ひらがなは1文字である必要があります");
}
```

### コンストラクタとパラメータの説明

```dart
// domain_japanese, japanese_character.dart
/// 漢字を作成する.
///
/// [character] は漢字1文字である必要がある.
const Kanji(this.character)
  : assert(character.length == 1, "漢字は1文字である必要があります");
```

### NOTE と前提・注意点

```dart
// domain_preferences, preference_key.dart
/// Preferencesに与える単一キー.
///
/// NOTE.
/// DBからの復元やUnit Test等で使いやすいようにコンストラクタを一部開放しているが、
/// 基本的には管理されたキー一覧を使うことを想定している.
extension type const PreferenceKey(String _value) {
}
```

### インターフェース・メソッドと Example（AI Agent 提案時必須）

```dart
// infra_firebase, firebase_analytics_proxy.dart
/// Firebase Analyticsにイベントを記録する.
///
/// [name] イベント名
/// [parameters] イベントパラメータ
///
/// Firebase非対応プラットフォームやテスト環境では、何も実行しない.
///
/// Example:
/// ```dart
/// // 画面遷移イベント（GoRouterのpathをそのまま使用）
/// await proxy.logEvent(name: "/home");
///
/// // タブ移動イベント
/// await proxy.logEvent(
///   name: "tab_selected",
///   parameters: {"tab_name": "HomeScreenTab.home"},
/// );
/// ```
Future<void> logEvent({
  required String name,
  Map<String, Object>? parameters,
});
```

## コードコメントのアンチパターン

以下のようなコメントや欠如は避ける。

### クラス・メソッドにコメントがない

```dart
// アンチパターン: クラスにコメントがない
class ExampleClass {
  String getData() {
    return "";
  }
}
```

### 自明なコメント

```dart
// アンチパターン: 自明なコメント
/// 値を取得する
String get value => _value;
```

### インターフェース・メソッドに Example がない

* メソッドやインターフェースに、利用例（Example）が一切ない。
* API の意図や使用方法が不明確になる。
* AI Agent がインターフェースを提案する場合は、Example の記載が必須である。

## ワークスペースとの関係

* **analysis_options.yaml**: `comment_references` が有効。ドキュメント内の `[symbol]` 等は実在するシンボルを参照している必要がある。
* **type_annotate_public_apis**: 公開 API に型注釈を要求するルールと合わせ、ドキュメントコメントで「何をする API か」を補足する。
* **ファイル編集後の確認**: Analyzer 実行時の確認ポイントの一つに「ドキュメントコメントが不足していないか」が含まれる。プロジェクトの編集後チェックリストを参照する。

## よくあるパターンとアンチパターン

### 推奨パターン

1. **日本語のドキュメントコメントを必ず付与する**  
   型・プロパティ・関数に、意図・前提・副作用・注意点を簡潔に書く。
2. **パラメータは `[param]` で参照する**  
   「[character] は漢字1文字である必要がある」のように、Dart の doc 参照を使う。
3. **NOTE で設計上の前提を書く**  
   テスト用の開放や、想定利用者（「管理されたキー一覧を使うことを想定」）を明示する。
4. **インターフェース・メソッドには Example を書く**  
   特に AI Agent がインターフェースを提案する場合は、利用例を必ず含める。

### 避けるべきパターン

1. **コメントの欠如**  
   クラス・メソッド・プロパティ・関数にコメントがない。
2. **自明な説明**  
   名前から分かることだけを繰り返す（例:「値を取得する」のみの getter コメント）。
3. **Example の欠如**  
   メソッド・インターフェースに利用例がなく、使い方が推測しづらい。
4. **誤った comment_references**  
   存在しないシンボルを `[symbol]` で参照し、リンターエラーになる。
