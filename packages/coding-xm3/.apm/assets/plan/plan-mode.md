# {機能名の実装等のタイトル}

<!-- 
  このテンプレートは計画書作成のための雛形である。
  各セクションの説明に従って内容を記載すること。
  オプションセクションは、必要に応じて追加・削除する。
-->

## 要件

### {要件カテゴリ}要件

<!-- 
必須

  UI要件、データ要件、実装要件など、カテゴリごとに記載する。
  必要に応じてカテゴリを追加・変更する。
-->

* **{要件名}**
  * {要件の詳細説明}
  * {補足事項}

### 暗黙的な要件

<!-- 
必須

  明示的に記載されていないが、実装に必要な要件を記載する。
  暗黙的な要件がなければ `なし` と提示する。
-->

* **{暗黙的な要件名}**
  * {要件の詳細}

### テスト要件

<!--
必須

* 追加すべきテストを箇条書きで追加する
-->

* 正常系
  * {XXX}が{YYY}のとき、{ZZZ}となっている
* 異常系
  * {XXX}が{YYY}のとき、{ZZZ}となっている
* その他
  * {XXX}が{YYY}のとき、{ZZZ}となっている

## 実装

提案ファイルツリー

<!--
必須

* 提案内容の全体像を把握するため、編集対象すべてのファイルをツリー構造で示す.
- 追加ファイルには`[New]`サフィックスを付ける
- 削除ファイルには`[Del]`サフィックスを付ける
- 変更ファイルは通常のファイル名のまま表示する（サフィックスなし）
  -->

```text
{ディレクトリ/ファイル構造}
├── {パッケージパス}/
│   ├── lib/
│   │   ├── {libraryファイル}.dart [Update]
│   │   └── src/
│   │       └── {ファイル名}.dart [New]
│   └── pubspec.yaml [Update]
```

<!-- 
例:

```text
├── app_packages/usecase/feature_x/
│   ├── lib/
│   │   ├── usecase_feature_x.dart [New]
│   │   └── src/
│   │       └── feature_x/
│   │           ├── feature_x_usecase.dart [New]
│   │           ├── feature_x_request.dart [New]
│   │           └── feature_x_result.dart [New]
│   └── pubspec.yaml [New]
├── app_packages/usecase/feature_x/_impl/
│   ├── lib/
│   │   ├── usecase_feature_x_impl.dart [New]
│   │   └── src/
│   │       └── feature_x_usecase_impl/
│   │           └── feature_x_usecase_impl.dart [New]
│   └── pubspec.yaml [New]
├── app_packages/screen/feature/feature_x2/
│   ├── lib/
│   │   ├── screen_feature_feature_x2.dart [New]
│   │   └── src/
│   │       ├── feature_x_screen_factory.dart [New]
│   │       ├── view/
│   │       │   └── feature_x_screen.dart [New]
│   │       └── viewmodel/
│   │           ├── feature_x_screen_view_model.dart [New]
│   │           └── state/
│   │               └── feature_x_screen_state.dart [New]
│   └── pubspec.yaml [New]
└── app_packages/old_feature_y/ [Del]
```

 -->

### {修正ファイル名}

<!-- 
必須

修正内容はサマリを記載すればよい.
修正対象のファイル全てに対し、修正内容のセクションを作成する.
 -->

* {実装内容のサマリ}

現在のコード

```dart
{修正箇所}
```

修正提案内容

```dart
{修正後の内容}
```

## 補足情報

<!-- 
* 追加でユーザーに提示する情報がある場合、このブロックにフリーフォーマットでまとめる
 -->
