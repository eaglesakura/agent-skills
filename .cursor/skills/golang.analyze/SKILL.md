---
name: golang.analyze
description: Golangの静的解析やテスト、フォーマッタ適用等、品質担保を行うためのSKILL
license: MIT License
metadata:
  author: @eaglesakura
---
# Golangコード品質向上SKILL

* Golangのコード品質を向上させ、開発する上での様々なリスクを低減するためのSKILL
* AI Agentによるコーディング後や途中経過等、適切なタイミングでコールする

## Formatter

* フォーマッタは、AI Agentによるコーディング完了後に必ず実行する
* 結果はべき等であり、副作用はない

```bash
# go.workのディレクトリで実施する
go fmt ./...
```

## Analyzer

* Analyzerは、AI Agentによるコーディング完了後に必ず実行する
* 結果はべき等であり、副作用はない
* 提示された問題点は、非破壊的であれば自動的に実施する

```bash
golangci-lint run ./...
```

### ガードレール条項

* [ ] **ロジックの変更等、破壊的変更が生じる場合はユーザーに作業内容を提示するのみで、作業の実施は行わない**

## Unit Test

* ユニットテストは、AI Agentによるコーディング完了後に必ず実行する
* 結果はべき等であり、基本的に副作用はない
  * 外部のAPIをコールする場合等、環境・状況依存で失敗する場合がある
* Failした場合、エラー内容のみをユーザーに提示する
  * **修正は行わない**
* リポジトリが `//go:build` タグを使う場合は、`go test` に **`-tags={tags...}`** を付与する。`{tags...}` はプレースホルダであり、実行時にプロジェクトの方針どおりのカンマ区切りタグ（例: `dev,test`）へ置き換える。

```bash
# ビルドタグがプロジェクト方針で必要な場合は、{tags...} をカンマ区切りのタグ名に置き換えて -tags を付与する（例: dev,test）
# workspace全体のテスト（go.work があるリポジトリルートで実行）
go test -tags={tags...} ./...

# 個別: パッケージ（ディレクトリ）単位
go test -tags={tags...} ./path/to/module

# 個別: 特定のテスト関数のみ（-run は正規表現）
go test -tags={tags...} ./path/to/module -run '^TestExample$'
```
