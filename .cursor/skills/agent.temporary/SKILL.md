---
name: agent.temporary
description: >-
  AI Agent が一時ファイル・実行計画・調査メモを置く場所（`.ai-agent/`）を規定する SKILL。
  一時スクリプト（*.sh/*.py/*.ts）、テンポラリ出力、計画ドキュメント、調査結果、チャット引き継ぎメモを作成・保存するときは必ず従う。
  「一時ファイルをどこに置くか」「plan/memory/tmp の使い分け」「`.ai-agent` を新規作成する」場面でもロードする。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# AI Agent / Temporary

AI Agent の作業成果のうち、リポジトリ本体にコミットしない一時成果物は、すべて `.ai-agent/` 配下に集約する。
散在すると後続チャットや他 Agent が発見できず、gitignore 漏れのリスクも上がるためである。

## いつ使うか

* 一時スクリプト・ログ・抽出結果・下書き Markdown を書くとき
* 実行計画（要件・詳細設計・実装手順）を `.md` で残すとき
* 調査結果や会話サマリを後続で再利用するとき（中身の書き方は `agent.memory.save`）
* リポジトリに `.ai-agent/` がまだ無いとき

## `.ai-agent/` の場所

* ディレクトリ名は **`.ai-agent/`（単数形）** のみを使う
* 未作成なら作成してよい。ひな形は [assets/.ai-agent/](./assets/.ai-agent/) をコピーする
* 実パスの解決順は `resolve-file-path` に従う（HQ では `headquarters/.ai-agent` を優先）

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

* `.ai-agent/` 配下は ignore し、コミット対象から外す（assets 内の `.gitignore` をそのまま使う）

## サブディレクトリの使い分け

| パス | 用途 |
| --- | --- |
| `.ai-agent/tmp/` | タスク用の使い捨てファイル（`*.sh` `*.py` `*.ts` `*.md` `*.txt` など） |
| `.ai-agent/plan/` | 実行中・レビュー中の計画ファイル（`*.md`） |
| `.ai-agent/plan/done/` | 完了した計画の保管先 |
| `.ai-agent/memory/` | 会話コンテキスト・調査結果の Memory（書き方は `agent.memory.save`） |
| `.ai-agent/memory/done/` | 用済み Memory の保管先 |

### `.ai-agent/tmp/`

* プロダクションコードや `docs/` に置かず、ここに書く
* 機密・大きなバイナリもここに閉じ込める（ルート `.gitignore` で除外される想定）

### `.ai-agent/plan/`

* 計画は `*.md` のみ
* 完了後は `plan/done/` へ移してよい

### `.ai-agent/memory/`

* 保存フォーマット・更新方針は `agent.memory.save` に委譲する
* パスだけはこの SKILL の規定に従う

## 新規作成手順

1. 上記の解決順で既存 `.ai-agent/` を探す
2. 無ければ [assets/.ai-agent/](./assets/.ai-agent/) をリポジトリ側の採用パスへコピーする
3. `tmp/` `plan/` `memory/`（および各 `done/`）が揃っていることを確認する
