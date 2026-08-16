# coding-security

モバイル／バックエンド／GCP／Firebase のセキュリティナレッジ SKILL を提供する。

公式・OWASP 等を蒸留した同梱 `references/` を、`markdown-search` の段階ロードで引き、
要件定義での DO 提案とコード／設計レビューでの DO NOT 監査に使う。
`agentic-workspace`（`markdown-search` / `markdown-documentation`）と
`coding-xm3`（Coding-Commands / 要件・設計 SKILL）に依存する。

## Quick Start

```yaml
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/agentic-workspace
    - eaglesakura/agent-skills/packages/coding-xm3
    - eaglesakura/agent-skills/packages/coding-security
```

```yaml
# SKILL だけ導入（仮想サブディレクトリ）
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/coding-security/.apm/skills/mobile-security-knowledge
```

SKILL 単体導入時も、本文が参照する `markdown-search` / Coding-Commands 系を使うなら
`agentic-workspace` と `coding-xm3` を別途入れる。

## 依存 APM Package

* `eaglesakura/agent-skills/packages/agentic-workspace`
* `eaglesakura/agent-skills/packages/coding-xm3`

## SKILLS

※ `.apm/skills/` 配下。

### mobile-security-knowledge

* セキュリティ条文の正本は同梱 `references/`（SKILL Body には知識本文を持たない）
* `markdown-search` の Stage 1 → 2 → 3 で必要な節だけ Context に載せる
* 要件時は `### DO:` をセキュリティ／技術要件へ参照付きで提案する
* レビュー時は関連 `### DO NOT:` を残さない（必須指摘）
* 対象領域の目安: Android / iOS / OWASP MAS・MASTG / Google Cloud / Firebase

第三者著作物の帰属・ライセンスは SKILL 内 `assets/LICENSE.md` を参照する。

## Commands

なし。

## Sub Agents

なし。
