---
name: agent.memory.save
description: AI Agentのコンテキストを一時的に保存するためのSKILL。Agentが現在のチャット文脈の保存を依頼された場合、このSKILLを使用して不揮発化し、その後の整理に活用する。
license: MIT License
metadata:
  author: @eaglesakura
---
# AI Agent / Memory Save

## 保存内容

* ユーザーが調査を依頼し、調査内容をまとめたらmemoryとして保存する
* 会話内容のサマリをまとめ、別チャットへの引き継ぎ文書としても良い

## 出力先

* `.ai-agent/memory/{文脈内容}.md`
* 同様のMemoryがすでに行われている場合、ドキュメントを更新する

### 出力時の考慮

* ロードするときは "##" のレベル2単位で把握される
* 適切にブロックを分離すること

## ドキュメントフォーマット

* [テンプレート](./assets/template.md)に従う
