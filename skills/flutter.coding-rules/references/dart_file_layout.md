# Dart ファイル・レイアウト規約

## 概要

本ドキュメントは、Dart プロジェクトにおける**ファイル名規約**・**1クラス1ファイル**・**library ファイル**・**ファイル命名・配置**のルールを定義する。

* Dart のソースファイル名は **`snake_case.dart`** を採用する。
* 1ファイルに1クラスを原則とし、ファイル名はクラス名を `snake_case` に変換したものとする。
* 各パッケージの library ファイルは **`lib/{パッケージ名}.dart`** とし、パッケージ名と同一のファイル名とする。
* 命名・配置を統一することで、インポートパスと責務が明確になり、可読性・保守性が向上する。

## Dart ファイル名規約

Dart のソースファイル名は `snake_case.dart` とする。クラスを格納するファイルは、クラス名を `snake_case` に変換した名前と一致させる。

### Dart ファイル名規約の補足

ファイル名とクラス名の対応を一意にすることで、ファイル名からクラス名を推測しやすくし、検索・リファクタリングを容易にする。Dart の公式スタイルガイドでも `snake_case` が推奨されている。

### Dart ファイル名規約の実装例

* クラス名 `KanjiPracticeScreenViewModel` → ファイル名 `kanji_practice_screen_view_model.dart`
* クラス名 `ExampleClassName` → ファイル名 `example_class_name.dart`

### Dart ファイル名規約のアンチパターン

* `PascalCase.dart` や `camelCase.dart` など、`snake_case` 以外のファイル名は使用しない。

## 1クラス1ファイルの原則

クラスを記述する場合、1ファイルに1クラスを原則とする。クラス名に対応するファイル名は、クラス名を `snake_case` に変換したものとする。

### 1クラス1ファイルの補足

1クラス1ファイルにより、ファイルの責務が明確になり、コードの可読性と保守性が向上する。大規模なクラスでも、1ファイルに1クラスを維持する。

### 1クラス1ファイルの実装例

`ExampleClassName` というクラス名に対し、ファイル名は `example_class_name.dart` とする。

### 1クラス1ファイルのアンチパターン

1ファイルに複数の public クラスを定義することは避ける。

```dart
// アンチパターン: 1ファイルに複数の public クラス
class ClassA {}

class ClassB {}
```

## library ファイル

**library ファイル**とは、各パッケージの `lib/` 直下に置く Dart ファイルであり、パッケージの公開 API を定義する。ファイル名は **パッケージ名と同一**（`{パッケージ名}.dart`）とする。`export` するのは公開 API となるファイルのみとする。

### library ファイルの補足

パッケージ名と同一のファイル名にすることで、`import "package:パッケージ名/パッケージ名.dart"` が `import "package:パッケージ名/パッケージ名.dart"` の形で統一され、インポートパスとパッケージの対応が明確になる。`lib/` 直下に置くため、`import "package:usecase_school/usecase_school.dart"` のように参照する。

### library ファイルの実装例

ワークスペース内の実例（パッケージ名 `usecase_school`、library ファイル `lib/usecase_school.dart`）：

```dart
// app_packages/usecase/school/lib/usecase_school.dart
library;

export "src/kanji_search/kanji_search_request.dart";
export "src/kanji_search/kanji_search_result.dart";
export "src/kanji_search/kanji_search_usecase.dart";
export "src/kanji_list_by_school_grade/kanji_list_by_school_grade_request.dart";
// ... 公開 API のみを列挙
```

### library ファイルのアンチパターン

パッケージ名と異なる library ファイル名を使用しない。例：パッケージ名 `usecase_school` なのに `lib/school.dart` とするのは誤りである。

## ファイル命名・配置の原則

* ファイル名は **`snake_case.dart`** を採用する。
* **1クラス1ファイル**に従い、クラス名を `snake_case` に変換したファイル名を使用する。
* 各パッケージは **`lib/{パッケージ名}.dart`** を必ず持ち、パッケージ名と同一の library ファイル名とする。
* ソースは `lib/src/` 以下に配置し、公開 API は library ファイルの `export` で列挙する。

### ファイル命名・配置の補足

命名と配置を統一することで、可読性と保守性が向上する。パッケージ名と library ファイル名を同一にすることで、インポートパスが一貫する。

### ファイル命名・配置の実装例

ワークスペースにおけるパッケージ配置の例：

```text
app_packages/usecase/school/
├── pubspec.yaml          # name: usecase_school
├── lib/
│   ├── usecase_school.dart   # パッケージ名と同一の library ファイル
│   └── src/
│       ├── kanji_search/
│       │   ├── kanji_search_request.dart
│       │   ├── kanji_search_result.dart
│       │   └── kanji_search_usecase.dart
│       └── ...
```

ファイル名の命名例：

* クラス名: `ExampleClassName` → ファイル名: `example_class_name.dart`
* クラス名: `KanjiPracticeScreenViewModel` → ファイル名: `kanji_practice_screen_view_model.dart`

## ワークスペースとの関係

* ワークスペースではパッケージが **`app_packages/`** 以下（および他ルート）に配置され、各パッケージは **`lib/{パッケージ名}.dart`** を library ファイルとして持つ。
* `pubspec.yaml` の `name` と、library ファイルのベース名（拡張子を除く）は一致させる。例：`name: usecase_school` → `lib/usecase_school.dart`。
* 実装やテスト用のサブパッケージ（`_impl`、`_test`、`_testing`、`_mobile` 等）も同様に、それぞれのパッケージ名と同一の library ファイル名を用いる。

## よくあるパターンとアンチパターン

### 推奨されるパターン

1. **1クラス1ファイルの原則**
   * クラスを記述する場合、1ファイルに1クラスを原則とする。
   * ファイル名はクラス名を `snake_case` に変換したものとする。

2. **library ファイルの命名規則**
   * パッケージ名と同一のファイル名を `lib/` 直下に置く。
   * 例：パッケージ名 `usecase_school` → ファイル名 `lib/usecase_school.dart`。

3. **ファイル名の統一**
   * すべての Dart ソースファイルに `snake_case.dart` を適用する。

### 避けるべきパターン

1. **1ファイルに複数の public クラス**
   * 責務が分散し、可読性が下がる。1クラス1ファイルを守る。

2. **library ファイル名の不一致**
   * パッケージ名と異なる library ファイル名（例：`lib/school.dart`）を使用しない。インポートパスが不明確になる。

3. **ファイル名の snake_case 違反**
   * `PascalCase.dart` や `camelCase.dart` は使用しない。
