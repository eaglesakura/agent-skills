---
name: flutter-layered-architecture-design-patterns
description: >-
  Flutter Layered Architecture の Repository（data）実装パターン用 SKILL。
  `{機能グループ}Repository`、Read/Write・監視、interface/impl 分離、
  Repository↔Usecase の相互 IF 依存とクラス循環回避では必ず使う。
  「Repository の IF 設計」「watch / Stream」「DataInjection」でもロードする。
  Usecase の切り出し・Request・IF/_impl・結線は
  flutter-layered-architecture-design-usecase、画面 MVVM は screen-mvvm、
  所在調査は code-search、Dart 言語規約のみは flutter-coding-rules では使わない。
license: MIT License
metadata:
  author: "@eaglesakura"
---
# Flutter-Layered-Architecture / Repository パターン

Data（Repository）層の **定番実装パターン** を適用する。
Usecase 側は `flutter-layered-architecture-design-usecase` を正とする。

## いつ使うか

* Repository のインターフェース・実装を新規作成・改修するとき
* Read/Write・監視（`watch` / `Stream`）の窓口を設計するとき
* Repository と Usecase の相互依存を組むとき

## いつ使わないか

* Usecase の切り出し・Request・結線 → `flutter-layered-architecture-design-usecase`
* 画面 MVVM → `flutter-layered-architecture-screen-mvvm`
* 所在調査 → `flutter-layered-architecture-code-search`
* 言語規約だけ → `flutter-coding-rules`

## 作業手順

1. 機能グループ単位で Repository 境界を決める
2. IF / 命名 / Read・Write・監視を決める
3. [references/repository-pattern.md](./references/repository-pattern.md) を読む
4. Usecase との相互 IF 依存ではクラス循環を避ける（`Provider.dependencies`）

## Repository パターン（要約）

* 名称は `{機能グループ名}Repository`
* **同一機能グループなら複数メソッド可**（Usecase の 1 操作原則とは違う）
* Read/Write・監視（`watch` / `Stream`）を窓口として抽象化してよい
* 入出力は Request / Result を基本としてよい
* interface / 実装は別 package。注入は DataInjection 等で一元化することが多い

詳細 → [references/repository-pattern.md](./references/repository-pattern.md)

## Repository ↔ Usecase の依存

* usecase と data は同レベルのため、**相互のインターフェース依存は可**
* **クラス循環は不可**。`Provider.dependencies` を把握して組む
* 実装 package 同士の密結合や、公開 IF への SDK リークを避ける
* Usecase 側の結線・切り出しは `design-usecase`

## ナレッジベース

### DO: Repository は機能グループでまとめる

* Usecase を肥大化させず、データ操作の窓口を散らしすぎない

### DO: 公開面は interface、詳細は実装 package

* テスト差し替えと循環防止のため

### DO NOT: Usecase の 1 操作原則を Repository に押し付けない

* Repository はグループ単位で複数メソッドを持ってよい
