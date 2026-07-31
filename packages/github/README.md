# github

GitHub 運用向け SKILL 集である。
Actions 依存のセキュリティ（SHA ピン留め等）、Issue URL からのメタデータ取得をまとめる。

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
    - eaglesakura/agent-skills/packages/github/.apm/skills/github-resolve-url-metadata
```

## SKILLS

※ `.apm/skills/` 配下（アルファベット順）。

### github-actions-dependencies-security

* GitHub Actions のワークフロー（`.github/**/*.yaml`）編集時に守るセキュリティ・運用ルールを規定する。
* 外部アクションは SHA ピン留めとし、`uses: org/action@tag` のような可変タグ指定を避ける。
* `gh api` 等でタグとコミット SHA を取得し、コメントで人間が追える形にする。

### github-resolve-url-metadata

* Issue URL 等からタスク ID・タイトルなど取得可能なメタデータを整理する。
* `gh issue view ... --json number,title` など CLI での取得例と JSON の読み方を示す。
* GitHub Issues の URL パターンごとのフィールド対応を SKILL 本文で規定する。

## Commands

なし。

## Sub Agents

なし。
