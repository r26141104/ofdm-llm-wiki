"""把 wiki/ 的 markdown 轉成 docs/wiki/*.html，並產生 docs/index.html 首頁（給 GitHub Pages 用）。"""
import html
import re
import sys

import markdown

from wikilib import LINK_RE, ROOT, load_pages, protect_math, restore_math

CSS = """
body{font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;max-width:860px;margin:0 auto;padding:28px 22px 80px;color:#1d2a3a;line-height:1.75;background:#fbfaf7}
a{color:#0f7c80}nav{font-size:14px;margin-bottom:24px;color:#6b7787}nav a{margin-right:14px}
h1{font-size:30px;border-bottom:4px solid #0f7c80;padding-bottom:8px}h2{font-size:22px;margin-top:30px}
table{border-collapse:collapse;margin:12px 0}td,th{border:1px solid #dfe3e6;padding:6px 12px}th{background:#e7eef0}
.meta{font-size:14px;color:#6b7787;background:#fff;border:1px solid #dfe3e6;border-radius:10px;padding:10px 14px}
code{background:#e7eef0;padding:1px 5px;border-radius:4px}math[display=block]{margin:14px 0;font-size:1.25em}
.hero{background:linear-gradient(135deg,#0f7c80,#1d2a3a);color:#fff;border-radius:18px;padding:34px}
.hero a{color:#fff;font-weight:700}.cards{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:22px}
.card{background:#fff;border:1px solid #dfe3e6;border-radius:14px;padding:18px}
"""


def page_html(title, body, depth=1):
    up = "../" * depth
    nav = (f'<nav><a href="{up}index.html">首頁</a><a href="{up}wiki/index.html">Wiki 索引</a>'
           f'<a href="{up}wiki/glossary.html">術語表</a><a href="{up}wiki/log.html">變更紀錄</a>'
           f'<a href="{up}slides.html">教學簡報</a></nav>')
    return (f'<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>'
            f'<style>{CSS}</style></head><body>{nav}{body}</body></html>')


def main():
    pages = load_pages()
    outdir = ROOT / "docs" / "wiki"
    outdir.mkdir(parents=True, exist_ok=True)
    for pid, pg in pages.items():
        m = pg["meta"]

        def link(mt):
            t = mt.group(1)
            title = pages[t]["meta"].get("title", t) if t in pages else t
            return f"[{title.split('（')[0]}]({t}.html)"

        text, found = protect_math(LINK_RE.sub(link, pg["body"]))
        body = markdown.markdown(text, extensions=["tables", "fenced_code"])
        info = []
        if m.get("sources"):
            info.append("來源：" + "、".join(m["sources"]))
        if m.get("prereq") is not None and m.get("type") == "concept":
            info.append("前置概念：" + ("、".join(f'<a href="{q}.html">{q}</a>' for q in m["prereq"]) or "無"))
        if m.get("url"):
            info.append(f'原始網址：<a href="{m["url"]}">{m["url"]}</a>')
        meta = f'<div class="meta">類型：{m.get("type", "")}　{"　".join(info)}</div>' if info or m.get("type") else ""
        doc = page_html(m.get("title", pid), f"<h1>{html.escape(m.get('title', pid))}</h1>{meta}{body}")
        (outdir / f"{pid}.html").write_text(restore_math(doc, found), encoding="utf-8")

    n_concept = sum(1 for p in pages.values() if p["meta"].get("type") == "concept")
    home = f"""
<div class="hero"><h1 style="border:0;color:#fff;margin:0">OFDM LLM Wiki</h1>
<p>以「正交分頻多工（OFDM）」為主題，由 LLM 讀取 6 篇資料、先討論後生成的知識庫，並用它產生一份教學 HTML 簡報。</p></div>
<div class="cards">
<div class="card"><h2 style="margin-top:0">📚 Wiki</h2><p>{n_concept} 個概念頁、6 個來源摘要頁、6 份討論紀錄。</p><a href="wiki/index.html">打開 Wiki 索引 →</a></div>
<div class="card"><h2 style="margin-top:0">🖥️ 教學簡報</h2><p>「OFDM 是什麼？」給沒學過通訊的人，每一點都連回 wiki 頁面。</p><a href="slides.html">打開簡報 →</a></div>
</div>"""
    (ROOT / "docs" / "index.html").write_text(page_html("OFDM LLM Wiki", home, depth=0), encoding="utf-8")
    print(f"  PASS  產生 docs/wiki/（{len(pages)} 頁）與 docs/index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
