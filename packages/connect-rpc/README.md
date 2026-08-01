# connect-rpc

Connect RPC 向け SKILL 集である。
Unary HTTP サービスの `buf curl` による検証手順をまとめる。

## Quick Start

```yaml
# 一括導入
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/connect-rpc
```

```yaml
# SKILL だけ導入（仮想サブディレクトリ）
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/connect-rpc/.apm/skills/connect-rpc-curl
```

## SKILLS

※ `.apm/skills/` 配下（アルファベット順）。

### connect-rpc-curl

* Connect RPC（Unary）の HTTP サービスを `buf curl` で呼び出す。
* `*.proto` の rpc / message から JSON リクエストを組み立て、`--protocol connect` でコールする。
* スキーマ（`buf.yaml`）・ホスト・Path 接頭辞はワークスペースのレイアウト指示から解決する。

## Commands

なし。

## Sub Agents

なし。
