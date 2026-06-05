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

## 特殊ルール / `.ai-agent/`

* AI Agentは、 `.ai-agent/` ディレクトリ配下のディレクトリに一時ファイルの出力を行う
* `.ai-agent/` ディレクトリの解決は、指定順番に解決を行う
  * `$(git rev-parse --show-toplevel)/headquarters/.ai-agent/`
  * `$(git rev-parse --show-toplevel)/.ai-agent`

```bash
ROOT="$(git rev-parse --show-toplevel)"

# 指定順に候補を列挙して存在確認する
for candidate in \
  "${ROOT}/headquarters/.ai-agent" \
  "${ROOT}/.ai-agent"; do
  ls -ld "$candidate" 2>/dev/null || echo "not found: $candidate"
done

# 最初に存在するディレクトリを採用する
AI_AGENT_DIR=""
for candidate in \
  "${ROOT}/headquarters/.ai-agent" \
  "${ROOT}/.ai-agent"; do
  if [ -d "$candidate" ]; then
    AI_AGENT_DIR="$candidate"
    break
  fi
done

# 例: 一時ファイルを出力する
# mkdir -p "${AI_AGENT_DIR}/tmp"
```

## [リンク](path/to/file) 形式

* Markdown内のリンクで記載されたパスは、該当ファイルからの相対パスで解決する

```bash
# example/markdown/file.md に [example](../doc.txt) で記載されている場合
SOURCE_MD="$(git rev-parse --show-toplevel)/example/markdown/file.md"
RELATIVE_PATH="../doc.txt"
cat "$(dirname "$SOURCE_MD")/$RELATIVE_PATH"
```
