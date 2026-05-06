---
name: parse.url-to-metadata
description: URLからメタデータをパースするためのSKILL. タスクIDやタイトル等、URLから取得可能な情報を整理する
license: MIT License
metadata:
  author: @eaglesakura
---
# メタデータ取得 / URL

## メタデータ一覧

* タスクID
  * タスクを一意に識別するID
  * 同一リポジトリにおいて重複しないが、リポジトリをまたぐと重複する可能性がある
* タイトル
  * タスクの内容を表した1行の文字列

## `https://github.com/{オーナー}/{リポジトリ名}/issues/{Issue番号}`

```bash
gh issue view {Issue番号} --repo {オーナー}/{リポジトリ名} --json number,title
```

```json
{
  "number": 261,
  "title": "（実際のIssueタイトル）"
}
```

* [ ] タスクID
  * `number` プロパティを使用する
  * `#` 等のPrefixを含まず、単純な数値となる
* [ ] タイトル
  * `title` プロパティを使用する
