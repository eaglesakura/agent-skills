---
name: workspace-resolve-agent-assets
description: >-
  ドキュメント内の `{assets}/...` メタ変数だけを実ファイルパスへ解決する SKILL。
  本文 `## アセットディレクトリ`（`## assets` / `### assets` も可）と互換の
  `metadata.assets` から候補を集め、文書相対とリポジトリルート相対の両方で探す。
  「`{assets}/template.md` の実体」「アセットを解決してからロード」
  「APM の template を開いて」「アセットディレクトリから読んで」では必ず使う。
  通常の path/to/file・Markdown リンク・`.ai-agent/` は workspace-resolve-file-path、
  URL メタデータは workspace-resolve-url-metadata を使う（混同しない）。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# Workspace / Resolve Agent Assets

APM などでインストール先が変わっても参照を保てるよう、アセットは **メタ変数** `{assets}/` で書く。
本 SKILL はその表記を、文書に書かれた候補ディレクトリから実パスへ落とす。

## いつ使うか

* コマンド / SKILL 本文や関連ファイルに `{assets}/template.md` のように書かれているとき
* パッケージソースと `apm_modules/` 展開先の両方に同じアセットがあり得るとき
* 「アセットを解決してから読んで」「`{assets}/` の実体はどこ？」と聞かれたとき

## いつ使わないか

* クォート相対 `path/to/file`、Markdown リンク `[text](rel)`、`.ai-agent/` の場所決め → `workspace-resolve-file-path`
* GitHub Issue URL から ID/タイトルを取る → `workspace-resolve-url-metadata`
* キーワードで文書を探すだけ → `markdown-search`

## 作業手順

1. 参照文字列からサフィックスを取る
2. 基準ファイルから候補ディレクトリ一覧を集める
3. 各候補について文書相対・ルート相対で存在確認する
4. ヒットを明示し、1 件なら採用、0 件なら推測読みしない

## 入力の読み方

1. **参照文字列**: `{assets}/` 以降をサフィックスとする（例: `{assets}/template.md` → `template.md`）
2. **候補ディレクトリ**: 同じファイルから、次の順で集める（重複は先勝ちで 1 回にまとめる）
   1. 本文の `## アセットディレクトリ`（または同等見出し `## assets` / `### assets`）直下の箇条書き
   2. frontmatter の `metadata.assets`（旧形式・互換用）
   * プレーン文字列: そのままディレクトリパス
   * Markdown リンク `[label](path)`: `path` をディレクトリパスとして使う
   * インラインコード `` `path` ``: 中身をディレクトリパスとして使う
3. **基準ファイル**: `{assets}/` が書かれているファイル自身（`SKILL.md` / `.prompt.md` / `.cursor/commands/*.md` など）

候補ディレクトリを読んだら、必ず **サフィックスを結合**する（ディレクトリ一覧だけでは実ファイルにならない）。
例: 候補 `../assets/` + 参照 `{assets}/coding/design.md` → `../assets/coding/design.md`。

`## アセットディレクトリ` が無く `metadata.assets` だけの文書、またはその逆でも解決してよい。両方ある場合は本文セクションを先に試し、続けて metadata を試す。

## 解決手順

各候補ディレクトリについて、次の **2 基準**で候補を作る（どちらも試す）。

1. **文書相対**: `dirname(基準ファイル) / assets候補 / サフィックス`
2. **ワークスペース（リポジトリ）ルート相対**: `$(git rev-parse --show-toplevel) / assets候補 / サフィックス`

存在するファイル（またはディレクトリ）を **ヒット**として列挙する。重複パスは 1 回にまとめる。

* ヒットが 1 件 → それを実体として使う
* ヒットが複数 → すべて示し、利用側が選べるようにする。非対話で 1 つに決める必要がある場合は、候補の列挙順で最初にヒットしたものを採用する（文書相対とルート相対の両方ヒットした同一エントリでは文書相対を先とする）
* ヒットが 0 件 → 試した候補パス一覧とルールを報告し、推測読みはしない

## 実例（`github.create-pull-request`）

本文（要約）:

```markdown
## アセットディレクトリ

* `../assets/github.create-pull-request/`
* `apm_modules/eaglesakura/agent-skills/packages/ohitorisama/.apm/assets/github.create-pull-request/`
```

互換の frontmatter がある場合（任意）:

```yaml
metadata:
  assets:
    - "[github.create-pull-request/](../assets/github.create-pull-request/)"
    - apm_modules/eaglesakura/agent-skills/packages/ohitorisama/.apm/assets/github.create-pull-request/
```

本文参照: `{assets}/template.md`

基準ファイルがパッケージソースの `.apm/prompts/github.create-pull-request.prompt.md` のとき、主な候補は次になる。

```text
# 文書相対 × 1件目
.apm/prompts/../assets/github.create-pull-request/template.md
  → .apm/assets/github.create-pull-request/template.md

# ルート相対 × 2件目（利用者が apm install した場合）
apm_modules/eaglesakura/agent-skills/packages/ohitorisama/.apm/assets/github.create-pull-request/template.md
```

```bash
ROOT="$(git rev-parse --show-toplevel)"
SOURCE_MD="path/to/github.create-pull-request.prompt.md"  # または展開後の .cursor/commands/...
SUFFIX="template.md"

# ## アセットディレクトリ または metadata.assets から取り出した DIR 候補ごとに:
for DIR in \
  "../assets/github.create-pull-request" \
  "apm_modules/eaglesakura/agent-skills/packages/ohitorisama/.apm/assets/github.create-pull-request"
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

## 書き手向けメモ

* 本文・関連ファイルにはインストール先の絶対的な 1 パスだけを書かず、`{assets}/...` を使う
* 探索先は本文の `## アセットディレクトリ` に **ソース相対**（開発時）と **install 後ルート相対**（利用者ワークスペース）を並べる
* 新規・改訂では `metadata.assets` に寄せず、本文セクションを正とする（APM が frontmatter の `metadata` を落とすターゲットでも本文が残る）
* 旧文書の `metadata.assets` だけでも本 SKILL は解決できる
* slash-command の書き方は `tool-command-creator` を参照する

## ナレッジベース

### DO: `{assets}/` は先に候補ディレクトリ一覧を読む

* 通常の相対パス解決やリテラルな `{assets}` フォルダ探索に落とさない

### DO: 全候補を試し、ヒットを明示する

* install 前後で生きるパスが違うため、1 候補だけで決め打ちしない
* 本文 `## アセットディレクトリ` を先に、無ければ／続けて `metadata.assets` を読む

### DO NOT: `{assets}/` をリテラルなディレクトリ名だと思い込む

* `{assets}` はメタ変数であり、ディスク上のフォルダ名ではない

### DO NOT: 解決失敗時に推測読みする

* 候補とルールを示し、存在しないパスを開かない
