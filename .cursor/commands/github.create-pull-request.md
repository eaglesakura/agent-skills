# Github / Pull Requestを作成する

* Branchでの作業を完了させ、Pull Requestを発行する

## 入力

### オプション: 対象リポジトリ

* 指定されない場合、現在のリポジトリの `origin` を対象リポジトリとする

### オプション: baseブランチ

* 指定しない場合は `origin/main` となる

### オプション: 既存Pull Request URL

* 指定のPull Request本文を上書きする場合に使用する
* 指定しない場合は新規に作成する

## 作業手順

1. 作業ブランチ名を特定する

    ```bash
    # 例
    git rev-parse --abbrev-ref HEAD
    ```

2. 差分を特定する

    ```bash
    # コミットログから整理
    git log origin/main..HEAD --oneline

    # 差分から整理
    git diff origin/main HEAD
    ```

3. [Pull Requestテンプレート](../extra/github.create-pull-request/template.md) を使用してPR本文を作成する
    * テキストは日本語で記載する
    * 規定された一時ファイル置き場に保存し、作業完了後に削除する

4. ghコマンドでpull request作成もしくは更新を行う

    ```bash
    # 新規作成（base はオプション指定時のみ。省略時はリモートのデフォルトブランチ）
    gh pr create --title "{PRタイトル}" --body-file path/to/body.md

    gh pr create --base main --title "{PRタイトル}" --body-file path/to/body.md

    # 既存 Pull Request の本文を上書き（PR 番号または URL）
    gh pr edit 123 --body-file path/to/body.md

    gh pr edit https://github.com/OWNER/REPO/pull/123 --body-file path/to/body.md
    ```

5. 作業レポートを出力する

```markdown
# {Pull Requestタイトル}

{Pull Request Body内容}

---
Repository: {https://path/to/repository}
Pull Request: [{#PR番号} {タイトル}]({PRへのリンク})
```
