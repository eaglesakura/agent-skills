# Golang / 一般コーディング規約

## import文

* import文は、`go.work` に登録されているローカルモジュールの場合、識別可能な語句をそのまま使用する
* go.workで連動したローカルモジュールの場合は、ワードごとの頭文字を使用する
* 頭文字が重複する場合のみ、その部分を略さず記載する

```go

import (
    // ローカルモジュールではない
 secretmanager "cloud.google.com/go/secretmanager/apiv1"

    // go.workに記述されたローカルモジュール
 ew "github.com/eaglesakura/example_words"

    // go.workに記述されたローカルモジュール
    // 略語が `ewf` のように重複する場合
 ew_factory "github.com/eaglesakura/example_words_factory"
 ew_fantasy "github.com/eaglesakura/example_words_fantasy"
)

```
