# Golang / 一般コーディング規約

## 概要

本ドキュメントは、Golang における一般的なコーディング規約のうち、import 文の別名指定と入れ子 error の確認方法を定義する。

* import 文の package 別名は、package 名の末尾1ワードを用いる。
* 入れ子の error を確認する場合は `errors.As` を使用する。

## import文

import文のpackage別名指定は、package名の中から末尾の1ワードを使用する。
バージョンsuffixが付与されている場合、識別可能な文字列を確認してimportする。

### import文の補足

別名を末尾1ワードに揃えることで、呼び出し側の識別子が短く一貫し、どのパッケージ由来かが読み取りやすくなる。

### import文の実装例

```go
import (
    // ローカルモジュールではない
 secretmanager "cloud.google.com/go/secretmanager/apiv1"
)
```

## error型のチェック(unwrap)

入れ子のerror型を確認する場合（内包するエラーを確認する場合）は、`errors.As` を使用する。

### error型のチェックの補足

`errors.As` により、ラップされた error の具象型を安全に取り出せる。型アサーションの繰り返しや文字列比較による判定を避ける。

### error型のチェックの実装例

```go
 var connectErr *connect.Error
 if !errors.As(err, &connectErr) {
  t.Fatalf("*connect.Error であるべき: 実際=%T", err)
 }
```

## ナレッジベース

### DO: import の別名に package 名の末尾1ワードを使う

* バージョン suffix がある場合は、識別可能な文字列を確認して import する。

```go
import (
    // ローカルモジュールではない
 secretmanager "cloud.google.com/go/secretmanager/apiv1"
)
```

### DO: 入れ子 error の確認に `errors.As` を使う

* 内包するエラーの具象型を安全に取り出す。

```go
 var connectErr *connect.Error
 if !errors.As(err, &connectErr) {
  t.Fatalf("*connect.Error であるべき: 実際=%T", err)
 }
```

### DO NOT: 入れ子 error を文字列比較や不安定な型アサーションだけで判定する

* 理由: ラップ構造の変化に弱く、誤判定や壊れやすいテストになる。
