---
name: flutter.layered-architecture.code-search
description: コードベースのドキュメントや既存コードの場所の詳細な調査を行うSKILL。特定機能に関するドキュメント、ディレクトリ、パッケージ等の場所や内容を調べます。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# Flutter / コード検索

* リポジトリ内のファイル・フォルダレイアウトを調査する
* 指定された機能・内容に関するコード、ドキュメントを、リポジトリ内から見つけ出す

## 入力値

与えられたプロンプトから下記の調査対象を判断する

例:

* リポジトリ内の機能
* アーキテクチャレイヤー
* パッケージ
* 具体的なソースコード

## 出力値

* 下記をレポートとして出力する

```markdown

<!-- 
出力テンプレート
 -->

# 調査結果 {調査内容}

## {調査内容の項目}

{要求された調査対象についてのサマリ}

* {調査対象の発見有無}
* {調査対象に関連するサブモジュール、ソースコード一覧}
  * ファイルツリー構造で出力する
* {調査対象内に含まれるTODO, FIXME等の埋め込み関連Issue}
* {コメントブロックから推測される留意事項}
```

ファイルツリー構造を出力する例

```text
├── app_packages/usecase/feature_x/
│   ├── lib/
│   │   └── usecase_feature_x.dart
│   └── pubspec.yaml 
├── app_packages/usecase/feature_x/_impl/
│   └── pubspec.yaml
├── app_packages/screen/feature/feature_x2/
│   ├── lib/
│   │   ├── screen_feature_feature_x2.dart
│   │   └── src/
│   │       ├── feature_x_screen_factory.dart
│   │       └── viewmodel/
│   │           └── state/
│   │               └── feature_x_screen_state.dart
│   └── pubspec.yaml
└── app_packages/old_feature_y/
```

ソースコードを出力する例

* 出力量を最適化するため、関連部分だけを引用する

```dart
/* 省略 */

void main() {
  /* 省略 */

  test("Flavor.current", () {
    expect(Flavor.current, isA<FlavorDevelopment>());
  });
}

```

## 調査手順

* ワークスペースの `pubspec.yaml` の `workspace:` ブロックから、すべてのpackageのレイアウトを把握する

  ```yaml
  workspace:
    - app
    - app_packages/data/database
    # 以下、すべてのpackageが列挙されている
  ```

* 関連SKILLから、リポジトリのレイアウト及びレイヤードアーキテクチャの構造を把握する
* アーキテクチャ構造から、対象となるpackageを推測する
* 対象packageを適宜探索し、必要な情報を収集する

## リポジトリを探索するヒント

### 1クラス1ファイルの原則

* 本アーキテクチャでは、 `1ファイルには基本的に1クラス` のみが記述される基本ルールがあるため、ファイル名を列挙することで内容を推測できる
