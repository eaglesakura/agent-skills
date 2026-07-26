---
name: tool-skill-creator-extension
description: >-
  SKILL 作成・改訂時のコマンド記述と共有アセット参照ルールを補足する SKILL。
  skill-creator で新規 SKILL を書く、既存 SKILL のコマンド例を直す、手順書に
  `dart` / `flutter` / `go` / `npm` 等を載せるときは必ず使う。
  `{assets}/` や共有テンプレートを SKILL から参照する、`## アセットディレクトリ` を書く、
  「mise を SKILL から外す」「portable な手順にする」でもロードする。
  `mise exec --` / `fvm` / `asdf` 等のツールチェイン wrapper を SKILL 本文に埋め込まない。
  実際のシェル実行そのものだけ（SKILL を書かない）では使わない。
  `{assets}/` の実行時解決は workspace-resolve-agent-assets を使う。
license: MIT License
metadata:
  author: "@eaglesakura"
  references:
    - skill-creator
    - workspace-resolve-agent-assets
    - tool-command-creator
    - tool-sub-agent-creator
---
# Tool / Skill Creator Extension

SKILL はリポジトリ横断・環境横断で再利用される。ツールチェイン管理（`mise` / `fvm` / `asdf` 等）の
prefix・wrapper は **プロジェクト固有の実行規約** であり、SKILL 本文に焼き付けると他環境でノイズになる。
コマンド例は素のツール呼び出しだけを書き、実行時の wrapper は各プロジェクトのルール（`AGENTS.md` 等）に任せる。

共有アセット（テンプレート・雛形・パッケージ配下の `.apm/assets/` 等）を参照する場合も、
インストール先の 1 パスを直書きせず、`{assets}/` と `## アセットディレクトリ` で解決できるようにする。

本 SKILL は `skill-creator` の補足である。SKILL を新規作成・改訂するときは本ルールも適用する。

## いつ使うか

* 新規 SKILL の `SKILL.md` / `references/` にシェルコマンド例を書くとき
* 既存 SKILL から `mise exec --` 等の project-local wrapper を除去・正規化するとき
* skill-creator のドラフト・レビューで「コマンドの書き方」を点検するとき
* SKILL 本文から共有アセット（テンプレート等）を参照するとき
* `{assets}/` や `## アセットディレクトリ` を追加・移行するとき

## コアルール

### SKILL に書くコマンド（portable）

* ツール本体の呼び出しだけを書く（`dart` / `flutter` / `go` / `npm` / `npx` など）
* プロジェクト固有のツールチェイン wrapper・prefix・suffix は **含めない**
  * 例: `mise exec --` / `mise run` / `fvm` / `asdf exec` / `direnv exec` / `nix-shell --run`

#### DO: ツール本体だけを書く

```bash
dart -h
flutter --version
go test ./...
npx markdownlint-cli2 --fix path/to/file.md
```

#### DO NOT: ツールチェイン wrapper を埋め込む

```bash
mise exec -- dart -h
fvm flutter --version
asdf exec go test ./...
```

### 実行時（runtime）の扱い

SKILL を **実際に実行する** ときは、この限りではない。

* 作業対象リポジトリに `mise` / `fvm` 等の規定があれば、そのプロジェクトルールに従う
* 規定の所在は `AGENTS.md`・リポジトリ README・既存スクリプトを優先して確認する
* SKILL 本文を「実行用の最終コマンド」と同一視しない（本文は portable、実行は local policy）

必要なら SKILL 側に次のような一文を置いてよい（具体的な wrapper 名は書かない）。

```markdown
コマンド実行時は、プロジェクト規定のツールチェイン（あれば）に従う。
```

### 共有アセットの参照（`{assets}/`）

Agent / パッケージが共有するテンプレートや雛形を SKILL から読む必要がある場合は、次に従う。

* 本文・手順・関連リンクでは、インストール先の絶対的な 1 パスを直書きしない
* 代わりにメタ変数 `{assets}/...` で参照する（例: `{assets}/coding/requirements.md`）
* `{assets}/` を使う場合は、本文に `## アセットディレクトリ` を置き、**解決候補ディレクトリの一覧**を箇条書きする（正本）
* 使わない SKILL では `## アセットディレクトリ` をセクションごと省略する
* 新規・改訂では `metadata.assets` に寄せない（旧文書の互換読みは `workspace-resolve-agent-assets` が担う）

#### `## アセットディレクトリ` の書き方

* 各行はディレクトリパス（ファイルパスではない）
* **文書相対**（この `SKILL.md` から）または **リポジトリルート相対**
* 開発時（ソース相対）と install 後（`apm_modules/...` 等のルート相対）の両方を並べると、展開先でも解決しやすい
* Markdown リンク `[label](path)` 形式でもよい（`path` をディレクトリとして使う）
* SKILL 改訂・新規ドラフトを提案するとき、本文に `{assets}/` が出るなら **同じ成果物に** `## アセットディレクトリ` ブロックを必ず含める（後回しにしない）
* 見出し位置は、手順・実行の **前**（導入の直後〜入力の前）がよい。末尾にだけ置くと読み手が探索先を見落とす

```markdown
## アセットディレクトリ

* `../../assets/`
* `apm_modules/eaglesakura/agent-skills/packages/coding-xm3/.apm/assets/`
```

本文での参照例:

```markdown
* `{assets}/coding/requirements.md`（要件定義フォーマット）をロードする
```

#### DO NOT（アセット）

* `{assets}/` 参照だけ書いて探索先セクションを省略する
* `metadata.assets` だけを正本にする
* 壊れた `../{assets}/file.md` 形式のリンクを残す
* アセット不要な SKILL に空の `## アセットディレクトリ` を足す

#### 実行時のパス解決

`{assets}/...` を実ファイルパスへ落とすときは、必ず `workspace-resolve-agent-assets` に従う。

* 基準ファイルは `{assets}/` が書かれている `SKILL.md`（またはその文書）自身
* 候補は `## アセットディレクトリ`（無ければ互換の `metadata.assets`）から読む
* 各候補について文書相対・ワークスペースルート相対の両方を試し、存在するヒットを使う
* 候補ディレクトリとサフィックスを結合する（ディレクトリ一覧だけでは実ファイルにならない）
* ヒットが 0 件なら推測読みしない

通常の `path/to/file`・Markdown リンク・`.ai-agent/` の解決は `workspace-resolve-file-path` の範囲であり、`{assets}/` とは混ぜない。

## 適用手順（SKILL 作成・改訂時）

1. 手順に出すコマンド列を列挙する
2. 各コマンドからツールチェイン wrapper を剥がし、ツール本体だけ残す
3. 「このプロジェクトでは `mise exec --` が必須」のような **環境固有の断言** を SKILL 本文に書かない
4. 実行時の wrapper が必要なら、上記の汎用一文に留めるか、実行 Agent が `AGENTS.md` を読む前提にする
5. 共有アセットが必要なら、本文参照を `{assets}/...` にし、`## アセットディレクトリ` に解決候補を列挙する
6. 実行時に `{assets}/` を読む手順があるなら、`workspace-resolve-agent-assets` で解決する旨を手順または関連に残す
7. 例示は DO / DO NOT が対になるようにすると読み手が迷いにくい

### 自己レビュー（追加）

* [ ] コマンド例に `mise` / `fvm` / `asdf` 等の wrapper が無い
* [ ] `{assets}/` を使う場合: `## アセットディレクトリ` に探索先が列挙されている（使わないならセクション無し）
* [ ] `{assets}/` がある成果物に、文書相対と（可能なら）install 後ルート相対の両方がある
* [ ] `{assets}/` の実行時解決が `workspace-resolve-agent-assets` 前提になっている（必要な場合）
* [ ] 旧 `metadata.assets` だけを正本にしていない

## 境界

* **本 SKILL の対象**: SKILL・手順ドキュメントに載せるコマンドの **記述**、および共有アセット参照の **書き方**
* **対象外**: いま開いているシェルで何を打つか（それは各リポジトリの実行規約）
* **対象外**: `{assets}/` 解決アルゴリズム本体（それは `workspace-resolve-agent-assets`）
* CI ワークフロー（`.github/workflows`）は実行環境そのものなので、そこでの `mise` 利用は本ルールの対象外。ただし「SKILL から CI を説明する」場合のコマンド例は portable に保つ

## やってはいけないこと

* 「この HQ / このリポジトリでは常に `mise exec --`」を SKILL の必須手順として固定すること
* コマンド例だけ portable にして、説明文で特定 wrapper を必須と書くこと（実質同じ漏れ）
* portable 化のために、ツール本体のサブコマンドやフラグまで省略すること（`dart -h` の `-h` は残す）
* 共有アセットへの参照を、install 先の 1 パス直書きや壊れた `../{assets}/...` リンクにすること
* `{assets}/` をリテラルなフォルダ名として探索し、`workspace-resolve-agent-assets` を飛ばすこと

## 関連

* SKILL 本体の作成フロー: `skill-creator`
* `{assets}/` の実体解決: `workspace-resolve-agent-assets`
* slash-command 側の同種ルール: `tool-command-creator`
* Sub Agent 側の同種ルール: `tool-sub-agent-creator`
