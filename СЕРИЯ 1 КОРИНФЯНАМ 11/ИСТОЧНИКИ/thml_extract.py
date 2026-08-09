#!/usr/bin/env python3
"""Extract a work (by workID) from CCEL ThML XML into a clean markdown file.

Usage: python3 thml_extract.py <file.xml> <workID> <out.md> [<title>]
"""
import re
import sys
from html.parser import HTMLParser

class ThmlExtractor(HTMLParser):
    BLOCK = {"p", "div", "br", "h1", "h2", "h3", "h4", "h5", "li", "tr", "blockquote", "div1", "div2", "div3", "table", "ul", "ol", "head"}
    SKIP = {"script", "style", "ThML.head", "electronicEdInfo", "notes"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag == "notes":
            self.skip += 1
        if not self.skip:
            if tag in ("h1", "h2", "h3", "h4"):
                self.out.append("\n\n" + "#" * int(tag[1]) + " ")
            elif tag in ("div1", "div2", "div3"):
                self.out.append("\n\n")
            elif tag in BLOCK if False else (tag in self.BLOCK):
                self.out.append("\n\n")

    def handle_endtag(self, tag):
        if tag == "notes" and self.skip > 0:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def main():
    src, work_id, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    title = sys.argv[4] if len(sys.argv) > 4 else work_id
    raw = open(src, encoding="utf-8", errors="replace").read()
    # cut to the work section
    start = raw.find(f"<workID>{work_id}</workID>")
    if start < 0:
        print(f"ERROR: workID {work_id} not found", file=sys.stderr)
        sys.exit(1)
    # find next workID boundary after this work's head
    body_start = raw.find("<div1", start)
    nxt = re.search(r"<workID>(?!%s\b)[a-z0-9_]+</workID>" % re.escape(work_id), raw[start + 2000:])
    end = raw.find("<div1", start + 2000 + (nxt.start() if nxt else 0)) if nxt else len(raw)
    if nxt:
        # end = position of next work's first div1
        end = start + 2000 + nxt.start()
        end = raw.rfind("<div1", start, end)
    section = raw[body_start:end]
    p = ThmlExtractor()
    p.feed(section)
    text = "".join(p.out)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    header = (
        f"# {title}\n\n"
        f"**Источник:** {src} (CCEL ThML, ANF, public domain)\n"
        f"**Извлечено:** 2026-08-09, скрипт thml_extract.py\n"
        f"**Rights:** PUBLIC DOMAIN\n\n---\n\n"
    )
    with open(dst, "w", encoding="utf-8") as f:
        f.write(header + text)
    print(f"{dst}: {len(text)} chars")


if __name__ == "__main__":
    main()
