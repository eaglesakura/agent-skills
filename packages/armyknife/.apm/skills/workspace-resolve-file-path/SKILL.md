---
name: workspace-resolve-file-path
description: >-
  ドキュメント（主に Markdown）に書かれたパス表記を、実ファイルパスへ解決する SKILL。
  クォートされた `path/to/file`（リポジトリルート相対）、Markdown リンク
  `[text](rel)`（リンク元ファイル相対）、`.ai-agent/` の候補順
  （`headquarters/.ai-agent` → ルート `.ai-agent`）、および `{assets}/...`
  （frontmatter の `metadata.assets` 候補ディレクトリから探索）を適用する。
  「この MD のリンク先はどこ？」「path/to/file の実体」「.ai-agent はどれ？」
  「`{assets}/template.md` の実体」「参照パスを解決してから読んで」では必ず使う。
  パス解決前にロードする。URL→Issue メタデータは workspace-resolve-url-metadata、
  Markdown 整形のみは markdown.format、内容検索のみは markdown-search では使わない。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# Workspace / Resolve File Path

ドキュメントに書かれたパスを、**実際に開くべき絶対パス（またはリポジトリルート相対の確定パス）**へ変換する。
解決を誤ると参照先を読み違え、出力品質が落ちるため、パス付きの参照を扱う前にこの SKILL を適用する。

## いつ使うか

* Markdown / 文書内の `path/to/file` や `[label](path)` の実体を探すとき
* `{assets}/...` 形式のアセット参照を、frontmatter の候補ディレクトリから実体へ落とすとき
* `.ai-agent/` 配下へ一時ファイルを書く／読む場所を決めるとき
* 「ドキュメントの参照先を開いて」と言われ、表記が相対・リンク・メタ変数混在のとき

## いつ使わないか

* GitHub Issue URL から ID/タイトルを取る → `workspace-resolve-url-metadata`
* Markdown の体裁整形だけ → `markdown.format`
* キーワードで文書を探すだけ（パス表記の解決が不要）→ `markdown-search`

## 作業手順

1. 表記がどれかを判別する（クォート相対 / Markdown リンク / `{assets}/` / `.ai-agent`）
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

## `{assets}/...` 形式

APM などでインストール先が変わっても参照を保てるよう、アセットは **メタ変数** `{assets}/` で書き、実ディレクトリは frontmatter の `metadata.assets` に候補として列挙する。

### いつ使うか

* コマンド / SKILL 本文や `metadata.references` に `{assets}/template.md` のように書かれているとき
* パッケージソースと `apm_modules/` 展開先の両方に同じアセットがあり得るとき

### 入力の読み方

1. **参照文字列**: `{assets}/` 以降をサフィックスとする（例: `{assets}/template.md` → `template.md`）
2. **候補ディレクトリ**: 同じファイルの frontmatter `metadata.assets` を上から読む
   * プレーン文字列: そのままディレクトリパス
   * Markdown リンク `[label](path)`: `path` をディレクトリパスとして使う（YAML ではクォートすること）
3. **基準ファイル**: `{assets}/` が書かれているファイル自身（`SKILL.md` / `.prompt.md` / `.cursor/commands/*.md` など）

### 解決手順

各 `metadata.assets` エントリについて、次の **2 基準**で候補を作る（どちらも試す）。

1. **文書相対**: `dirname(基準ファイル) / assets候補 / サフィックス`
2. **ワークスペース（リポジトリ）ルート相対**: `$(git rev-parse --show-toplevel) / assets候補 / サフィックス`

存在するファイル（またはディレクトリ）を **ヒット**として列挙する。重複パスは 1 回にまとめる。

* ヒットが 1 件 → それを実体として使う
* ヒットが複数 → すべて示し、利用側が選べるようにする。非対話で 1 つに決める必要がある場合は、`metadata.assets` の列挙順で最初にヒットしたものを採用する（文書相対とルート相対の両方ヒットした同一エントリでは文書相対を先とする）
* ヒットが 0 件 → 試した候補パス一覧とルールを報告し、推測読みはしない

### 実例（`github.create-pull-request`）

frontmatter（要約）:

```yaml
metadata:
  assets:
    - "[github.create-pull-request/](../assets/github.create-pull-request/)"
    - apm_modules/eaglesakura/agent-skills/packages/armyknife/.apm/assets/github.create-pull-request/
  references:
    - "`{assets}/template.md`"
```

本文参照: `{assets}/template.md`

基準ファイルがパッケージソースの `.apm/prompts/github.create-pull-request.prompt.md` のとき、主な候補は次になる。

```text
# 文書相対 × 1件目
.apm/prompts/../assets/github.create-pull-request/template.md
  → .apm/assets/github.create-pull-request/template.md

# ルート相対 × 2件目（利用者が apm install した場合）
apm_modules/eaglesakura/agent-skills/packages/armyknife/.apm/assets/github.create-pull-request/template.md
```

```bash
ROOT="$(git rev-parse --show-toplevel)"
SOURCE_MD="path/to/github.create-pull-request.prompt.md"  # または展開後の .cursor/commands/...
SUFFIX="template.md"

# metadata.assets から取り出した DIR 候補ごとに:
for DIR in \
  "../assets/github.create-pull-request" \
  "apm_modules/eaglesakura/agent-skills/packages/armyknife/.apm/assets/github.create-pull-request"
do
  for CAND in \
    "$(dirname "$SOURCE_MD")/${DIR}/${SUFFIX}" \
    "${ROOT}/${DIR}/${SUFFIX}"
  do
    # 正規化して存在確認
    if [ -e "$CAND" ]; then
      echo "HIT: $CAND"
    else
      echo "miss: $CAND"
    fi
  done
done
```

### 書き手向けメモ

* 本文・`metadata.references` にはインストール先の絶対的な 1 パスだけを書かず、`{assets}/...` を使う
* `metadata.assets` には **ソース相対**（開発時）と **install 後ルート相対**（利用者ワークスペース）を並べる
* APM が frontmatter の `metadata` を落とすターゲットでも、本文の `{assets}/` とパッケージ実体（`apm_modules/...` やソース側）の定義を突き合わせて解決する

## ナレッジベース

### DO: 表記の種類を先に分けてから解決する

* ルート相対とリンク元相対を混ぜると、別ファイルを開いてしまう
* `{assets}/` は先に `metadata.assets` を読み、通常の相対パス解決に落とさない

### DO: `.ai-agent` は候補順を守り、存在する最初のものを使う

* HQ 構成では `headquarters/.ai-agent` がルート `.ai-agent` より優先

### DO: `{assets}/` は全候補を試し、ヒットを明示する

* install 前後で生きるパスが違うため、1 候補だけで決め打ちしない

### DO NOT: Markdown リンクをリポジトリルート相対だと決めつける

* `[text](../x.md)` はリンク元ディレクトリ基準

### DO NOT: パスを解決せずに「たぶんこのファイル」で読み進める

* 解決失敗時は候補とルールを示し、推測読みを避ける

### DO NOT: `{assets}/` をリテラルなディレクトリ名だと思い込む

* `{assets}` はメタ変数であり、ディスク上のフォルダ名ではない
