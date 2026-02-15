# Data Object利用ルール

## 概要

データオブジェクトは、主に Immutable なデータの保持・転送を役割とするクラスである。
`@freezed` を用いたデータクラスや Union Type、および `extension type` による値オブジェクトが主な実装形式である。
コード作成時のテンプレートは [architecture_data_object.code-snippets](../assets/architecture_data_object.code-snippets) に定義している。

## 実装形式の選択基準

データオブジェクトの実装形式は、以下の順序で検討する。

### 1. extension type（単一プロパティの場合）

単一プロパティのみを持つ値オブジェクトの場合は、`extension type` を使用する。

#### extension typeの補足

`extension type` は Dart 3.5 以降で導入された機能であり、ゼロコストの型安全性を提供する。
実行時のオーバーヘッドがなく、コンパイル時に型チェックのみが行われる。

#### extension typeの実装例

```dart
// domain_preferences, preference_key.dart
extension type const PreferenceKey(String _value) {
  /// アプリ設定バージョン.
  /// 下位バージョンである場合は、アプリ設定のマイグレーションを行う
  static const settingsVersion = PreferenceKey("settings_version");

  /// 文字列からキーを生成する.
  factory PreferenceKey.parse(String value) {
    checkArgument(value.isNotEmpty, "value is empty");
    checkArgument(!value.contains(" "), "value contains space");
    return PreferenceKey(value);
  }

  /// テスト用のキーを生成する
  @visibleForTesting
  factory PreferenceKey.test(String value) => PreferenceKey(value);

  /// 内部の文字列値を取得する
  String unsafe() => _value;
}
```

#### extension typeのテンプレート

VS Code のスニペット `arch-value-object` を使用する。

### 2. 通常のクラス（単一プロパティ、センシティブ情報の場合）

単一プロパティだが、`toString()` で値をマスクするなどカスタマイズが必要な場合は、通常のクラスを使用する。

#### 通常のクラスの補足

センシティブな情報を扱う場合、ログ出力時に値が露出しないよう `toString()` を適切に実装する必要がある。
`extension type` では `toString()` のカスタマイズが制限されるため、その場合は通常のクラスを用い、必要に応じて `toString()` でマスク（例: `"PkAccountId(***)"`）する。

#### 通常のクラスの実装例

```dart
// domain_account, pk_account_id.dart
/// Pocket KosodateアカウントID.
///
class PkAccountId {
  /// 一意の識別子.
  /// NOTE.
  /// Firebase AuthのIDがそのまま利用される.
  final String value;

  const PkAccountId(this.value);

  @override
  String toString() => "PkAccountId($value)";

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) {
      return true;
    }

    return other is PkAccountId && other.value == value;
  }

  @override
  int get hashCode => value.hashCode;
}
```

#### 通常のクラスのテンプレート

VS Code のスニペット `arch-value-object-legacy` を使用する。

### 3. @freezed（複数プロパティまたは Union Type の場合）

複数のプロパティを持つデータクラスや、Union Type（sealed class）を定義する場合は、`@freezed` を使用する。

#### @freezedの補足

`@freezed` を用いることで、Immutable なデータクラスに必要な `copyWith`、`==`、`hashCode`、`toString` などが自動生成される。
Union Type を定義する場合は `sealed class` と組み合わせて使用する。

#### @freezedの実装例（通常のデータクラス）

```dart
// usecase_error, crash_report_request.dart
@freezed
abstract class CrashReportRequest with _$CrashReportRequest {
  const factory CrashReportRequest({
    /// エラー内容.
    required dynamic error,

    /// エラーが発生したコンテキスト.
    required StackTrace stackTrace,

    /// エラー送信の理由.
    String? reason,
  }) = _CrashReportRequest;

  const CrashReportRequest._();
}
```

```dart
// domain_account, pk_account.dart
@freezed
abstract class PkAccount with _$PkAccount {
  const factory PkAccount({
    /// 一意の識別子.
    required PkAccountId id,

    /// アカウントタイプ.
    required PkAccountType type,
  }) = _PkAccount;

  const PkAccount._();
}
```

#### @freezedの実装例（Union Type）

```dart
// usecase_school, kanji_search_result.dart
@freezed
sealed class KanjiSearchResult with _$KanjiSearchResult {
  /// データが見つかった
  const factory KanjiSearchResult.found({
    /// 対象漢字
    required Kanji kanji,

    /// 習う学年
    required SchoolGrade? learningGrade,

    /// 漢検の級
    required KankenGrade? kankenGrade,
  }) = KanjiSearchResultFound;

  /// データが見つからなかった
  const factory KanjiSearchResult.notFound() = KanjiSearchResultNotFound;

  const KanjiSearchResult._();
}
```

```dart
// view_designkit, designkit_resource_data.dart
@internal
@freezed
sealed class DesignkitResourceData with _$DesignkitResourceData {
  /// コードポイントデータ.
  const factory DesignkitResourceData.codePoint({
    required IconData codePoint,
  }) = DesignkitResourceDataCodePoint;

  /// 組み込みデータ.
  const factory DesignkitResourceData.embedded({
    required IconData embedded,
  }) = DesignkitResourceDataEmbedded;

  /// 画像データ.
  const factory DesignkitResourceData.image({
    required AssetGenImage image,
  }) = DesignkitResourceDataImage;

  const DesignkitResourceData._();
}
```

#### @freezedのテンプレート

VS Code のスニペットを使用する。

* `arch-freezed-data`: 通常のデータクラス用
* `arch-freezed-union-data`: Union Type 用
* `arch-freezed-json-data`: JSON シリアライゼーション対応用

## 型での分岐は switch を利用する

freezed の `when` / `map` は基本的に使わず、Dart の標準機能である `switch` 文を推奨する。

### switch利用の補足

`switch` 文を用いることで、次の利点がある。

* パターンマッチングが簡潔で読みやすい
* すべてのケースを網羅しているかコンパイル時にチェックできる（exhaustive check）
* 標準機能のため、追加の依存関係が不要である

### switch利用の実装例

Union Type や sealed な型での分岐に `switch` を用いる例である。

```dart
// usecase_kanji_practice_impl, passage_parse_usecase_impl.dart
    for (final c in japaneseCharacters) {
      switch (c) {
        case Hiragana():
          passageTokens.add(
            PassageToken.hiragana(
              character: c,
            ),
          );
        case Kanji():
          final kanjiSearchResult = await kanjiSearchUsecase.search(...);
          passageTokens.add(
            PassageToken.kanji(
              character: c,
              learningGrade: switch (kanjiSearchResult) {
                KanjiSearchResultFound() => kanjiSearchResult.learningGrade,
                KanjiSearchResultNotFound() => null,
              },
              kankenGrade: switch (kanjiSearchResult) {
                KanjiSearchResultFound() => kanjiSearchResult.kankenGrade,
                KanjiSearchResultNotFound() => null,
              },
            ),
          );
        case Katakana():
          passageTokens.add(
            PassageToken.katakana(
              character: c,
            ),
          );
        case OtherCharacter():
          passageTokens.add(
            PassageToken.other(
              character: c,
            ),
          );
      }
    }
```

```dart
// view_designkit, designkit_icon.dart
    final data = icon.data;
    return switch (data) {
      DesignkitResourceDataCodePoint() => _buildCodePointIcon(context, data),
      DesignkitResourceDataEmbedded() => _buildIconData(context, data),
      DesignkitResourceDataImage() => _buildImageIcon(context, data),
    };
```

### switch利用のアンチパターン

`when` や `map` を使うことは推奨しない。

```dart
// アンチパターン: when を使用
result.when(
  success: (data) => ...,
  failure: (error) => ...,
);

// 推奨: switch を使用
switch (result) {
  case ResultSuccess(data: final data):
    ...
  case ResultFailure(error: final error):
    ...
}
```

## JSON 用の DTO では @JsonKey(name: "{Key名}") を指定する

互換性の維持や、リファクタリングによる意図しないプロパティ名の変更を防ぐため、JSON 用 DTO では必ず `@JsonKey` アノテーションを指定する。

### JSON用DTOの@JsonKey指定の補足

API やストレージのキー名と Dart のプロパティ名を明示的に対応させることで、リネーム時の不整合を防ぎ、スキーマの意図をドキュメント化できる。

### JSON用DTOの@JsonKey指定の実装例

```dart
// data_source_embedded_impl, end_user_license_agreement_dto.dart
  const factory EndUserLicenseAgreementDto({
    /// EULAの本文
    // ignore: invalid_annotation_target
    @JsonKey(name: "body") required String body,

    /// EULAのバージョン
    // ignore: invalid_annotation_target
    @JsonKey(name: "version") required String version,
  }) = _EndUserLicenseAgreementDto;
```

## よくあるパターンとアンチパターン

### 推奨されるパターン

1. **実装形式の選択基準に従う**
   * 単一プロパティなら extension type、センシティブなら通常クラス、複数プロパティや Union なら @freezed を選ぶ。

2. **型分岐には switch を使う**
   * freezed の when/map ではなく、Dart の switch で網羅性をコンパイル時に担保する。

3. **JSON DTO では @JsonKey を付与する**
   * API やストレージのキー名を明示し、互換性とリファクタリングの安全性を保つ。

4. **パッケージ内部専用には @internal を付与する**
   * パッケージ外に公開しないデータオブジェクトには `@internal` を付ける。

5. **JSON シリアライゼーションが必要な場合は arch-freezed-json-data を使う**
   * API 取得やローカルストレージ保存が必要な DTO は、該当スニペットで fromJson 対応を行う。

### 避けるべきパターン

1. **データオブジェクトにビジネスロジックを載せる**
   * データの保持・転送に専念し、振る舞いは別クラス（Usecase や Delegate など）に実装する。

2. **mutable なプロパティを定義する**
   * データオブジェクトは常に Immutable とし、変更時は `copyWith` で新しいインスタンスを生成する。

3. **freezed の when/map に依存する**
   * 網羅性の担保と可読性のため、switch を優先する。

4. **JSON DTO で @JsonKey を省略する**
   * キー名の変更やリネーム時の不整合を防ぐため、必ずキー名を明示する。

## 参考リンク

* freezed: <https://pub.dev/packages/freezed>
* Dart - Extension types: <https://dart.dev/language/extension-types>
