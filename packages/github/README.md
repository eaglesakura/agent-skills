# github

GitHub 運用向け SKILL 集である。
Actions 依存のセキュリティ（SHA ピン留め等）をまとめる。

## Quick Start

```yaml
# 一括導入
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/github
```

```yaml
# SKILL だけ導入（仮想サブディレクトリ）
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/github/.apm/skills/github-actions-dependencies-security
```

## SKILLS

※ `.apm/skills/` 配下（アルファベット順）。

### github-actions-dependencies-security

* GitHub Actions のワークフロー（`.github/**/*.yaml`）編集時に守るセキュリティ・運用ルールを規定する。
* 外部アクションは SHA ピン留めとし、`uses: org/action@tag` のような可変タグ指定を避ける。
* `gh api` 等でタグとコミット SHA を取得し、コメントで人間が追える形にする。

## Commands

なし。

## Sub Agents

なし。
