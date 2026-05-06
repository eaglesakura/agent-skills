---
name: flutter.layered-architecture.design-patterns
description: Flutter-Layered-Architecture アプリに最適化された汎用的デザインパターンを知るためのSKILL。コード調査についても、アーキテクチャを知ることで精度を高めることができる。
license: MIT License
metadata:
  author: @eaglesakura
---
# Flutter-Layered-Architecture / デザインパターン

## Usecase層 / Usecase設計

Usecase層における一般的な実装パターン。

1インターフェースにつき1機能を提供し、 `Request & Result` オブジェクトによる引数・レスポンスパターンの統制を行う。

* 詳細については、ドキュメントをロードして把握する。
* [Usecase層のインターフェース設計・実装パターン](./references/usecase-pattern.md)
  * 例: Usecase層の設計・実装を行う

## Data層 / Repository設計

Data層における一般的な実装パターン。

データのRead/Write両方を行うインターフェースを `{機能グループ名}Repository` として定義する。

* 詳細については、ドキュメントをロードして把握する。
* [Data層/Repositoryインターフェース設計・実装パターン](./references/repository-pattern.md)

## Repository <--> Usecaseの依存関係

* Data層はUsecase層と同一レベルに属しているため、相互でインターフェースに依存することを認めている
  * 例: 特定のRepositoryが、特定のUsecaseのビジネスロジックを使用する
  * 例: 特定のUsecaseが、特定のRepositoryの操作を行う
* ただし、クラス設計上の循環参照にならないよう、依存関係に注意して設計する
  * Riverpodの `Provider.dependencies` を適切に管理・把握する
