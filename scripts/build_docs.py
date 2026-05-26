#!/usr/bin/env python3
"""Build a small static documentation site for the skills repository."""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
SITE_DIR = ROOT / "site"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


CSS = """
:root {
  color-scheme: light dark;
  --bg: #f8fafc;
  --fg: #111827;
  --muted: #4b5563;
  --panel: #ffffff;
  --border: #d1d5db;
  --accent: #0f766e;
  --code-bg: #111827;
  --code-fg: #f9fafb;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #111827;
    --fg: #f9fafb;
    --muted: #d1d5db;
    --panel: #1f2937;
    --border: #374151;
    --accent: #5eead4;
    --code-bg: #030712;
    --code-fg: #f9fafb;
  }
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.55;
}

main {
  max-width: 1120px;
  margin: 0 auto;
  padding: 2rem 1rem 4rem;
}

a {
  color: var(--accent);
}

.topbar {
  border-bottom: 1px solid var(--border);
  background: var(--panel);
}

.topbar-inner {
  max-width: 1120px;
  margin: 0 auto;
  padding: 0.8rem 1rem;
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
}

.brand {
  font-weight: 700;
  color: var(--fg);
  text-decoration: none;
}

.nav {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
}

.hero {
  margin: 2rem 0;
}

.hero p,
.muted {
  color: var(--muted);
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
}

.card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
}

.card h2,
.card h3 {
  margin-top: 0;
}

.meta {
  color: var(--muted);
  font-size: 0.95rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: var(--panel);
  border: 1px solid var(--border);
}

th,
td {
  border-bottom: 1px solid var(--border);
  padding: 0.65rem;
  text-align: left;
  vertical-align: top;
}

pre {
  overflow-x: auto;
  background: var(--code-bg);
  color: var(--code-fg);
  padding: 1rem;
  border-radius: 8px;
}

code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}

:not(pre) > code {
  background: color-mix(in srgb, var(--border) 55%, transparent);
  padding: 0.1rem 0.25rem;
  border-radius: 4px;
}
"""


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}, "\n".join(lines)

    data: dict[str, str] = {}
    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            return data, "\n".join(lines[index + 1 :])
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data, "\n".join(lines)


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


def render_markdown(markdown: str) -> str:
    output: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            output.append("<ul>")
            output.extend(f"<li>{inline_markdown(item)}</li>" for item in list_items)
            output.append("</ul>")
            list_items.clear()

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            if in_code:
                output.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines.clear()
                in_code = False
            else:
                flush_paragraph()
                flush_list()
                in_code = True
            continue

        if in_code:
            code_lines.append(raw_line)
            continue

        if not line.strip():
            flush_paragraph()
            flush_list()
            continue

        if line.startswith("#"):
            flush_paragraph()
            flush_list()
            level = min(len(line) - len(line.lstrip("#")), 6)
            text = line[level:].strip()
            output.append(f"<h{level}>{inline_markdown(text)}</h{level}>")
        elif line.startswith("- "):
            flush_paragraph()
            list_items.append(line[2:].strip())
        elif line.startswith("<!--") or line.startswith("-->"):
            continue
        else:
            paragraph.append(line.strip())

    flush_paragraph()
    flush_list()
    if in_code:
        output.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")

    return "\n".join(output)


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="../index.html">Project Skills</a>
      <nav class="nav">
        <a href="../index.html">Index</a>
        <a href="../skills.html">Skills</a>
        <a href="../contributing.html">Contributing</a>
      </nav>
    </div>
  </header>
  <main>
{body}
  </main>
</body>
</html>
"""


def root_page(title: str, body: str) -> str:
    return page(title, body).replace('href="../', 'href="').replace('src="../', 'src="')


def collect_skills() -> list[dict[str, str]]:
    skills: list[dict[str, str]] = []
    for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        frontmatter, markdown = parse_frontmatter(skill_file)
        name = frontmatter.get("name", skill_file.parent.name)
        skills.append(
            {
                "name": name,
                "description": frontmatter.get("description", ""),
                "license": frontmatter.get("license", ""),
                "path": str(skill_file.relative_to(ROOT)),
                "html": f"skills/{name}.html",
                "markdown": markdown,
            }
        )
    return skills


def build_index(skills: list[dict[str, str]]) -> str:
    cards = "\n".join(
        f"""<article class="card">
  <h3><a href="{skill['html']}">{html.escape(skill['name'])}</a></h3>
  <p>{inline_markdown(skill['description'])}</p>
  <p class="meta">{html.escape(skill['path'])}</p>
</article>"""
        for skill in skills
    )
    return root_page(
        "Project Skills",
        f"""<section class="hero">
  <h1>Project Skills</h1>
  <p>Portable, independently installable skills for AI-assisted scientific software usage, maintenance, CI debugging, documentation, and workflow support.</p>
</section>
<section>
  <h2>Available Skills</h2>
  <div class="grid">
{cards}
  </div>
</section>""",
    )


def build_skills_index(skills: list[dict[str, str]]) -> str:
    rows = "\n".join(
        f"""<tr>
  <td><a href="{skill['html']}"><code>{html.escape(skill['name'])}</code></a></td>
  <td>{inline_markdown(skill['description'])}</td>
  <td><code>{html.escape(skill['license'])}</code></td>
</tr>"""
        for skill in skills
    )
    return root_page(
        "Skills Index",
        f"""<h1>Skills Index</h1>
<p class="muted">Each skill is an independent bundle at <code>skills/&lt;skill-name&gt;/SKILL.md</code>.</p>
<table>
  <thead>
    <tr><th>Skill</th><th>Description</th><th>License</th></tr>
  </thead>
  <tbody>
{rows}
  </tbody>
</table>""",
    )


def build() -> None:
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)

    (SITE_DIR / "assets").mkdir(parents=True)
    (SITE_DIR / "skills").mkdir(parents=True)
    (SITE_DIR / "assets" / "style.css").write_text(CSS.strip() + "\n", encoding="utf-8")

    skills = collect_skills()
    (SITE_DIR / "index.html").write_text(build_index(skills), encoding="utf-8")
    (SITE_DIR / "skills.html").write_text(build_skills_index(skills), encoding="utf-8")

    for skill in skills:
        if not NAME_RE.fullmatch(skill["name"]):
            raise ValueError(f"invalid skill name: {skill['name']}")
        body = f"""<p class="meta"><code>{html.escape(skill['path'])}</code></p>
{render_markdown(skill['markdown'])}"""
        (SITE_DIR / skill["html"]).write_text(page(skill["name"], body), encoding="utf-8")

    for source, target in [
        (ROOT / "README.md", SITE_DIR / "repository.html"),
        (ROOT / "CONTRIBUTING.md", SITE_DIR / "contributing.html"),
        (ROOT / "NOTICE.md", SITE_DIR / "notice.html"),
    ]:
        if source.exists():
            _, markdown = parse_frontmatter(source)
            target.write_text(root_page(source.stem.title(), render_markdown(markdown)), encoding="utf-8")

    print(f"Built documentation site in {SITE_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
