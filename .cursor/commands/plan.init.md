# Planモード初期化

## 概要

* Planモード開始前に、このコマンドの内容を遵守してAI Agentの初期化を行う

## 出力ルール

* ユーザーへの提案書式は [テンプレート](../extra/plan/plan-mode.md) に従う

## 計画立案ルール

* 提案は `シニアエンジニア` が作業可能な粒度を目安に詳細化する
  * 詳細化の指示を受けた場合、 `ジュニアエンジニア` が作業可能なレベル以上を目安に詳細化する
  
* Planを行うにあたり、積極的にSKILLの適用を行う。
  * SKILL例
    * `/engineer.software-requirement`
    * `/engineer.software-design`

## レビュールール

必要に応じ、積極的にSub Agentを呼び出してレビューを受ける

* Sub Agent例
  * `/coding-assistant.plan-reviewer`
  * `/coding-assistant.requirement-reviewer`

---

以後のプロンプトは、すべてPlanに対する指示です。
