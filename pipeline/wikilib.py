"""共用工具：讀 wiki 頁面、解析 front matter 與 [[連結]]、數字擷取、數學渲染。"""
import json
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
NUM_RE = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?")


def split_front_matter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        meta = yaml.safe_load(text[3:end]) or {}
        body = text[end + 4:].lstrip("\n")
        return meta, body
    return {}, text


def load_pages():
    """回傳 {page_id: {"meta", "body", "path"}}，page_id = 檔名（不含 .md）。"""
    pages = {}
    for p in sorted(WIKI.rglob("*.md")):
        meta, body = split_front_matter(p.read_text(encoding="utf-8"))
        pages[p.stem] = {"meta": meta, "body": body, "path": p}
    return pages


def load_raw():
    """回傳 {"S1": 全文, ...}"""
    out = {}
    for p in sorted(RAW.glob("S*.md")):
        meta, body = split_front_matter(p.read_text(encoding="utf-8"))
        out[meta.get("id", p.stem.split("-")[0])] = body
    return out


def links(text):
    return LINK_RE.findall(text)


def numbers(text):
    """擷取文字裡「有意義」的數字：去掉 [[連結]]、千分位逗號；忽略 < 10 的整數。"""
    text = LINK_RE.sub("", text)
    found = []
    for m in NUM_RE.findall(text):
        n = m.rstrip(",").replace(",", "")
        if not n:
            continue
        if "." not in n and int(n) < 10:
            continue
        found.append(n)
    return found


def normalized(text):
    return text.replace(",", "")


def concept_pages(pages):
    return {k: v for k, v in pages.items() if v["meta"].get("type") == "concept"}


def topo_order(pages, wanted):
    """沿 prereq 圖把 wanted 的所有前置概念找齊，回傳拓撲排序（同層依 index.md 的順序）。"""
    index_order = links(pages["index"]["body"])
    rank = {pid: i for i, pid in enumerate(index_order)}
    need, stack = set(), list(wanted)
    while stack:
        pid = stack.pop()
        if pid in need:
            continue
        need.add(pid)
        stack.extend(pages[pid]["meta"].get("prereq", []) or [])
    order, done = [], set()
    while len(order) < len(need):
        ready = [p for p in need - done
                 if all(q in done for q in (pages[p]["meta"].get("prereq") or []))]
        if not ready:
            raise ValueError("prereq 圖有循環：" + ", ".join(sorted(need - done)))
        nxt = min(ready, key=lambda p: rank.get(p, 999))
        order.append(nxt)
        done.add(nxt)
    return order


# ---------- 數學：用 KaTeX 在建置時轉成 MathML（成品不需要網路） ----------
MATH_RE = re.compile(r"\$\$(.+?)\$\$|\$(.+?)\$", re.S)
_KATEX_JS = r"""
const katex = require('katex');
let s = ''; process.stdin.on('data', d => s += d);
process.stdin.on('end', () => {
  const items = JSON.parse(s);
  const out = items.map(it => {
    try { return {ok: true, html: katex.renderToString(it.tex, {displayMode: it.display, output: 'mathml', throwOnError: true})}; }
    catch (e) { return {ok: false, html: '<span class="math-error">' + it.tex + '</span>', err: String(e.message)}; }
  });
  process.stdout.write(JSON.stringify(out));
});
"""


def render_math_batch(items):
    """items: [(tex, display_bool)] → [(html, error_or_None)]"""
    if not items:
        return []
    payload = json.dumps([{"tex": t, "display": d} for t, d in items])
    res = subprocess.run(["node", "-e", _KATEX_JS], input=payload, capture_output=True,
                         text=True, cwd=Path(__file__).parent, check=True)
    return [(r["html"], None if r["ok"] else r["err"]) for r in json.loads(res.stdout)]


def protect_math(text):
    """把 $..$ 換成佔位符，回傳 (新文字, 佔位符清單)；之後用 restore_math 填回。"""
    found = []

    def sub(m):
        tex = m.group(1) if m.group(1) is not None else m.group(2)
        found.append((tex.strip(), m.group(1) is not None))
        return f"@@MATH{len(found) - 1}@@"

    return MATH_RE.sub(sub, text), found


def restore_math(html, found, errors=None):
    rendered = render_math_batch(found)
    for i, (h, err) in enumerate(rendered):
        if err and errors is not None:
            errors.append((found[i][0], err))
        html = html.replace(f"@@MATH{i}@@", h)
    return html
