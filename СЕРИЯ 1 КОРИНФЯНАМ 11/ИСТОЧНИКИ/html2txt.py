#!/usr/bin/env python3
"""Convert HTML page to plain-text markdown-ish archive copy.

Usage: python3 html2txt.py <input.html> <output.md> [start_marker] [end_marker]
Extracts main text between optional markers (regex), strips tags, keeps headings.
"""
import re
import sys
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    BLOCK = {"p", "div", "br", "h1", "h2", "h3", "h4", "li", "tr", "blockquote", "td", "th", "section", "article", "ul", "ol"}
    SKIP = {"script", "style", "noscript", "head", "nav", "footer", "form", "iframe"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip_depth = 0
        self.in_skip = False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_depth += 1
            self.in_skip = True
        if not self.in_skip and tag in self.BLOCK:
            self.out.append("\n")
        if not self.in_skip and tag.startswith("h") and len(tag) == 2 and tag[1].isdigit():
            self.out.append("\n## ")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip_depth > 0:
            self.skip_depth -= 1
            if self.skip_depth == 0:
                self.in_skip = False
        if not self.in_skip and tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.in_skip:
            self.out.append(data)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    start_marker = sys.argv[3] if len(sys.argv) > 3 else None
    end_marker = sys.argv[4] if len(sys.argv) > 4 else None
    raw = open(src, encoding="utf-8", errors="replace").read()
    if start_marker:
        m = re.search(start_marker, raw, re.S | re.I)
        if m:
            raw = raw[m.start():]
        else:
            print(f"WARN: start marker not found: {start_marker}", file=sys.stderr)
    if end_marker:
        m = re.search(end_marker, raw, re.S | re.I)
        if m:
            raw = raw[:m.end()]
        else:
            print(f"WARN: end marker not found: {end_marker}", file=sys.stderr)
    p = TextExtractor()
    p.feed(raw)
    text = "".join(p.out)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\s*\n\s*", "\n", text)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"{dst}: {len(text)} chars")


if __name__ == "__main__":
    main()
