#!/usr/bin/env python3
"""Migrate remaining .cursor content into packages/coding-xm3."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

REPO = Path("/Users/eaglesakura/work/eaglesakura.com/pocket-kosodate-hq/repo/agent-skills")
SRC = REPO / ".cursor"
DST = REPO / "packages" / "coding-xm3"
APM = DST / ".apm"

ASSET_INSTALL = (
    "apm_modules/eaglesakura/agent-skills/packages/coding-xm3/.apm/assets/"
)

SKILL_RENAMES = {
    "agent.job-description": "agent-job-description",
    "engineer.software-design": "engineer-software-design",
    "engineer.software-requirement": "engineer-software-requirement",
}

# Map old relative extra paths (from various bases) to {assets}/...
EXTRA_TO_ASSETS = {
    "../extra/coding/design.md": "{assets}/coding/design.md",
    "../../extra/coding/design.md": "{assets}/coding/design.md",
    "../extra/coding/requirements.md": "{assets}/coding/requirements.md",
    "../../extra/coding/requirements.md": "{assets}/coding/requirements.md",
    "../extra/coding.execute/work-orders.md": "{assets}/coding.execute/work-orders.md",
    "../extra/plan/plan-mode.md": "{assets}/plan/plan-mode.md",
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rename_skill_names(text: str) -> str:
    # Longer names first to avoid partial issues (none overlap oddly here)
    for old, new in sorted(SKILL_RENAMES.items(), key=lambda x: -len(x[0])):
        text = text.replace(old, new)
    return text


def replace_extra_links(text: str) -> str:
    for old, new in EXTRA_TO_ASSETS.items():
        # markdown links
        text = text.replace(f"]({old})", f"]({new})")
        # bare path mentions in backticks rarely
        text = text.replace(f"`{old}`", f"`{new}`")
        text = text.replace(old, new)
    return text


def quote_yaml_md_links_in_list(text: str) -> str:
    """Quote unquoted markdown-link list items under metadata for YAML safety."""

    def repl(m: re.Match[str]) -> str:
        indent, item = m.group(1), m.group(2)
        if item.startswith('"') or item.startswith("'"):
            return m.group(0)
        if item.startswith("[") and "](" in item:
            return f'{indent}- "{item}"'
        if item.startswith("`{assets}/"):
            return f'{indent}- "{item}"'
        if item.startswith("{assets}/"):
            return f'{indent}- "`{item}`"'
        return m.group(0)

    return re.sub(r"^([ \t]*)- (.+)$", repl, text, flags=re.M)


def ensure_assets_block(frontmatter: str, assets_rel: str) -> str:
    """Insert metadata.assets if missing; rewrite if present."""
    assets_yaml = (
        "    assets:\n"
        f'        - "[assets/]({assets_rel})"\n'
        f"        - {ASSET_INSTALL}\n"
    )
    if re.search(r"(?m)^\s*assets:\s*$", frontmatter):
        # replace existing assets block (simple: from assets: until next non-indented-more key at same level)
        frontmatter = re.sub(
            r"(?ms)^(?P<indent>[ \t]*)assets:\n(?:(?P=indent)[ \t]+.+\n)+",
            assets_yaml,
            frontmatter,
            count=1,
        )
        return frontmatter

    # insert after metadata: or inside metadata after author
    if re.search(r"(?m)^metadata:\s*$", frontmatter):
        # after metadata line
        frontmatter = re.sub(
            r"(?m)^(metadata:\s*\n)",
            r"\1" + assets_yaml,
            frontmatter,
            count=1,
        )
        return frontmatter

    # no metadata — add before closing ---
    return frontmatter.rstrip() + "\nmetadata:\n" + assets_yaml


def transform_prompt(text: str, assets_rel: str = "../assets/") -> str:
    text = rename_skill_names(text)
    text = replace_extra_links(text)

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]
            # add description from help if missing
            if "description:" not in fm and re.search(r"(?m)^\s*help:", fm):
                help_m = re.search(
                    r"(?ms)^\s*help:\s*>-\s*\n((?:\s+.+\n)+)",
                    fm,
                )
                if help_m:
                    help_body = help_m.group(1)
                    fm = "\ndescription: >-\n" + help_body + fm.lstrip("\n")
            fm = ensure_assets_block(fm, assets_rel)
            # ensure references include {assets} entries already rewritten
            fm = quote_yaml_md_links_in_list(fm)
            # also quote remaining [..](..) in references that weren't caught
            text = "---" + fm + "---" + body
    return text


def transform_agent(text: str, assets_rel: str = "../assets/") -> str:
    text = rename_skill_names(text)
    text = replace_extra_links(text)
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]
            fm = ensure_assets_block(fm, assets_rel)
            fm = quote_yaml_md_links_in_list(fm)
            # convert design template markdown links in body to backtick {assets}
            body = re.sub(
                r"\[詳細設計テンプレート\]\(\{assets\}/coding/design\.md\)",
                "`{assets}/coding/design.md`",
                body,
            )
            body = re.sub(
                r"\[要件定義フォーマット\]\(\{assets\}/coding/requirements\.md\)",
                "`{assets}/coding/requirements.md`",
                body,
            )
            text = "---" + fm + "---" + body
    return text


def transform_skill(text: str, new_name: str, assets_rel: str = "../../assets/") -> str:
    text = rename_skill_names(text)
    text = replace_extra_links(text)
    # force name field
    text = re.sub(r"(?m)^name:\s*.*$", f"name: {new_name}", text, count=1)
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]
            fm = ensure_assets_block(fm, assets_rel)
            fm = quote_yaml_md_links_in_list(fm)
            body = re.sub(
                r"\[詳細設計テンプレート\]\(\{assets\}/coding/design\.md\)",
                "`{assets}/coding/design.md`",
                body,
            )
            body = re.sub(
                r"\[要件定義フォーマット\]\(\{assets\}/coding/requirements\.md\)",
                "`{assets}/coding/requirements.md`",
                body,
            )
            # skill should mention workspace-resolve-file-path for assets
            text = "---" + fm + "---" + body
    return text


def main() -> None:
    if DST.exists():
        shutil.rmtree(DST)
    DST.mkdir(parents=True)

    # apm.yml
    write(
        DST / "apm.yml",
        """name: coding-xm3
version: 0.1.0
description: |
  Coding-Commands（要件→詳細設計→実施）と関連 Sub Agent / SKILL / 共有アセット。
  plan.init・コメント適正化も含む。
author: "@eaglesakura"
license: MIT
type: hybrid
includes: auto
targets:
  - cursor
  - claude
  - copilot
dependencies:
  apm:
    - eaglesakura/agent-skills/packages/armyknife
""",
    )

    write(
        DST / ".gitignore",
        """# APM generated (do not commit producer deploy output)
apm_modules/
apm.lock.yaml
.agents/
.cursor/
.claude/
.codex/
.github/instructions/
.github/agents/
.github/prompts/
.github/skills/
""",
    )

    # --- assets ---
    assets_map = {
        "extra/coding/design.md": "coding/design.md",
        "extra/coding/requirements.md": "coding/requirements.md",
        "extra/coding.execute/work-orders.md": "coding.execute/work-orders.md",
        "extra/plan/plan-mode.md": "plan/plan-mode.md",
    }
    for src_rel, dst_rel in assets_map.items():
        src = SRC / src_rel
        dst = APM / "assets" / dst_rel
        write(dst, src.read_text(encoding="utf-8"))
        print(f"asset {src_rel} -> {dst.relative_to(DST)}")

    # --- skills ---
    for old, new in SKILL_RENAMES.items():
        src_dir = SRC / "skills" / old
        dst_dir = APM / "skills" / new
        for path in src_dir.rglob("*"):
            if path.is_dir():
                continue
            rel = path.relative_to(src_dir)
            dst = dst_dir / rel
            raw = path.read_text(encoding="utf-8")
            if path.name == "SKILL.md":
                raw = transform_skill(raw, new)
            else:
                raw = rename_skill_names(raw)
            write(dst, raw)
            print(f"skill {old}/{rel} -> skills/{new}/{rel}")

    # --- agents ---
    for path in sorted((SRC / "agents").glob("*.md")):
        dst = APM / "agents" / f"{path.stem}.agent.md"
        text = transform_agent(path.read_text(encoding="utf-8"))
        write(dst, text)
        print(f"agent {path.name} -> {dst.relative_to(DST)}")

    # --- prompts ---
    for path in sorted((SRC / "commands").glob("*.md")):
        dst = APM / "prompts" / f"{path.stem}.prompt.md"
        text = transform_prompt(path.read_text(encoding="utf-8"))
        # coding.comment: rewrite cross-package skill reference paths to install layout
        if path.stem == "coding.comment":
            text = text.replace(
                "../../packages/golang/.apm/skills/golang-coding-rules/references/code_comment.md",
                "../../.agents/skills/golang-coding-rules/references/code_comment.md",
            )
            text = text.replace(
                "../../packages/flutter/.apm/skills/flutter-coding-rules/references/code_comment.md",
                "../../.agents/skills/flutter-coding-rules/references/code_comment.md",
            )
        # body: prefer backtick {assets} over markdown links to assets
        text = re.sub(
            r"\[([^\]]+)\]\(\{assets\}/([^)]+)\)",
            r"`{assets}/\2`",
            text,
        )
        # mention resolve skill where assets loaded
        text = text.replace(
            "`{assets}/coding/design.md` をロードする",
            "`{assets}/coding/design.md` を `workspace-resolve-file-path` で解決してからロードする",
        )
        text = text.replace(
            "`{assets}/coding/requirements.md` をロードする",
            "`{assets}/coding/requirements.md` を `workspace-resolve-file-path` で解決してからロードする",
        )
        text = text.replace(
            "`{assets}/coding.execute/work-orders.md`",
            "`{assets}/coding.execute/work-orders.md`",
        )
        write(dst, text)
        print(f"prompt {path.name} -> {dst.relative_to(DST)}")

    print("migration file copy/transform done")


if __name__ == "__main__":
    main()
