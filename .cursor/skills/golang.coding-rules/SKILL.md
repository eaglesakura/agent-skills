---
name: golang.coding-rules
description: Golangコーディング規約遵守のSKILL, *.goファイルを記述するに当たって必ず守らなければならないルール、一般的な実装パターンのアーキテクチャ説明
license: MIT License
metadata:
  author: "@eaglesakura"
---
# Golangコーディング規約

* `*.go` ファイルについて実装や修正を行う場合、必ずこのSKILLに示された規約に従う

## 文脈に応じたドキュメントのロード

詳細については、文脈に応じた追加ドキュメントを読み込む.

* [general](./references/general.md)
  * 一般コーディング規約
  * *.goファイル全般に関わるコーディング規約
* [data_object](./references/data_object.md)
  * 例: データオブジェクト（Data transfer objectや、data class, typedef, 構造体といった文脈）を扱う場合
* [code_comment](./references/code_comment.md)
  * コードコメント規約
  * すべての関数・構造体・インターフェース等のpublicなオブジェクトにはコメントが必須であり、すべてのコメントはこのドキュメントの内容に従う必要がある
  * 例: ドキュメントコメントの付与・修正、API の Example 記載を行う場合
