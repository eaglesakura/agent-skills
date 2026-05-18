# Golang / 一般コーディング規約

## import文

* import文のpackage別名指定は、package名の中から末尾の1ワードを使用する
  * バージョンsuffixが付与されている場合、識別可能な文字列を確認してimportする

```go

import (
    // ローカルモジュールではない
 secretmanager "cloud.google.com/go/secretmanager/apiv1"

)

```

## error型のチェック(unwrap)

* 入れ子のerror型を確認する場合（内包するエラーを確認する場合）は、 `errors.As` を使用する

```go
 var connectErr *connect.Error
 if !errors.As(err, &connectErr) {
  t.Fatalf("*connect.Error であるべき: 実際=%T", err)
 }
```
