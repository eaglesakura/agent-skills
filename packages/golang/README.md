# golang

Go 向け SKILL 集である。
コーディング規約と、`fmt` / `lint` / `test` などの品質担保手順をまとめる。

## Quick Start

```yaml
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/golang
```

## SKILLS

※ `.apm/skills/` 配下（アルファベット順）。

### golang-analyze

* Go のフォーマット・静的解析・テストなど、品質担保の実行タイミングとコマンドを規定する。
* `go fmt ./...`・`golangci-lint run ./...` 等をコーディング完了後に実行することを推奨する。
* `go.work` 起点のモジュール構成での実行場所にも言及する。

### golang-coding-rules

* `*.go` の実装・修正時に従うコーディング規約と実装パターンをまとめる。
* `references/general.md`・`data_object.md`・`code_comment.md` など文脈別ドキュメントを読み込む。
* データオブジェクト・公開 API のドキュメントコメントなど詳細ルールを参照で満たす。

## Commands

なし。

## Sub Agents

なし。
