---
name: tool-skill-creator-extension
description: >-
  SKILL 作成・改訂時のコマンド記述ルールを補足する SKILL。 skill-creator で新規 SKILL を書く、
  既存 SKILL のコマンド例を直す、手順書に `dart` / `flutter` / `go` / `npm` 等を載せるときは必ず使う。
  `mise exec --` / `fvm` / `asdf` 等のツールチェイン wrapper を SKILL 本文に埋め込まない。
  「SKILL にコマンド例を書く」「portable な手順にする」「mise を SKILL から外す」でもロードする。
  実際のシェル実行そのものだけ（SKILL を書かない）では使わない。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# Tool / Skill Creator Extension

SKILL はリポジトリ横断・環境横断で再利用される。ツールチェイン管理（`mise` / `fvm` / `asdf` 等）の
prefix・wrapper は **プロジェクト固有の実行規約** であり、SKILL 本文に焼き付けると他環境でノイズになる。
コマンド例は素のツール呼び出しだけを書き、実行時の wrapper は各プロジェクトのルール（`AGENTS.md` 等）に任せる。

本 SKILL は `skill-creator` の補足である。SKILL を新規作成・改訂するときは本ルールも適用する。

## いつ使うか

* 新規 SKILL の `SKILL.md` / `references/` にシェルコマンド例を書くとき
* 既存 SKILL から `mise exec --` 等の project-local wrapper を除去・正規化するとき
* skill-creator のドラフト・レビューで「コマンドの書き方」を点検するとき

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

## 適用手順（SKILL 作成・改訂時）

1. 手順に出すコマンド列を列挙する
2. 各コマンドからツールチェイン wrapper を剥がし、ツール本体だけ残す
3. 「このプロジェクトでは `mise exec --` が必須」のような **環境固有の断言** を SKILL 本文に書かない
4. 実行時の wrapper が必要なら、上記の汎用一文に留めるか、実行 Agent が `AGENTS.md` を読む前提にする
5. 例示は DO / DO NOT が対になるようにすると読み手が迷いにくい

## 境界

* **本 SKILL の対象**: SKILL・手順ドキュメントに載せるコマンドの **記述**
* **対象外**: いま開いているシェルで何を打つか（それは各リポジトリの実行規約）
* CI ワークフロー（`.github/workflows`）は実行環境そのものなので、そこでの `mise` 利用は本ルールの対象外。ただし「SKILL から CI を説明する」場合のコマンド例は portable に保つ

## やってはいけないこと

* 「この HQ / このリポジトリでは常に `mise exec --`」を SKILL の必須手順として固定すること
* コマンド例だけ portable にして、説明文で特定 wrapper を必須と書くこと（実質同じ漏れ）
* portable 化のために、ツール本体のサブコマンドやフラグまで省略すること（`dart -h` の `-h` は残す）
