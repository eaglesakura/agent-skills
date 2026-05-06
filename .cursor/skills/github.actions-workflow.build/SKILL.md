---
name: github.actions-workflow.build
description: Github ActionsのWorkflow構築に関わるSKILL。守るべきセキュリティ上のプラクティスや、基本的なルールについて指示している。 `.github/**/*.yaml` の編集に際し、必ずロードする。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# Github / Github Actions / ワークフロー構築

* Github Actionsのワークフロー構築する際に守るべきSKILL

## Security / SHAによるアーティファクトバージョン固定

* Github Actionsで用いる外部ワークフローは、必ずSHAピン留を採用する

### DO

* `jdx/mise-action@{sha}` の使用を提案する
* `# {repo}@{version name}` をコメントとして付与することで、エンジニアが容易に確認できるようにする
* `gh` コマンドにより、実際にtagとして管理されているバージョンとSHAを取得する

```yaml
    # ハッシュ値が設定されており、アーティファクトが侵害された場合でも、侵害されたアーティファクトを利用してしまうリスクを最小限にできる
      - name: Setup mise
        uses: jdx/mise-action@{sha} # {repo}@{version name}
```

```bash
# 最新版 / バージョン一覧を取得するためのghコマンドの例
# 例: jdx/mise-action のタグ一覧 + 各タグが指すコミットSHAを取得
gh api repos/jdx/mise-action/git/matching-refs/tags \
  --jq '.[] | {tag: (.ref | sub("^refs/tags/"; "")), sha: .object.sha}'

# 最新Releaseのタグ名を取得
gh api repos/jdx/mise-action/releases/latest --jq '.tag_name'
```

### DO NOT

```yaml
    # バージョンが指定されており、サプライチェーンアタックの対象となる恐れがある
      - name: Setup mise
        uses: jdx/mise-action@v2
```
