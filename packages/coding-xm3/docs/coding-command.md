# `/coding.*` コマンド

## AI駆動開発

* AI Agentによる開発を円滑に行うため、コード生成は3ステップに分割されている
    1. 要件定義
    2. 詳細設計
    3. 実施
* Cursorの `Auto` Agentモードに最適化されている
  * これは個人開発者の課金額に最適化したもので、業務利用のように課金額の上限が高い場合はより良いModel・大量のContext・高い並列性に最適化すべきである
* 1つのAgentチャットで行うことを推奨する
* Context量が増えた場合、適宜 `/Summarize` で要約して良い
* 計画ドキュメントとして出力されることで、初手からコードを変更するよりも設計上の考慮をしやすい利点がある

## 利用手順

### ステップ1: `/coding.requirement` コマンド

* 要件定義を行う粒度はコーディングを行うエンジニアの裁量であり、CursorのAutoモードのContext量（200k Token程度）に実装が収まるよう想定した分量する
* Cursor Autoモードは、一つの画面をすべて一度に実装するほどの現実的なContext量・実装能力を持たないため、 `状態設計` `UI設計` `統合`等、適宜エンジニア自身が分割することが望ましい

利用例:

```text
/coding.requirement

# 要件

* ログインを行う画面のStateを実装する
* 要素
    * ユーザーメールアドレス入力フォーム
    * パスワード入力フォーム
    * 規約同意チェック
    * ログインボタン
```

* コマンドを実行すると、定義漏れや暗黙的要件の明文化を促されるため、適宜質問に回答する

```mermaid
sequenceDiagram
    participant U as ユーザー
    participant Main as Main Agent
    participant ReqRev as coding-assistant.requirement-reviewer

    U->>Main: /coding.requirement（要件）
    loop ユーザーが承認するまで繰り返す
        Main->>Main: 計画更新（要件定義）
        Main->>ReqRev: レビュー依頼
        ReqRev-->>Main: レビュー結果
        Main->>Main: 指摘反映・計画更新
        Main-->>U: 指摘・要件定義結果・質問
        U->>Main: 質問への回答・修正指示
    end
```

### ステップ2: `/coding.design` コマンド

* 要件がまとまったら、 `/coding.design` で、実際のコード差分の提案を受ける

利用例:

```text
/coding.design
```

* 提案されたコードに対し、適宜修正を行う

```mermaid
sequenceDiagram
    participant U as ユーザー
    participant Main as Main Agent
    participant DesRev as "coding-assistant.software-design-reviewer（並列）"
    participant DesAudit as coding-assistant.software-design-audit
    participant PlanRev as coding-assistant.plan-reviewer

    U->>Main: /coding.design
    loop ユーザーが承認するまで繰り返す
        Main->>Main: 計画更新（詳細設計）
        par 並列レビュー
            Main->>DesRev: レビュー（監査者／実装者視点）
            DesRev-->>Main: レビュー結果
            Main->>DesAudit: DO NOT 監査
            DesAudit-->>Main: 監査結果
        end
        Main->>Main: 指摘反映・詳細設計改善
        Main->>PlanRev: ジュニア実現性確認
        PlanRev-->>Main: 査読結果
        Main->>Main: 指摘反映・計画更新
        Main-->>U: 指摘・詳細設計結果
        U->>Main: 修正指示／承認
    end
```

### ステップ3: `/coding.execute` コマンド

* コード差分の提案に問題がないと判断したら、 `/coding.execute` で、実施を行う
* ステップ・バイ・ステップとして手順が文書化されているため、特定のステップだけを実施することが可能

利用例: 計画をすべて承認し、実行完了させる

```text
/coding.execute
```

利用例: 計画の一部を承認し、実行させる

```text
/coding.execute ステップ1を完了させてください
```

```text
/coding.execute ステップ1, 3, 5を完了させてください
```

```mermaid
sequenceDiagram
    participant U as ユーザー
    participant Main as Main Agent
    participant Junior as coding-assistant.junior-engineer
    participant Senior as coding-assistant.senior-engineer

    U->>Main: /coding.execute（任意でステップ指定）
    Main->>Main: 実行範囲の確定・ハーネス解除
    Main->>Junior: 実装依頼
    alt ジュニアが完遂
        Junior-->>Main: 実装結果
    else ジュニアが未完遂
        Junior-->>Main: 未完了報告
        Main->>Senior: 未完了ステップの引き継ぎ
        Senior-->>Main: 実装結果
    end
    Main->>Main: 結果統合・チェックリスト更新
    Main->>Senior: 品質フォローアップ
    Senior-->>Main: 指摘・修正反映
    Main-->>U: 実行結果サマリ
```
