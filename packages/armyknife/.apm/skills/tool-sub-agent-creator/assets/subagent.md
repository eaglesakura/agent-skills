---
name: {Sub Agent名}
model: inherit
description: >-
    {Sub Agentのロール、役割、入出力等の情報}
readonly: true
is_background: false
license: {Optional, ライセンス}
metadata:
    author: {Optional, Author}
    references:
        - {関連するコマンド}
        - {関連するSKILL}
        - [関連する共有アセット](../extra/{領域またはコマンド名}/{file}.md)
        - [関連するファイル]({path/to/document.md})
    required_skills:
        # このSub Agentが必須で Apply する SKILL の name（ディレクトリ名）。無い場合はキーごと省略可
        - {必須とするSKILL}
---

<!-- 
Sub Agentは、個々に適切な「職能」と「実施するタスク」を明確にする.
 -->

# {職能} / {実施するタスク}

## 専門性

<!-- 
* このSub Agentの専門分野、役割等を箇条書きで記載する
 -->

## 追加コンテキスト

* 親Agentから指示されたSKILLやドキュメントを自己判断によりロードする

## 実施タスク

<!-- 
* このSub Agentが実行すべき作業内容等を記載する
* 明確にワークフローが決まっている場合は、コマンドと同様に詳細な手順書を記載する
* 明確な手順が決まっていない場合は、期待される役割を記載する
 -->

## 出力フォーマット

<!-- 
* 出力フォーマットを記載する
* 可能な限り固定書式にするが、明確にフリーフォーマットであればその旨を記載する
-->

## ガードレール

<!-- 
* このSub Agentが遵守すべき事項を記載する
 -->

## ナレッジベース

<!-- 
* /markdown-documentationの書式に従ったDO/DO NOTナレッジを記載する
 -->
