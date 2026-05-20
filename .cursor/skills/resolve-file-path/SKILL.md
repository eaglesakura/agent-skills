---
name: resolve-file-path
description: ワークスペース内のドキュメント内容に記載されたパスから、実際のファイルパスを探索するSKILL. 主にMarkdown形式で記載されたファイルのpathを解決するために使用する. ドキュメントの参照先解決有無は、プロンプトの出力品質に直結するため、パス解決前にかならずロードする.
license: MIT License
metadata:
  author: "@eaglesakura"
---

# ファイルパス解決

## `path/to/file` 形式

* クォートされた `path/to/file` で記載されたパスは、Gitリポジトリのルートディレクトリからの相対パスで解決する

```bash
# リポジトリルートからの相対パス
cat "$(git rev-parse --show-toplevel)/path/to/file"
```

## [リンク](path/to/file) 形式

* Markdown内のリンクで記載されたパスは、該当ファイルからの相対パスで解決する

```bash
# example/markdown/file.md に [example](../doc.txt) で記載されている場合
SOURCE_MD="$(git rev-parse --show-toplevel)/example/markdown/file.md"
RELATIVE_PATH="../doc.txt"
cat "$(dirname "$SOURCE_MD")/$RELATIVE_PATH"
```
