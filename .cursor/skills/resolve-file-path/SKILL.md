---
name: resolve-file-path
description: >-
  ドキュメント（主に Markdown）に書かれたパス表記を、実ファイルパスへ解決する SKILL。
  クォートされた `path/to/file`（リポジトリルート相対）、Markdown リンク
  `[text](rel)`（リンク元ファイル相対）、`.ai-agent/` の候補順
  （`headquarters/.ai-agent` → ルート `.ai-agent`）を適用する。
  「この MD のリンク先はどこ？」「path/to/file の実体」「.ai-agent はどれ？」
  「参照パスを解決してから読んで」では必ず使う。パス解決前にロードする。
  URL→Issue メタデータは parse.url-to-metadata、Markdown 整形のみは
  markdown.format、内容検索のみは markdown.search では使わない。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# ファイルパス解決

ドキュメントに書かれたパスを、**実際に開くべき絶対パス（またはリポジトリルート相対の確定パス）**へ変換する。
解決を誤ると参照先を読み違え、出力品質が落ちるため、パス付きの参照を扱う前にこの SKILL を適用する。

## いつ使うか

* Markdown / 文書内の `path/to/file` や `[label](path)` の実体を探すとき
* `.ai-agent/` 配下へ一時ファイルを書く／読む場所を決めるとき
* 「ドキュメントの参照先を開いて」と言われ、表記が相対・リンク混在のとき

## いつ使わないか

* GitHub Issue URL から ID/タイトルを取る → `parse.url-to-metadata`
* Markdown の体裁整形だけ → `markdown.format`
* キーワードで文書を探すだけ（パス表記の解決が不要）→ `markdown.search`

## 作業手順

1. 表記がどれかを判別する（クォート相対 / Markdown リンク / `.ai-agent`）
2. 対応ルールで候補パスを組み立てる
3. 存在確認してから読む・書く（無ければ候補と解決ルールを報告する）

## `path/to/file` 形式

クォートされた `path/to/file` は、**Git リポジトリルートからの相対パス**で解決する。

```bash
# リポジトリルートからの相対パス
cat "$(git rev-parse --show-toplevel)/path/to/file"
```

## 特殊ルール / `.ai-agent/`

AI Agent の一時ファイルは `.ai-agent/` 配下に出す。解決は **次の順番**で、最初に存在するディレクトリを採用する。

1. `$(git rev-parse --show-toplevel)/headquarters/.ai-agent/`
2. `$(git rev-parse --show-toplevel)/.ai-agent`

```bash
ROOT="$(git rev-parse --show-toplevel)"

for candidate in \
  "${ROOT}/headquarters/.ai-agent" \
  "${ROOT}/.ai-agent"; do
  ls -ld "$candidate" 2>/dev/null || echo "not found: $candidate"
done

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

HQ モノレポでは `headquarters/.ai-agent` が先に来る点に注意する（ルート直下より優先）。

## `[リンク](path/to/file)` 形式

Markdown リンクのパスは、**そのリンクが書かれているファイルからの相対パス**で解決する（リポジトリルート基準ではない）。

```bash
# example/markdown/file.md に [example](../doc.txt) とある場合
SOURCE_MD="$(git rev-parse --show-toplevel)/example/markdown/file.md"
RELATIVE_PATH="../doc.txt"
cat "$(dirname "$SOURCE_MD")/$RELATIVE_PATH"
```

## ナレッジベース

### DO: 表記の種類を先に分けてから解決する

* ルート相対とリンク元相対を混ぜると、別ファイルを開いてしまう

### DO: `.ai-agent` は候補順を守り、存在する最初のものを使う

* HQ 構成では `headquarters/.ai-agent` がルート `.ai-agent` より優先

### DO NOT: Markdown リンクをリポジトリルート相対だと決めつける

* `[text](../x.md)` はリンク元ディレクトリ基準

### DO NOT: パスを解決せずに「たぶんこのファイル」で読み進める

* 解決失敗時は候補とルールを示し、推測読みを避ける
