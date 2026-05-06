---
name: flutter.coding-rules
description: Flutter / dartコーディング規約遵守のSKILL, dartファイルを記述するに当たって必ず守らなければならないルール、一般的なDelegateパターン等、実装パターンのアーキテクチャ説明
license: MIT License
metadata:
  author: @eaglesakura
---
# Flutter & Dartコーディング規約

* `*.dart` ファイルについて実装や修正を行う場合、必ずこのSKILLに示された規約に従う

## 文脈に応じたドキュメントのロード

詳細については、文脈に応じた追加ドキュメントを読み込む.

* [クラス作成のテンプレート](./assets/architecture_data_object.code-snippets)
  * 例: データオブジェクト（Data transfer objectや、data class, 構造体といった文脈）を扱う場合
* [data_object](./references/data_object.md)
  * 例: データオブジェクト（Data transfer objectや、data class, 構造体といった文脈）を扱う場合
* [delegate-pattern](./references/delegate-pattern.md)
  * 例: Delegate パターンによるクラス分離を行う場合
* [code_comment](./references/code_comment.md)
  * 例: ドキュメントコメントの付与・修正、API の Example 記載を行う場合
* [code_internal](./references/code_internal.md)
  * 例: 可視性の付与・修正、`@internal`・`@visibleForTesting`・`@protected` を扱う場合
* [dart_file_layout](./references/dart_file_layout.md)
  * 例: ファイル名・1クラス1ファイル・library ファイル・パッケージ配置を扱う場合
* [enum](./references/enum.md)
  * 例: enum の利用・dot-shorthands・switch の網羅性を扱う場合
* [try-catch](./references/try-catch.md)
  * 例: 例外処理・Error/Exception の catch 方針・理由コメントを扱う場合
