---
name: flutter.layered-architecture.library-update
description: Layered Architectureの推奨設計に従い、ライブラリ更新を行う
---
# Flutter-Layered-Architecture / ライブラリアップデート

* 参照しているライブラリの更新を行う

## 手順

1. ライブラリの更新状態を取得する

    ```bash
    flutter pub outdated
    ```

2. 推奨されるライブラリバージョンを確認する
    * `Resolvable` 等の属性から判断する

3. リポジトリルートの `pubspec.yaml` `dependency_overrides:` のバージョンを更新する

    ```yaml
    dependency_overrides:
        armyknife_dartx: "^1.0.0"   # <- 必要に応じて更新する
    ```

    * **互換性の問題により、バージョンアップできない場合は、スキップする**

4. 妥当性を検証する

    ```bash
    flutter pub get
    ```

    ```bash
    cd app/
    flutter pub get
    cd ios/
    rm Podfile.lock
    pod install
    cd ../../
    ```

5. 必要に応じて、テストやビルド等を行い、妥当性を検証する
