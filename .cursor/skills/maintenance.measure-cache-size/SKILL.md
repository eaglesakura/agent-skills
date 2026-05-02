---
name: maintenance.measure-cache-size
description: ローカルPCのキャッシュサイズを特定する。インストールされている開発ツールごとに測定し、不要なキャッシュを表示する
---

# メンテナンス / キャッシュサイズ特定

* ローカルPCにインストールされているツールのキャッシュサイズを特定する際に使用する

## 基本的手順

* 指定されたディレクトリから、占有サイズの大きなディレクトリを探索する
  * 10GiBよりも大きなディレクトリの場合、下の階層を調査する
  * 最大2階層下まで探索する
* ディレクトリごとに `GiB` 単位でディスク占有量を計算する
  * 占有サイズで降順ソートを行う
  * 1GiB未満のディレクトリは除外する

### 出力フォーマット

| Path | サイズ(GiB) | 予想される用途 | 復元可否 | 削除コマンド |
| --- | --- | --- | --- | --- |
| ~/path/to/dir | 128GiB | ビルドキャッシュ | 再取得可能 | rm -rf ~/path/to/dir |
| ~/Library | 128GiB | システムキャッシュ | OS用 | - |
| Docker Image / ubuntu:24.04 LTS | 1GiB | Docker用 Ubuntu Image | 再取得可能 | docker rm |

## OSごとの探索対象ディレクトリ

### macOS / Linux共通

* `~/.bundle`
* `~/.cache/`
* `~/.cargo/`
* `~/.cocoapods`
* `~/.composer/`
* `~/.dart*/`
* `~/.dlv/`
* `~/.flutter*/`
* `~/.fvm/`
* `~/.gem/`
* `~/.gradle/`
* `~/.gsutil/`
* `~/.nodebrew/`
* `~/.npm/`
* `~/.pub-cache/`
* `~/.sdkman/`
* `~/.yarn/`
* `~/go/`
* `${GOMODCACHE}`

### macOS

* `~/Library/Caches/`
* `/Library/Caches/`
* `/opt/homebrew/var/cache/`
* `~/Library/Caches/Homebrew/`
* `/Applications`
* `~/Applications`

## ツールごとの確認対象

### dockerがインストールされている場合

下記のコマンドを例に、使用しているキャッシュサイズを収集する

```bash
# イメージ・コンテナ・ローカルボリューム・ビルドキャッシュの集計（人間可読）
docker system df

# 上記の詳細（各イメージ・コンテナ行まで展開）
docker system df -v

# イメージごとのサイズ（REPOSITORY:TAG / IMAGE ID / SIZE）
docker images

# 実行中コンテナごとのサイズ（SIZE 列に書き込み可能レイヤを含む）
docker ps -s

# 停止中含む全コンテナのサイズ
docker ps -as

# ボリューム一覧
docker volume ls

# ボリュームのドライバ・マウントパス等（<volume名> を置き換え）
docker volume inspect <volume名>
```

## 追加の探査

* ユーザーがディレクトリを指定した場合（ユーザー固有のWorkspace等）、そのディレクトリも同様の手順で探査する
* 容量の少ないディレクトリについては、基本ルールを遵守して除外する
