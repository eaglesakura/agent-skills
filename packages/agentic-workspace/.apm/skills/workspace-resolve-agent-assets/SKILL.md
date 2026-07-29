---
name: workspace-resolve-agent-assets
description: >-
  ドキュメント内の `{assets}/...` メタ変数だけを実ファイルパスへ解決する SKILL。
  本文 `## アセットディレクトリ`（`## assets` / `### assets` も可）と互換の
  `metadata.assets` から候補を集め、文書相対とリポジトリルート相対の両方で探す。
  候補に `*` / `**` ワイルドカードがあれば展開して複数ディレクトリを探す
  （例: `apm_modules/**/coding-xm3/.apm/assets/`）。
  「`{assets}/template.md` の実体」「アセットを解決してからロード」
  「APM の template を開いて」「アセットディレクトリから読んで」
  「apm_modules の glob でアセットを探して」では必ず使う。
  通常の path/to/file・Markdown リンク・`.ai-agent/` は workspace-resolve-file-path、
  URL メタデータは workspace-resolve-url-metadata を使う（混同しない）。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# Workspace / Resolve Agent Assets

APM などでインストール先が変わっても参照を保てるよう、アセットは **メタ変数** `{assets}/` で書く。
本 SKILL はその表記を、文書に書かれた候補ディレクトリから実パスへ落とす。
`apm install`・fork・`_local` 展開などで `apm_modules/` 配下が揺れる場合は、候補にワイルドカードを書いて複数レイアウトを一度に拾う。

## いつ使うか

* コマンド / SKILL 本文や関連ファイルに `{assets}/template.md` のように書かれているとき
* パッケージソースと `apm_modules/` 展開先の両方に同じアセットがあり得るとき
* `apm_modules/**/package-name/...` のように install 先が揺れる候補を解決するとき
* 「アセットを解決してから読んで」「`{assets}/` の実体はどこ？」と聞かれたとき

## いつ使わないか

* クォート相対 `path/to/file`、Markdown リンク `[text](rel)`、`.ai-agent/` の場所決め → `workspace-resolve-file-path`
* GitHub Issue URL から ID/タイトルを取る → `workspace-resolve-url-metadata`
* キーワードで文書を探すだけ → `markdown-search`

## 作業手順

1. 参照文字列からサフィックスを取る
2. 基準ファイルから候補ディレクトリ一覧を集める
3. 各候補について、リテラルならそのまま・ワイルドカードなら展開し、文書相対・ルート相対で存在確認する
4. ヒットを明示し、1 件なら採用、0 件なら推測読みしない

## 入力の読み方

1. **参照文字列**: `{assets}/` 以降をサフィックスとする（例: `{assets}/template.md` → `template.md`）
2. **候補ディレクトリ**: 同じファイルから、次の順で集める（重複は先勝ちで 1 回にまとめる）
   1. 本文の `## アセットディレクトリ`（または同等見出し `## assets` / `### assets`）直下の箇条書き
   2. frontmatter の `metadata.assets`（旧形式・互換用）
   * プレーン文字列: そのままディレクトリパス（または glob パターン）
   * Markdown リンク `[label](path)`: `path` をディレクトリパス（または glob）として使う
   * インラインコード `` `path` ``: 中身をディレクトリパス（または glob）として使う
3. **基準ファイル**: `{assets}/` が書かれているファイル自身（`SKILL.md` / `.prompt.md` / `.cursor/commands/*.md` など）

候補ディレクトリを読んだら、必ず **サフィックスを結合**する（ディレクトリ一覧だけでは実ファイルにならない）。
例: 候補 `../assets/` + 参照 `{assets}/coding/design.md` → `../assets/coding/design.md`。

`## アセットディレクトリ` が無く `metadata.assets` だけの文書、またはその逆でも解決してよい。両方ある場合は本文セクションを先に試し、続けて metadata を試す。

## ワイルドカード（glob）

候補文字列に `*` または `**` が含まれる場合は、**ディレクトリの glob** として展開してからサフィックスを結合する。

| 記号 | 意味 |
| --- | --- |
| `*` | 1 パスセグメント内の任意文字列（`/` は跨がない） |
| `**` | 0 個以上のディレクトリ階層 |

例:

* `apm_modules/**/coding-xm3/.apm/assets/` → `_local/coding-xm3` でも `eaglesakura/.../packages/coding-xm3` でも拾う
* `apm_modules/*/agentic-workspace/.apm/assets/` → `apm_modules` 直下の 1 階層だけの別名に対応

展開ルール:

1. 文書相対ベース `dirname(基準ファイル)` と、リポジトリルートベースの **両方**で glob する
2. 各ベース内のマッチは **辞書順（パス文字列の昇順）** に並べ、決定的にする
3. 列挙順は「候補行の出現順 → 文書相対の展開結果 → ルート相対の展開結果」。重複パスは先勝ちで 1 回にまとめる
4. 展開結果が 0 件の候補行は miss として記録し、次の候補行へ進む（推測で別パスを足さない）

リテラル候補（ワイルドカード無し）は従来どおり、展開せず 1 パスとして扱う。

## 解決手順

各候補（リテラル、または glob 展開後の各ディレクトリ）について、次の **2 基準**で候補ファイルを作る。

1. **文書相対**: `dirname(基準ファイル) / assets候補 / サフィックス`
2. **ワークスペース（リポジトリ）ルート相対**: `$(git rev-parse --show-toplevel) / assets候補 / サフィックス`

存在するファイル（またはディレクトリ）を **ヒット**として列挙する。重複パスは 1 回にまとめる。

* ヒットが 1 件 → それを実体として使う
* ヒットが複数 → すべて示し、利用側が選べるようにする。非対話で 1 つに決める必要がある場合は、**列挙順の先勝ち**（文書相対をルート相対より先、同一基準内では辞書順）
* ヒットが 0 件 → 試した候補パス一覧とルールを報告し、推測読みはしない

## 実例（自 package 内の架空コマンド）

本文（要約）:

```markdown
## アセットディレクトリ

* `../assets/example.command/`
* `apm_modules/**/agentic-workspace/.apm/assets/example.command/`
```

互換の frontmatter がある場合（任意）:

```yaml
metadata:
  assets:
    - "[example.command/](../assets/example.command/)"
    - apm_modules/**/agentic-workspace/.apm/assets/example.command/
```

本文参照: `{assets}/template.md`

基準ファイルがパッケージソースの `.apm/prompts/example.command.prompt.md` のとき、主な候補は次になる。

```text
# 文書相対 × 1件目（リテラル）
.apm/prompts/../assets/example.command/template.md
  → .apm/assets/example.command/template.md

# ルート相対 × 2件目（glob。install / fork 先が揺れても拾う）
apm_modules/_local/agentic-workspace/.apm/assets/example.command/template.md
apm_modules/**/agentic-workspace/.apm/assets/example.command/template.md
```

```bash
ROOT="$(git rev-parse --show-toplevel)"
SOURCE_MD="path/to/example.command.prompt.md"  # または展開後の .cursor/commands/...
SUFFIX="template.md"
shopt -s globstar nullglob  # bash: ** と 0 件時の扱い

# ## アセットディレクトリ または metadata.assets から取り出した DIR 候補ごとに:
for DIR in \
  "../assets/example.command" \
  "apm_modules/**/agentic-workspace/.apm/assets/example.command"
do
  # リテラルか glob かで展開先を決める
  expanded=()
  if [[ "$DIR" == *[\*\?]* ]]; then
    # 文書相対 → ルート相対の順。各ベース内は辞書順
    doc_matches=( "$(dirname "$SOURCE_MD")"/$DIR )
    root_matches=( "$ROOT"/$DIR )
    # nullglob 時は配列に実マッチのみ。辞書順へ
    # （実装では printf '%s\n' ... | sort -u でも可）
    for base_match in "${doc_matches[@]}" "${root_matches[@]}"; do
      [ -e "$base_match" ] || continue
      expanded+=( "$base_match" )
    done
  else
    expanded=(
      "$(dirname "$SOURCE_MD")/${DIR}"
      "${ROOT}/${DIR}"
    )
  fi

  for CAND_DIR in "${expanded[@]}"; do
    CAND="${CAND_DIR%/}/${SUFFIX}"
    # 正規化して存在確認
    if [ -e "$CAND" ]; then
      echo "HIT: $CAND"
    else
      echo "miss: $CAND"
    fi
  done
done
```

Python で書く場合の目安（決定的な並び）:

```python
from pathlib import Path

def expand_dirs(pattern: str, bases: list[Path]) -> list[Path]:
    if any(ch in pattern for ch in "*?"):
        found: list[Path] = []
        for base in bases:
            found.extend(sorted(base.glob(pattern)))
        # 先勝ち dedupe
        seen: set[Path] = set()
        out: list[Path] = []
        for p in found:
            rp = p.resolve()
            if rp in seen:
                continue
            seen.add(rp)
            out.append(p)
        return out
    return [base / pattern for base in bases]
```

## 書き手向けメモ

* 本文・関連ファイルにはインストール先の絶対的な 1 パスだけを書かず、`{assets}/...` を使う
* 探索先は本文の `## アセットディレクトリ` に **ソース相対**（開発時）と **install 後ルート相対**（利用者ワークスペース）を並べる
* install 後パスは固定の `apm_modules/eaglesakura/.../packages/<pkg>/` より、**ワイルドカード推奨**（fork・`_local`・ネスト深さの揺れに耐える）
  * 推奨例: `apm_modules/**/<package-name>/.apm/assets/`
  * 避ける例（壊れやすい）: `apm_modules/**/<package-name>/.apm/assets/` のみ
* 新規・改訂では `metadata.assets` に寄せず、本文セクションを正とする（APM が frontmatter の `metadata` を落とすターゲットでも本文が残る）
* 旧文書の `metadata.assets` だけでも本 SKILL は解決できる
* slash-command 本体の書き方は、各プロジェクトの command 作成用 SKILL / テンプレートに従う

## ナレッジベース

### DO: `{assets}/` は先に候補ディレクトリ一覧を読む

* 通常の相対パス解決やリテラルな `{assets}` フォルダ探索に落とさない

### DO: 全候補を試し、ヒットを明示する

* install 前後で生きるパスが違うため、1 候補だけで決め打ちしない
* 本文 `## アセットディレクトリ` を先に、無ければ／続けて `metadata.assets` を読む
* ワイルドカード候補は展開してからサフィックス結合する

### DO: install 後パスはワイルドカードで書く

* `apm_modules/**/<pkg>/...` なら `_local` と vendor ネストの両方を同じ行でカバーできる

### DO NOT: `{assets}/` をリテラルなディレクトリ名だと思い込む

* `{assets}` はメタ変数であり、ディスク上のフォルダ名ではない

### DO NOT: 解決失敗時に推測読みする

* 候補とルールを報告し、存在しないパスを開かない
* glob が 0 件でも、勝手に別パッケージ名へ読み替えない
