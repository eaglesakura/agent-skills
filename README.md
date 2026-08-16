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

| パッケージ | 用途 | 依存の書き方 |
| --- | --- | --- |
| [`agent-creator`](packages/agent-creator/README.md) | SKILL・slash-command・Sub Agent の作成・改訂 | `eaglesakura/agent-skills/packages/agent-creator` |
| [`agentic-workspace`](packages/agentic-workspace/README.md) | AI Agentに最適化したワークスペースの構築・運用 | `eaglesakura/agent-skills/packages/agentic-workspace` |
| [`coding-xm3`](packages/coding-xm3/README.md) | 要件定義・詳細設計・実施を効率的に行うAI Agentフロー | `eaglesakura/agent-skills/packages/coding-xm3` |
| [`coding-security`](packages/coding-security/README.md) | モバイル／GCP／Firebase のセキュリティナレッジ（DO 提案・DO NOT 監査） | `eaglesakura/agent-skills/packages/coding-security` |
| [`connect-rpc`](packages/connect-rpc/README.md) | Connect RPC 向け（`buf curl` による Unary 検証等） | `eaglesakura/agent-skills/packages/connect-rpc` |
| [`cursor-extensions`](packages/cursor-extensions/README.md) | Cursor 固有の運用（Claude Code CLI → Cursor Agent CLI 置換等） | `eaglesakura/agent-skills/packages/cursor-extensions` |
| [`flutter`](packages/flutter/README.md) | Flutter / Dart 向け SKILL（規約・Layered Architecture・デバッグ等） | `eaglesakura/agent-skills/packages/flutter` |
| [`github`](packages/github/README.md) | GitHub 運用（Actions 依存のセキュリティ、Issue URL メタデータ等） | `eaglesakura/agent-skills/packages/github` |
| [`golang`](packages/golang/README.md) | Go 向け SKILL（規約・fmt / lint / test 等） | `eaglesakura/agent-skills/packages/golang` |
| [`machine`](packages/machine/README.md) | ローカルマシン運用（ディスク占有・キャッシュ調査等） | `eaglesakura/agent-skills/packages/machine` |
| [`ohitorisama`](packages/ohitorisama/README.md) | 個人開発向け（PR 作成・ブランチ命名等） | `eaglesakura/agent-skills/packages/ohitorisama` |

```yaml
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/agent-creator
    - eaglesakura/agent-skills/packages/agentic-workspace
    - eaglesakura/agent-skills/packages/coding-xm3
    - eaglesakura/agent-skills/packages/coding-security
    - eaglesakura/agent-skills/packages/connect-rpc
    - eaglesakura/agent-skills/packages/cursor-extensions
    - eaglesakura/agent-skills/packages/flutter
    - eaglesakura/agent-skills/packages/github
    - eaglesakura/agent-skills/packages/golang
    - eaglesakura/agent-skills/packages/machine
    - eaglesakura/agent-skills/packages/ohitorisama
```
