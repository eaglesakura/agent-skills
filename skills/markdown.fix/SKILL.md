---
name: markdown.fix
description: Markdown(*.md) ファイルのFormatterとLint対応を行う。Markdownを提供する際は、可能な限りこのSKILLによって書式を統一する。
---

# Markdown / Fix Lint, Fix Format

* Markdownファイルの書式を統一し、一貫した可読性を確保する
* 統一した手順で扱いやすいMarkdownファイルを提供する

## 入力

* プロンプトを通じて、対象ファイルを特定する
* ディレクトリを入力された場合、配下にあるすべてのMarkdownファイルが対象となる

    ```bash
    mise exec -- find "path/to/directory/" -name "*.md"
    ```

## 手順

* コマンドは基本的に `npx markdownlint-cli2` を使用する

### ステップ1. markdownlint実行

```bash
mise exec -- npx markdownlint-cli2 --fix path/to/markdown_file.md
```

### ステップ2. 個別対応

* 自動修正されない問題は、Linterの警告内容を確認し、個別に対応を行う
