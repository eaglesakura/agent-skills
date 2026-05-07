---
name: flutter.maintenance.check-latest-version
description: Flutter自体の最新バージョンの調査を行うためのSKILL
license: MIT License
metadata:
  author: "@eaglesakura"
---

# Flutter / 最新バージョン調査

## バージョン一覧取得

[flutter/flutter](https://github.com/flutter/flutter)

* リポジトリの `tag` 一覧から、リリース済みのバージョンを取得できる
* 必要に応じてgrepして対象メジャーバージョンを絞る等の対応を行う

```bash
# 一覧を取得
gh api repos/flutter/flutter/tags --paginate --jq '.[].name'

# バージョンを3.xに絞る
gh api repos/flutter/flutter/tags --paginate --jq '.[].name' | rg '^3\.'
```

## 各リリースバージョンごとの変更サマリを取得

* [CHANGELOG](https://github.com/flutter/flutter/blob/master/CHANGELOG.md) を取得する
  * `master` ブランチから取得すれば、Stableバージョンの直近リリース済み情報は満たされる
  * 各バージョンを個別に取得する必要はない
* `flutter --version` で取得した現在のバージョンと、対象バージョンの差分を確認する
