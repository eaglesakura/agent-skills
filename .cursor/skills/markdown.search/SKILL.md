---
name: markdown.search
description: ワークスペース内のドキュメント内容を検索・把握するSKILL。ワークスペース内のドキュメント検索に特化している。コード提案、レビュー等、積極的にこのSKILLを使用し、ナレッジを把握する。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# ドキュメント検索

* ワークスペース内のドキュメント（主に各リポジトリの `**/docs/**/*.md` ディレクトリ内）の構造は、基本的に次の内容に統一されている
* 検索結果を確認し、必要に応じて完全な文書をロードする

## ドキュメントの基本的な配置

リポジトリルート(.gitディレクトリの配置されたディレクトリ) からの相対パスで、下記のディレクトリ/ファイルを優先する

* `docs/`
* `README.md`
* `.cursor/skills/`
* `.ai-agent/memory/`

## ドキュメント把握手順

1. レベル2以上のヘッダから概要を調査
    * レベル2以上のヘッダを確認することで、ドキュメント全体の大まかな内容と関連性を把握する

    ```bash
    grep -rH -E '^(# |## |### |#### )' --include='*.md' path/to/directory

    # 実行例
    grep -rH -E '^(# |## |### |#### )' --include='*.md' .cursor/skills
    grep -rH -E '^(# |## |### |#### )' --include='*.md' docs
    ```

2. 実際のドキュメントを読み込み、詳細内容を把握
    * 詳細はドキュメントを直接読み込む
    * ヘッダは関連性の推測に使用し、内容は直接ドキュメントを参照する

3. `.cursor/skills/` 配下のドキュメントは、ファイルパスからSKILL名が抽出できる。関連性が高いドキュメントに一致するSKILLは、必要に応じて追加ロードを行う。
    * `.cursor/skills/{SKILL名}/SKILL.md`
    * `.cursor/skills/{SKILL名}/**/*.md`

## ナレッジベース把握

* コーディングや設計を行う際は、 `### DO:` で始まるヘッダを検索し、積極的に従う
* レビューを行う際は、 `### DO NOT:` で始まるヘッダを検索し、積極的に指摘する

```bash
# DO（コーディング・設計時）
grep -rH -E '^### DO:' --include='*.md' path/to/directory

# DO NOT（レビュー時）
grep -rH -E '^### DO NOT:' --include='*.md' path/to/directory

# 実行例
grep -rH -E '^### DO:' --include='*.md' .cursor/skills
grep -rH -E '^### DO NOT:' --include='*.md' .cursor/skills
grep -rH -E '^### DO:' --include='*.md' docs
grep -rH -E '^### DO NOT:' --include='*.md' docs

# DO / DO NOT をまとめて抽出する場合
grep -rH -E '^### DO( NOT)?:' --include='*.md' path/to/directory
```
