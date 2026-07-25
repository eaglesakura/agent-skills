---
name: claude.alias-cursor
description: >-
  Claude Code CLI（`claude` / `claude -p` 等）の提案・記述・スクリプトを、未契約環境向けに
  Cursor Agent CLI（`agent` または `cursor agent`）へ置き換える SKILL。
  他 SKILL・ドキュメント・eval・CI・skill-creator の `run_loop` / `run_eval` が
  `claude` を出したら必ずロードし、実行前にバインディングへ変換する。
  「claude の代わり」「cursor agent」「agent -p」「Claude 未契約」「トリガー最適化」でも使う。
  IDE 起動だけの `cursor`（agent サブコマンドなし）、純粋な Cursor SDK 実装のみ、
  Claude 契約済みで本物の `claude` を使う明示指示がある場合は使わない。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# Claude → Cursor Agent CLI エイリアス

この環境では Claude Code（`claude`）は未契約である。他 SKILL や手順が `claude` を提案しても、**実行せず** [Cursor CLI](https://cursor.com/ja/cli) の Agent CLI に置き換える。

## エントリポイント（重要）

次の **どちらも Agent CLI** である（同等に使ってよい）。

| 呼び方 | 例 |
| --- | --- |
| `agent …` | `agent -p "…"` |
| `cursor agent …` | `cursor agent -p "…"` |

IDE を開くだけの `cursor`（サブコマンドなし）は Agent CLI **ではない**。置き換え先にしない。

スクリプトでは `CURSOR_AGENT_BIN`（未設定なら `cursor` または `agent`）を使うとよい。`cursor agent` を選ぶ場合は引数に `agent` サブコマンドを付ける。

## いつ使うか

* 他 SKILL / スクリプト / ドキュメントが `claude` や `claude -p` を指示したとき
* skill-creator の description 最適化（`scripts/run_loop` / `run_eval` / `improve_description`）が `claude -p` を呼ぶとき
* headless / CI / eval で Claude Code 相当の呼び出しが必要なとき
* ユーザーが「claude の代わりに cursor / cursor-cli / agent」と明示したとき

## 前提

1. `agent` または `cursor agent` が使えること（未導入なら `curl https://cursor.com/install -fsS | bash`）
2. 認証済みであること
   * 対話: `agent login` または `cursor agent login`（ブラウザ認証）
   * スクリプト / CI: `CURSOR_API_KEY`
3. headless（`-p`）ではワークスペース信頼が必要なことがある → `--trust` および／または `-f` / `--force`
4. 詳細対応表が必要なら [references/command-bindings.md](./references/command-bindings.md) を読む

### 認証の落とし穴

* `agent status` が成功に見えても、`agent -p` が Authentication required になることがある → `agent login` / `cursor agent login` をやり直すか `CURSOR_API_KEY` を使う
* `agent about` の User Email が Not logged in でも、別経路で login 済みのことがある → 最終確認は短い `-p` プローブ（例: `cursor agent -p --mode ask --trust -f "Reply OK"`）
* `NO_OPEN_BROWSER=1 agent login` はリンク待ちで止まりやすい。対話可能ならブラウザ付き login を使う

## 変換手順

1. 提案されたコマンド列から `claude` 呼び出しを抽出する
2. 下表（または references）で Agent CLI 相当へ置換する（`agent` または `cursor agent`）
3. headless なら `--trust` / `-f` の要否を足す
4. **バインディング不能**なら、実行せず代替を提示する（無理に近似しない）
5. 置換後コマンドを示す。実行が求められていれば Agent CLI 側を実行する

## コア 1:1 バインディング

表の Cursor 列は `agent` で書く。先頭を `cursor agent` にしても同じである。

| Claude Code | Cursor Agent CLI | 備考 |
| --- | --- | --- |
| `claude` | `agent` / `cursor agent` | 対話セッション開始 |
| `claude "query"` | `agent "query"` | 初期プロンプト付き起動 |
| `claude -p "query"` / `--print` | `agent -p "query"` / `--print` | headless。スクリプト・CI の定番 |
| `claude -c` / `--continue` | `agent --continue` または `agent resume` | 直前セッション継続 |
| `claude -r <id>` / `--resume <id>` | `agent --resume <id>` | セッション再開 |
| `claude update` | `agent update` | CLI 更新 |
| `claude auth login` | `agent login` / `cursor agent login` | 認証 |
| `claude auth logout` | `agent logout` | ログアウト |
| `claude auth status` | `agent status` / `agent whoami` | 認証状態（`-p` 成功が最終確認） |
| `claude mcp …` | `agent mcp …` | MCP 管理（サブコマンドは完全一致しない） |
| `claude mcp login <id>` | `agent mcp login <id>` | MCP OAuth |
| `claude plugin …` | `agent plugin …` | プラグイン（エコシステムは別） |
| `claude -v` / `--version` | `agent -v` / `--version` | バージョン |
| `--model <name>` | `--model <name>` | モデル ID 体系は別。`agent --list-models` で確認 |
| `--output-format text\|json\|stream-json` | 同左（`--print` 時） | 形式名は共通 |
| `--stream-partial-output` 相当 | `--stream-partial-output` | Cursor 側フラグ名 |
| `--add-dir <path>` | `--add-dir <path>` | 追加ワークスペースルート |
| `--plugin-dir <path>` | `--plugin-dir <path>` | ローカルプラグイン |
| `-w` / `--worktree` | `-w` / `--worktree` | git worktree 隔離実行 |
| `--dangerously-skip-permissions` | `-f` / `--force` / `--yolo` | 意図は近いが権限モデルは同一ではない |
| （非対話で trust プロンプト回避） | `--trust` | Claude 側に同名はない。headless でよく必要 |
| `--permission-mode plan` | `--mode plan` / `--plan` | 読み取り寄り・計画モード |
| （ask 相当） | `--mode ask` | 編集しない Q&A |
| `ANTHROPIC_API_KEY` | `CURSOR_API_KEY` | 環境変数の対応 |

### よく使う置換例

```bash
# Before (Claude Code — 実行しない)
claude -p "Analyze this repository" --output-format json

# After（どちらでも可）
agent -p --trust -f "Analyze this repository" --output-format json
cursor agent -p --trust -f "Analyze this repository" --output-format json
```

```bash
# ファイル変更を伴う headless
# Claude: claude -p --dangerously-skip-permissions "Refactor …"
agent -p --trust --force "Refactor …"
```

```bash
# CI
# Claude: ANTHROPIC_API_KEY=… claude -p "…"
CURSOR_API_KEY=… agent -p --trust -f "…"
```

## skill-creator / `claude -p` スクリプトの扱い

skill-creator の `scripts/run_eval.py`・`run_loop.py`・`improve_description.py` は内部で `claude -p` を呼ぶ。

* **コマンド置換だけ**では足りないことがある。Claude 側は stream-json 上の Skill / Read ツール呼び出しで「スキルが発火したか」を検知する。Cursor Agent のイベント形・ツール名は同じではない
* description トリガー最適化では、次の **近似プロトコル** が実用的である
  1. `cursor agent -p --mode ask --trust -f`（または `agent -p …`）に、スキル名＋ description ＋ユーザークエリを渡し `TRIGGER` / `SKIP` だけ答えさせる
  2. 失敗例を同じ headless 呼び出しで description 改善プロンプトに渡す
  3. train / holdout test で再評価し最良を SKILL.md に適用する
* 本 SKILL の [scripts/trigger_opt_cursor.py](./scripts/trigger_opt_cursor.py) がその実装である。`python -m scripts.run_loop` の代わりにこれを使う。新規に `claude -p` 依存スクリプトを書くときも、最初から Agent CLI 版にする

### `scripts/trigger_opt_cursor.py` の使い方

skill-creator の description 最適化（`run_loop`）相当を、Cursor Agent CLI で行う。

```bash
# 例: 対象 SKILL の description を TRIGGER/SKIP 評価で改善する
python path/to/claude.alias-cursor/scripts/trigger_opt_cursor.py \
  --eval-set /path/to/trigger-eval.json \
  --skill-path /path/to/target-skill \
  --results-out /path/to/results.json \
  --max-iterations 5 \
  --verbose

# 最良 description を SKILL.md に書き戻す場合
# …同じ引数に --apply-best を追加
```

* エントリポイントは環境変数 `CURSOR_AGENT_BIN`（既定 `cursor` → `cursor agent …`、`agent` なら直呼び）
* eval set は `[{"query":"…","should_trigger":true}, …]` 形式

## 近似対応（完全 1:1 ではない）

| Claude Code | Cursor 側の現実的な代替 | 注意 |
| --- | --- | --- |
| `--permission-mode ask` / 読み取り専用に近い運用 | `--mode ask` | Ask は編集しない |
| `claude doctor` | `agent about` + `agent status` + 短い `-p` プローブ | 診断範囲は狭い |
| `claude setup-token` | Dashboard で API Key 発行 → `CURSOR_API_KEY` | トークン生成コマンドは無い |
| `claude --cloud "…"` / Remote Control | Cloud Agent（メッセージ先頭 `&`）や [cursor.com/agents](https://cursor.com/agents) / `agent worker` | プロトコルも UX も別物 |
| `claude agents` / `attach` / `logs` / `stop` / `rm` / `respawn` / `daemon` | `agent ls` / `agent resume` / `agent create-chat`、または Cloud / worker | バックグラウンドセッション管理は互換ではない |
| `--json-schema` | `--output-format json` + プロンプトでスキーマ遵守を指示 | サーバ側スキーマ検証は無い |
| `--system-prompt` / `--system-prompt-file` / append 系 | プロンプト本文・Cursor Rules・SKILL に書く | CLI フラグとしての置換は不可 |
| `--allowedTools` / `--disallowedTools` / `--tools` | Cursor CLI の [permissions](https://cursor.com/docs/cli/reference/permissions) 設定 | フラグ 1:1 は不可 |
| `--chrome` | browser MCP / Maestro 等 | Agent CLI に Chrome 統合フラグは無い |
| `claude ultrareview` | Bugbot / security-review 系 SKILL、または `agent -p` でレビュー指示 | 専用コマンドは無い |
| `--workspace` 相当の cwd 固定 | `--workspace <path>` | 効かない・無視される場合がある。`cd` してから実行する方が確実なことがある |

## バインディング不能（実行しない）

次は Cursor Agent CLI に対応コマンドが無い。**`claude` をそのまま実行せず**、ユーザーに不能である旨と代替案を伝える。

| Claude Code | 理由 / 代替 |
| --- | --- |
| `claude gateway` | Anthropic 側セルフホスト gateway。代替なし |
| `claude project purge` | ローカル Claude 状態削除。代替なし（不要ならスキップ） |
| `claude auto-mode …` | Claude 固有の auto mode 設定。`--auto-review` は別物 |
| `--bare` / `--safe-mode` | 起動時コンテキスト削減の同等フラグなし。必要な制約はプロンプトと permissions で表現 |
| `--max-budget-usd` / `--max-turns` | コスト・ターン上限フラグなし。CI 側タイムアウト等で制御 |
| `--input-format stream-json` | stdin ストリーム入力プロトコルは互換前提にしない |
| `--fallback-model` / `--effort` / `--advisor` 等 | Claude 固有。モデルは `--model` と `agent models` で選ぶ |
| stream-json 上の Claude `Skill` ツール発火検知そのもの | Cursor ではイベント互換なし。TRIGGER/SKIP 分類や Read 監視など別設計が必要 |

## やってはいけないこと

* `claude` バイナリのインストールや契約を前提にした手順を進めること
* **サブコマンドなしの** `cursor`（IDE 起動）を Agent CLI の代替として使うこと（`cursor agent` は可）
* バインディング不能なフラグを黙って落とすこと（必ず明示する）
* Claude 専用のモデル alias（`sonnet` / `opus` / `haiku` 等）をそのまま `--model` に渡すこと → `agent --list-models` または `agent models` で実際の ID を使う
* headless で Trust プロンプトに当たったのに、対話待ちのまま放置すること → `--trust` / `-f` を足す

## 参照

* 製品ページ: [Cursor CLI](https://cursor.com/ja/cli)
* パラメータ: [Parameters](https://cursor.com/docs/cli/reference/parameters)
* Headless: [Using Headless CLI](https://cursor.com/docs/cli/headless)
* Claude 側原典: [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference)
* 詳細表: [references/command-bindings.md](./references/command-bindings.md)
* description トリガー最適化: [scripts/trigger_opt_cursor.py](./scripts/trigger_opt_cursor.py)
