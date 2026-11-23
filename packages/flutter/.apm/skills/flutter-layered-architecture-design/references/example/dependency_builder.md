# DependencyBuilderリファレンス実装

プロジェクト固有の事情が発生することが多々あるため、次のようなクラスをプロジェクトの要件に応じて作成・拡張することを推奨する。

DI 構築の正本は [`riverpod_container_builder`](https://pub.dev/packages/riverpod_container_builder) の `ProviderContainerBuilder` を使う。
プロジェクト差分（例: `ProviderContainerAsyncHelper.inject()` の自動適用）だけを薄いラッパーに閉じ込める。

```dart
// app_packages/foundation/dependency_injection/lib/src/dependency_builder.dart

import "package:flutter_riverpod/flutter_riverpod.dart";
import "package:riverpod/misc.dart";
import "package:riverpod_container_async/riverpod_container_async.dart";
import "package:riverpod_container_builder/riverpod_container_builder.dart";

/// DI構築を行うインターフェース.
///
/// [ProviderContainerBuilder] を内包し、プロジェクト固有として
/// [ProviderContainerAsyncHelper.inject] を常に適用する.
class DependencyBuilder {
  final _builder = ProviderContainerBuilder();

  /// オーバーライドを追加する.
  void addOverrides(Iterable<Override> overrides) {
    _builder.addOverrides(overrides);
  }

  /// [ProviderContainer]を構築する.
  ///
  /// [ProviderContainerAsyncHelper.inject] を先頭に適用する.
  ProviderContainer build({
    ProviderContainer? parent,
  }) {
    return ProviderContainer(
      parent: parent,
      overrides: [
        ...ProviderContainerAsyncHelper.inject(),
        ..._builder.overrides,
      ],
    );
  }

  /// 指定したProviderを別なProviderで上書きする.
  void inject<T, T2 extends T>(Provider<T> origin, Provider<T2> override) {
    _builder.inject(origin, override);
  }

  /// 指定したProviderを指定した値で上書きする.
  void injectValue<T>(Provider<T> origin, T value) {
    _builder.injectValue(origin, value);
  }

  /// プロバイダーのオーバーライドを設定する.
  void override<T>(Provider<T> provider, Override override) {
    _builder.override(provider, override);
  }
}
```
