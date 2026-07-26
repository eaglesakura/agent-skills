# ai-agent-headquarters

## このリポジトリについて

* @eaglesakura が個人開発時に使用する SKILL や Sub Agent 等の AI Agent 設定集である
* 基本的に @eaglesakura 個人の開発者としての宗教観・設計・趣味に基づいている
* すべて日本語で記載されており、Token 数の最適化については考慮されていない

## APM Packages

SKILL / Prompt / Agent / 共有アセットは APM パッケージとして `packages/` 配下に置く。
各パッケージの SKILL・Command・Sub Agent の詳細は、パッケージごとの README を参照する。

| パッケージ | パス | 依存の書き方 |
| --- | --- | --- |
| `armyknife` | [`packages/armyknife`](packages/armyknife) | `eaglesakura/agent-skills/packages/armyknife` |
| `armyknife-cursor` | [`packages/armyknife-cursor`](packages/armyknife-cursor) | `eaglesakura/agent-skills/packages/armyknife-cursor` |
| `coding-xm3` | [`packages/coding-xm3`](packages/coding-xm3) | `eaglesakura/agent-skills/packages/coding-xm3` |
| `flutter` | [`packages/flutter`](packages/flutter) | `eaglesakura/agent-skills/packages/flutter` |
| `golang` | [`packages/golang`](packages/golang) | `eaglesakura/agent-skills/packages/golang` |

```yaml
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/armyknife
    - eaglesakura/agent-skills/packages/armyknife-cursor
    - eaglesakura/agent-skills/packages/coding-xm3
    - eaglesakura/agent-skills/packages/flutter
    - eaglesakura/agent-skills/packages/golang
```

| パッケージ | README |
| --- | --- |
| `armyknife` | [packages/armyknife/README.md](packages/armyknife/README.md) |
| `armyknife-cursor` | [packages/armyknife-cursor/README.md](packages/armyknife-cursor/README.md) |
| `coding-xm3` | [packages/coding-xm3/README.md](packages/coding-xm3/README.md) |
| `flutter` | [packages/flutter/README.md](packages/flutter/README.md) |
| `golang` | [packages/golang/README.md](packages/golang/README.md) |
