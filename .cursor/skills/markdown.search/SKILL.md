---
name: markdown.search
description: >-
  ワークスペース内の Markdown ドキュメントを検索・概要把握する SKILL。
  「docs を調べて」「DO / DO NOT を探して」「関連ドキュメントを把握してから実装／レビュー」、
  コーディング・設計・レビュー前のナレッジ収集時は積極的に使う。
  文書を新規に書く作業は markdown.documentation、lint 修正は markdown.fix。
  Memory の中身を保存する作業は agent.memory.save。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# ドキュメント検索

実装やレビューの前に、既存の `DO` / 構成ドキュメントを拾うための SKILL である。
全文をいきなり読まず、見出しで当たりをつけてから必要なファイルだけロードする。

## いつ使うか

* コーディング・詳細設計・レビューの前にナレッジを集めたいとき
* 「どこに書いてあるか」を探すとき
* `### DO:` / `### DO NOT:` を横断したいとき

## 優先して見る配置

リポジトリルート（`.git` があるディレクトリ）からの相対パス:

* `docs/`
* `README.md`
* `.cursor/skills/`
* `.ai-agent/memory/`（場所は `agent.temporary` に従う）

## 把握手順

### 1. 見出しで概要を取る

レベル2以上のヘッダから関連性を推測する。

```bash
grep -rH -E '^(# |## |### |#### )' --include='*.md' path/to/directory
```

### 2. 必要な本文だけ読む

* ヘッダは当たり付け、中身は該当ファイルを直接読む
* 無関係な全文ロードは避ける

### 3. SKILL ドキュメントの追加ロード

`.cursor/skills/{SKILL名}/SKILL.md` および配下 `*.md` がヒットしたら、関連 SKILL を必要に応じてロードする。

## ナレッジベース（DO / DO NOT）

* コーディング・設計時: `### DO:` を検索し従う
* レビュー時: `### DO NOT:` を検索し指摘に使う

```bash
grep -rH -E '^### DO:' --include='*.md' path/to/directory
grep -rH -E '^### DO NOT:' --include='*.md' path/to/directory
grep -rH -E '^### DO( NOT)?:' --include='*.md' path/to/directory
```

## 出力の目安

* ヒットしたパスと見出しの一覧
* 採用すべき `DO` / 避けるべき `DO NOT` の要約
* 次に読むべきファイルの提案
