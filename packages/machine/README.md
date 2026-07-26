# machine

ローカルマシン運用向け SKILL 集である。
ディスク占有調査など、開発マシンのメンテナンス手順をまとめる。

## Quick Start

```yaml
# 一括導入
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/machine
```

```yaml
# SKILL だけ導入（仮想サブディレクトリ）
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/machine/.apm/skills/maintenance-measure-cache-size
```

## SKILLS

※ `.apm/skills/` 配下（アルファベット順）。

### maintenance-measure-cache-size

* ローカル PC の開発ツールキャッシュ占有を調査し、大きなディレクトリを一覧する。
* パス・GiB・用途・復元不足・削除コマンドなどの出力フォーマットを規定する。
* OS ごとの探索対象ディレクトリとしきい値（例: 10GiB 超で深掘り）を SKILL 本文で示す。

## Commands

なし。

## Sub Agents

なし。
