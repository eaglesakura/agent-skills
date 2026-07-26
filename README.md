# eaglesakura/agent-skills

## このリポジトリについて

* @eaglesakura が個人開発時に使用する SKILL や Sub Agent 等の AI Agent 設定集である
* 基本的に @eaglesakura 個人の開発者としての宗教観・設計・趣味に基づいている

## プロンプトの実装方針

* すべて日本語で記載されており、Token 数の最適化については考慮されていない
* プロントはCursor + Autoの課金体系に基づき最適化されている

## Quick Start

* [microsoft/apm](https://github.com/microsoft/apm) によるパッケージ導入をサポートしている
* 必要なpackageもしくはSKILLのみを選択して導入することが可能
* 各パッケージの SKILL・Command・Sub Agent の詳細は、パッケージごとの README を参照する。

| パッケージ | パス | 依存の書き方 |
| --- | --- | --- |
| `agent-creator` | [`packages/agent-creator`](packages/agent-creator) | `eaglesakura/agent-skills/packages/agent-creator` |
| `armyknife` | [`packages/armyknife`](packages/armyknife) | `eaglesakura/agent-skills/packages/armyknife` |
| `coding-xm3` | [`packages/coding-xm3`](packages/coding-xm3) | `eaglesakura/agent-skills/packages/coding-xm3` |
| `cursor-extensions` | [`packages/cursor-extensions`](packages/cursor-extensions) | `eaglesakura/agent-skills/packages/cursor-extensions` |
| `flutter` | [`packages/flutter`](packages/flutter) | `eaglesakura/agent-skills/packages/flutter` |
| `github` | [`packages/github`](packages/github) | `eaglesakura/agent-skills/packages/github` |
| `golang` | [`packages/golang`](packages/golang) | `eaglesakura/agent-skills/packages/golang` |
| `machine` | [`packages/machine`](packages/machine) | `eaglesakura/agent-skills/packages/machine` |
| `ohitorisama` | [`packages/ohitorisama`](packages/ohitorisama) | `eaglesakura/agent-skills/packages/ohitorisama` |

```yaml
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/agent-creator
    - eaglesakura/agent-skills/packages/armyknife
    - eaglesakura/agent-skills/packages/coding-xm3
    - eaglesakura/agent-skills/packages/cursor-extensions
    - eaglesakura/agent-skills/packages/flutter
    - eaglesakura/agent-skills/packages/github
    - eaglesakura/agent-skills/packages/golang
    - eaglesakura/agent-skills/packages/machine
    - eaglesakura/agent-skills/packages/ohitorisama
```

| パッケージ | 用途 | README |
| --- | --- | --- |
| `agent-creator` | SKILL・slash-command・Sub Agent の作成・改訂 | [packages/agent-creator/README.md](packages/agent-creator/README.md) |
| `armyknife` | 汎用開発向けユーティリティ（Markdown・ワークスペース等） | [packages/armyknife/README.md](packages/armyknife/README.md) |
| `coding-xm3` | 要件定義・詳細設計・実施を効率的に行うAI Agentフロー | [packages/coding-xm3/README.md](packages/coding-xm3/README.md) |
| `cursor-extensions` | Cursor 固有の運用（Claude Code CLI → Cursor Agent CLI 置換等） | [packages/cursor-extensions/README.md](packages/cursor-extensions/README.md) |
| `flutter` | Flutter / Dart 向け SKILL（規約・Layered Architecture・デバッグ等） | [packages/flutter/README.md](packages/flutter/README.md) |
| `github` | GitHub 運用（Actions 依存のセキュリティ等） | [packages/github/README.md](packages/github/README.md) |
| `golang` | Go 向け SKILL（規約・fmt / lint / test 等） | [packages/golang/README.md](packages/golang/README.md) |
| `machine` | ローカルマシン運用（ディスク占有・キャッシュ調査等） | [packages/machine/README.md](packages/machine/README.md) |
| `ohitorisama` | 個人開発向け（GitHub Pull Request 作成コマンド等） | [packages/ohitorisama/README.md](packages/ohitorisama/README.md) |
