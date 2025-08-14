from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


DOCS_SRC = Path("Docs")
CONVERTED_DIR = Path("site_docs/source/converted")


def _slugify(name: str) -> str:
	out = "".join(ch.lower() if ch.isalnum() else "-" for ch in name)
	while "--" in out:
		out = out.replace("--", "-")
	return out.strip("-")


def _read_text_file(p: Path) -> str:
	try:
		return p.read_text(encoding="utf-8", errors="ignore")
	except Exception:
		return p.read_text(encoding="latin-1", errors="ignore")


def _write_markdown_with_frontmatter(title: str, body: str, source_path: Path) -> str:
	front = [
		"---\n",
		f"title: {title}\n",
		f"source_path: {source_path.as_posix()}\n",
		f"ingested_at: {datetime.now().isoformat()}\n",
		"tags: []\n",
		"---\n\n",
	]
	return "".join(front) + body


def ingest() -> None:
	CONVERTED_DIR.mkdir(parents=True, exist_ok=True)
	index_lines = ["# Converted Sources\n\n"]
	for p in sorted(DOCS_SRC.iterdir()):
		if p.is_dir():
			continue
		# Only convert simple text-like files now; PDFs/DOCs skipped in this scaffold
		ext = p.suffix.lower()
		if ext in {".txt", ".md", ""}:
			title = p.stem.replace("-", " ").title()
			slug = _slugify(p.stem)
			outfile = CONVERTED_DIR / f"{slug}.md"
			if p.suffix.lower() == ".md":
				content = _read_text_file(p)
				md = _write_markdown_with_frontmatter(title, content, p)
				outfile.write_text(md, encoding="utf-8")
			elif p.suffix.lower() in {".txt", ""}:
				content = _read_text_file(p)
				md = _write_markdown_with_frontmatter(title, f"``\n{content}\n``\n", p)
				outfile.write_text(md, encoding="utf-8")
			else:
				# copy as-is (fallback)
				shutil.copy2(p, outfile)
			index_lines.append(f"- [{title}]({slug}.md)\n")

	# Write/update index
	(CONVERTED_DIR / "index.md").write_text("".join(index_lines), encoding="utf-8")


if __name__ == "__main__":
	ingest()


