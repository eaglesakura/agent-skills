---
name: workspace-agent-temporary
description: >-
  一時ファイルが必要な作業で、配置先（`.ai-agent/` 配下のどれか）を提案する SKILL。
  一時スクリプト（*.sh/*.py/*.ts）、テンポラリ出力、計画ドキュメント、調査下書きを
  「どこに書くか」決めるときは必ず従う。
  「plan/memory/tmp の使い分け」「このメモは tmp？ memory？」でもロードする。
  ワークスペース全体の推奨レイアウトや `.ai-agent/` ひな形の導入は workspace-layout、
  Memory 本文の書き方は workspace-agent-memory-save。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# Workspace / Agent Temporary

一時成果物が必要な作業では、置き場を先に決めてから書く。
ルート直下や `docs/`・プロダクションコードへ散らすと、後続 Agent が発見できず ignore 漏れも増える。

**全体の箱（推奨レイアウト・`.ai-agent/` ひな形）** は `workspace-layout` が担う。
本 SKILL は、その箱の中で **いまの作業ファイルをどこに置くか** を提案する。

## いつ使うか

* 一時スクリプト・ログ・抽出結果・下書き Markdown を書くとき
* 実行計画（要件・詳細設計・実装手順）を `.md` で残すとき
* 「このファイルは tmp / plan / memory のどれ？」と迷ったとき

## いつ使わないか

* リポジトリ全体の推奨構成・不足ディレクトリの導入 → `workspace-layout`
* Memory の見出し構成・テンプレート本文 → `workspace-agent-memory-save`

## 前提: `.ai-agent/` の実パス

* ディレクトリ名は **`.ai-agent/`（単数形）** のみ
* 無ければ `workspace-layout` に従いひな形を導入する（本 SKILL はひな形アセットを持たない）
* 実パスの解決順は `workspace-resolve-file-path`（HQ では `headquarters/.ai-agent` を優先）

```bash
ROOT="$(git rev-parse --show-toplevel)"
for candidate in \
  "${ROOT}/headquarters/.ai-agent" \
  "${ROOT}/.ai-agent"; do
  if [ -d "$candidate" ]; then
    AI_AGENT_DIR="$candidate"
    break
  fi
done
```

## 配置先の提案（サブディレクトリ）

| パス | この作業向けの用途 |
| --- | --- |
| `.ai-agent/tmp/` | タスク用の使い捨てファイル（`*.sh` `*.py` `*.ts` `*.md` `*.txt` など） |
| `.ai-agent/plan/` | 実行中・レビュー中の計画ファイル（`*.md`） |
| `.ai-agent/plan/done/` | 完了した計画の保管先 |
| `.ai-agent/memory/` | 会話コンテキスト・調査結果の Memory（書き方は `workspace-agent-memory-save`） |
| `.ai-agent/memory/done/` | 用済み Memory の保管先 |

### `.ai-agent/tmp/`

* プロダクションコードや `docs/` に置かず、ここに書く
* 機密・大きなバイナリもここに閉じ込める（ルート `.gitignore` で除外される想定）

### `.ai-agent/plan/`

* 計画は `*.md` のみ
* 完了後は `plan/done/` へ移してよい

### `.ai-agent/memory/`

* 「再利用したい結論・判断材料」があるとき。フォーマットは `workspace-agent-memory-save`
* 使い捨て下書きだけなら `tmp/` で足りる

## 作業手順

1. 書く成果物の種類（使い捨て / 進行中計画 / 再利用 Memory）を判別する
2. 上表で配置先を決める。`.ai-agent/` が無ければ先に `workspace-layout` で導入する
3. ファイルを作成し、採用したパスを報告する
