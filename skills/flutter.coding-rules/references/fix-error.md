# コーディング中のエラー修正

## `dart fix --apply` による自動修正

* コーディング中に発生した警告は、dartコマンドによる自動修復を試みる

```bash
# analyzerの案内に従い、修復を行う
dart fix --apply path/to/directory-or-file
```

## `dart analyze --fatal-infos --fatal-warnings` コマンドによる問題点抽出

* `dart fix` コマンドで自動修復が行えない場合に限り、analyzeを実行して問題点を個別対応する

```bash
dart analyze --fatal-infos --fatal-warnings
```

## `dart format path/to/directory-or-file` による自動フォーマッタ

* コーディング後は、 `dart format` コマンドを使用して自動的にフォーマッタを適用する

```bash
dart format path/to/directory-or-file
```
