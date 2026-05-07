---
name: flutter.layered-architecture.workspace
description: Flutter-Layered-Architecture アプリのワークスペース構造を把握するSKILL。基本的なpackageレイアウトや、依存ライブラリの管理方法等を把握する。
license: MIT License
metadata:
  author: "@eaglesakura"
---

# Flutter / ワークスペース構造

## ルートレベル pubspec.yamlの `workspace` で、すべてのローカルパッケージを管理する

* アプリ固有のpackageは、すべてプロジェクトルートの `pubspec.yaml` のworkspaceブロックに記載されている
* ワークスペースの `pubspec.yaml` の `workspace:` ブロックから、すべてのpackageのレイアウトを把握可能である

  ```yaml
  workspace:
    - app
    - app_packages/data/database
    # 以下、すべてのpackageが列挙されている
  ```

* 関連SKILLから、リポジトリのレイアウト及びレイヤードアーキテクチャの構造を把握する
* アーキテクチャ構造から、対象となるpackageを推測する
* 対象packageを適宜探索し、必要な情報を収集する

### 慣習 / `app` packageでアプリをビルドする

* ユーザーに提供すべきアプリpackageは、 `app` packageとして提供する

```bash
# appディレクトリでビルドを行う
cd app/
flutter build ...
```

## ルートレベル pubspec.yamlの `dependency_overrides` で、すべての依存を管理する

* アプリ内の依存管理は、すべてルートレベルのpubspec.yamlが管理している
* ライブラリの更新は、 `dependency_overrides` を操作することで行う

```yaml
# ルートレベルのpubspec.yaml
---

# flutter / dartバージョンは、ワークスペース内で統一する
environment:
  sdk: ">=3.11.0 <4.0.0"
  flutter: ">=3.41.0 <4.0.0"

dependency_overrides:
  armyknife_dartx: "^1.0.0"         # バージョンを特定する
  armyknife_exceptions: "^1.0.0+2"
  armyknife_flutter_testx: "^1.0.0"
  armyknife_flutterx: "^1.0.0"
```

```yaml
# アプリ内packageでのpubspec.yaml
---
# workspace所属と、publish禁止属性を付与する
publish_to: "none"
resolution: workspace

# flutter / dartバージョンは、ワークスペース内で統一する
environment:
  sdk: ">=3.11.0 <4.0.0"
  flutter: ">=3.41.0 <4.0.0"

dependencies:
  flutter:
    sdk: flutter
  armyknife_dartx: any  # anyを使用する
```

### ライブラリ更新

1. 依存ライブラリの最新情報を取得する

    ```bash
    flutter pub outdated --json
    ```

2. ユーザーの指示に従い、アップデート可能なバージョンをサジェストするなど、対応を行う
3. ライブラリ更新は、再度各種依存を解決する

    ```bash
    # 最新依存を解決する
    flutter pub get

    # アプリの依存（Pod等）を解決する
    cd app
    flutter clean
    flutter pub get
    ```

4. アプリのクリーンビルドが行えることを確認する
