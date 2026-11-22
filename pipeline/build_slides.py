"""節點 N7：產生簡報。slides/outline.yaml → docs/slides.html（單一檔案，可離線開啟）。"""
import html
import sys

import yaml

from figures import FIGS
from wikilib import ROOT, load_pages, load_raw, protect_math, restore_math, split_front_matter

CSS = r"""
:root{--ink:#1d2a3a;--muted:#6b7787;--acc:#0f7c80;--acc2:#d9731a;--soft:#e7eef0;--bg:#fbfaf7;--line:#dfe3e6}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#1d2a3a;overflow:hidden}
body{font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei","Noto Sans CJK TC",system-ui,sans-serif;color:var(--ink)}
#stage{position:absolute;left:50%;top:50%;width:1280px;height:720px;transform-origin:center center}
.slide{position:absolute;inset:0;background:var(--bg);padding:56px 72px 64px;display:none;flex-direction:column}
.slide.active{display:flex}
.slide h2{font-size:42px;margin:0 0 6px;line-height:1.25;letter-spacing:.5px}
.slide h2::after{content:"";display:block;width:64px;height:5px;background:var(--acc);border-radius:3px;margin-top:14px}
.body{flex:1;display:grid;gap:40px;align-items:center;min-height:0;margin-top:22px}
.body.two{grid-template-columns:1.05fr 1fr}.body.one{grid-template-columns:1fr}
ul.pts{list-style:none;margin:0;padding:0}
ul.pts li{font-size:27px;line-height:1.5;margin:0 0 20px;padding-left:30px;position:relative}
ul.pts li::before{content:"";position:absolute;left:4px;top:15px;width:11px;height:11px;border-radius:50%;background:var(--acc)}
.cite{display:inline-block;font-size:14px;line-height:1;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 9px;margin-left:8px;vertical-align:3px;text-decoration:none;white-space:nowrap}
.cite:hover{color:var(--acc);border-color:var(--acc)}
.math{font-size:34px;text-align:center;background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 10px;margin:0 0 24px}
.fig{display:flex;justify-content:center;align-items:center;min-height:0}
.fig svg{width:100%;max-height:470px}
.title-slide{justify-content:center;background:linear-gradient(135deg,#0f7c80 0%,#1d2a3a 100%);color:#fff}
.title-slide h1{font-size:60px;margin:0 0 18px;letter-spacing:2px}
.title-slide .sub{font-size:32px;opacity:.92;margin-bottom:46px}
.title-slide .meta{font-size:19px;opacity:.75;line-height:1.7}
.title-slide .meta a{color:#fff}
table.t{border-collapse:collapse;font-size:25px;width:100%}
table.t td{padding:13px 18px;border-bottom:1px solid var(--line)}
table.t tr td:first-child{font-weight:700;color:var(--acc);white-space:nowrap}
.note{font-size:23px;color:var(--muted);margin-top:22px}
.tl{display:flex;justify-content:space-between;position:relative;margin-top:30px}
.tl::before{content:"";position:absolute;left:0;right:0;top:30px;height:4px;background:var(--line)}
.tl .ev{width:16%;text-align:center;position:relative}
.tl .yr{font-weight:800;font-size:24px;color:var(--acc);background:var(--bg);display:inline-block;padding:0 6px;position:relative}
.tl .dot{width:18px;height:18px;border-radius:50%;background:var(--acc2);margin:12px auto 16px;position:relative}
.tl .tx{font-size:21px;line-height:1.45}
.summary li{font-size:30px}
.quiz{display:grid;grid-template-columns:repeat(3,1fr);gap:26px}
.q{background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px}
.q p{font-size:22px;font-weight:700;margin:0 0 16px;line-height:1.45}
.q button{display:block;width:100%;text-align:left;font:inherit;font-size:20px;margin:0 0 10px;padding:10px 14px;border:1px solid var(--line);border-radius:10px;background:var(--bg);cursor:pointer;color:var(--ink)}
.q button.right{background:#d9efe9;border-color:var(--acc)}.q button.wrong{background:#f8e1d4;border-color:var(--acc2)}
.refs{display:grid;grid-template-columns:1fr 1fr;column-gap:36px}.refs li{font-size:19px;margin-bottom:16px;line-height:1.45}.refs a{color:var(--acc);font-size:15px;word-break:break-all}
.agenda li{font-size:30px}
.spectrum-wrap{width:100%}.spectrum-wrap svg{width:100%}
.slider{font-size:20px;margin-top:6px}.slider input{width:100%;accent-color:var(--acc2)}
.ici{font-size:17px;color:var(--muted);margin-top:4px}
footer{position:absolute;left:72px;right:150px;bottom:20px;display:flex;justify-content:space-between;font-size:15px;color:var(--muted)}
.title-slide footer{color:rgba(255,255,255,.6)}
#bar{position:fixed;left:0;bottom:0;height:5px;background:var(--acc2);transition:width .25s}
#nav{position:fixed;right:18px;bottom:16px;display:flex;gap:8px;z-index:5}
#nav button{width:44px;height:44px;border-radius:50%;border:0;background:rgba(255,255,255,.14);color:#fff;font-size:22px;cursor:pointer}
.math-error{color:#c00;font-family:monospace}
@media print{html,body{overflow:visible;background:#fff}#stage{position:static;transform:none!important}.slide{display:flex!important;position:relative;page-break-after:always;height:720px}#nav,#bar{display:none}}
"""

JS = r"""
const slides=[...document.querySelectorAll('.slide')];let cur=0;
function fit(){const s=Math.min(innerWidth/1280,innerHeight/720);document.getElementById('stage').style.transform=`translate(-50%,-50%) scale(${s})`}
function show(i){cur=Math.max(0,Math.min(slides.length-1,i));slides.forEach((s,j)=>s.classList.toggle('active',j===cur));
 document.getElementById('bar').style.width=((cur+1)/slides.length*100)+'%';history.replaceState(null,'','#'+(cur+1))}
addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key)){show(cur+1);e.preventDefault()}
 if(['ArrowLeft','PageUp'].includes(e.key)){show(cur-1);e.preventDefault()}if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1)});
addEventListener('resize',fit);addEventListener('hashchange',()=>show((+location.hash.slice(1)||1)-1));
function sinc(x){return Math.abs(x)<1e-9?1:Math.sin(Math.PI*x)/(Math.PI*x)}
const PAL=['#0f7c80','#d9731a','#5b6fd6','#c2417a','#5a8f29'];
function drawSpectrum(id,eps){const svg=document.getElementById(id);const W=+svg.dataset.w,H=+svg.dataset.h;
 const f0=-1.6,f1=5.6,y0=-0.3,y1=1.08,L=30,R=W-10,T=14,B=H-34;
 const X=f=>L+(f-f0)/(f1-f0)*(R-L),Y=v=>T+(y1-v)/(y1-y0)*(B-T);let s='';
 s+=`<line x1="${L}" y1="${Y(0)}" x2="${R}" y2="${Y(0)}" stroke="#6b7787"/>`;
 for(let k=0;k<5;k++){s+=`<line x1="${X(k)}" y1="${T}" x2="${X(k)}" y2="${B}" stroke="#c9d0d6" stroke-dasharray="4 4"/>`;
  s+=`<text x="${X(k)}" y="${H-12}" text-anchor="middle" font-size="15" fill="#6b7787">${k+1}Δf</text>`}
 for(let k=0;k<5;k++){let p='';for(let i=0;i<=360;i++){const f=f0+(f1-f0)*i/360;p+=(i?'L':'M')+X(f).toFixed(1)+' '+Y(sinc(f-k-eps)).toFixed(1)}
  s+=`<path d="${p}" fill="none" stroke="${PAL[k]}" stroke-width="2.6" opacity=".9"/>`}
 let ici=0;for(let m=0;m<5;m++){if(m!==2)ici+=sinc(2-m-eps)**2}
 for(let m=0;m<5;m++){const v=sinc(2-m-eps);if(m!==2&&Math.abs(v)>0.004)s+=`<circle cx="${X(2)}" cy="${Y(v)}" r="5" fill="#c00"/>`}
 s+=`<circle cx="${X(2)}" cy="${Y(sinc(-eps))}" r="6" fill="none" stroke="#1d2a3a" stroke-width="2"/>`;
 svg.innerHTML=s;const v=document.getElementById(id+'-v');if(v)v.textContent=eps.toFixed(2);
 const c=document.getElementById(id+'-ici');if(c)c.textContent=ici.toFixed(3)}
document.querySelectorAll('svg.spectrum').forEach(s=>drawSpectrum(s.id,0));
document.querySelectorAll('.q').forEach(q=>{const a=+q.dataset.ans;q.querySelectorAll('button').forEach((b,i)=>b.onclick=()=>{
 q.querySelectorAll('button').forEach((x,j)=>x.classList.toggle('right',j===a));if(i!==a)b.classList.add('wrong')})});
fit();show((+location.hash.slice(1)||1)-1);
"""


def short_title(t):
    for sep in ["（", "("]:
        t = t.split(sep)[0]
    return t.strip()


def main():
    pages, raw_meta = load_pages(), {}
    for p in sorted((ROOT / "raw").glob("S*.md")):
        m, _ = split_front_matter(p.read_text(encoding="utf-8"))
        raw_meta[m["id"]] = m
    goal = yaml.safe_load(open(ROOT / "slides" / "goal.yaml", encoding="utf-8"))
    outline = yaml.safe_load(open(ROOT / "slides" / "outline.yaml", encoding="utf-8"))["slides"]
    found_math, errors = [], []

    def tx(s):
        """文字 → HTML：先保護 $..$，再跳脫 HTML。"""
        s, f = protect_math(str(s))
        base = len(found_math)
        for i in range(len(f)):
            s = s.replace(f"@@MATH{i}@@", f"@@M{base+i}@@")
        found_math.extend(f)
        return html.escape(s).replace("@@M", "@@MATH")

    def cites(src):
        return "".join(f'<a class="cite" href="wiki/{p}.html" target="_blank" title="來自 wiki 頁面 {p}">'
                       f'wiki · {html.escape(short_title(pages[p]["meta"]["title"]))}</a>'
                       for p in (src or []) if p in pages)

    n = len(outline)
    out = []
    for i, s in enumerate(outline, 1):
        kind = s["kind"]
        foot = f'<footer><span>OFDM 是什麼？— LLM Wiki 教學簡報</span><span>{i} / {n}</span></footer>'
        if kind == "title":
            out.append(f'<section class="slide title-slide"><h1>{tx(s["title"])}</h1>'
                       f'<div class="sub">{tx(s.get("subtitle", ""))}</div>'
                       f'<div class="meta">知識來源：OFDM LLM Wiki（{len(raw_meta)} 篇來源、'
                       f'{sum(1 for p in pages.values() if p["meta"].get("type") == "concept")} 個概念頁）'
                       f'　·　<a href="wiki/index.html">打開 Wiki</a><br>'
                       f'對象：{html.escape(goal["audience"])}<br>操作：← → 鍵或右下角按鈕換頁</div>{foot}</section>')
            continue
        head = f'<h2>{tx(s["title"])}</h2>'
        if kind in ("bullets", "agenda", "summary"):
            lis = "".join(f'<li>{tx(b["t"])}{cites(b.get("src"))}</li>' for b in s.get("bullets") or [])
            math = f'<div class="math">@@DISP{len(found_math)}@@</div>' if s.get("math") else ""
            if s.get("math"):
                found_math.append((s["math"], True))
                math = math.replace(f"@@DISP{len(found_math)-1}@@", f"@@MATH{len(found_math)-1}@@")
            cls = {"agenda": "pts agenda", "summary": "pts summary"}.get(kind, "pts")
            left = f'{math}<ul class="{cls}">{lis}</ul>'
            if s.get("figure"):
                body = f'<div class="body two"><div>{left}</div><div class="fig">{FIGS[s["figure"]]()}</div></div>'
            else:
                body = f'<div class="body one"><div>{left}</div></div>'
        elif kind == "table":
            rows = "".join("<tr>" + "".join(f"<td>{tx(c)}</td>" for c in r) + "</tr>" for r in s["table"])
            note = f'<div class="note">{tx(s["note"])}</div>' if s.get("note") else ""
            body = f'<div class="body one"><div><table class="t">{rows}</table>{note}<div class="note">{cites(s.get("src"))}</div></div></div>'
        elif kind == "timeline":
            evs = "".join(f'<div class="ev"><div class="yr">{tx(y)}</div><div class="dot"></div><div class="tx">{tx(t)}</div></div>'
                          for y, t in s["timeline"])
            body = f'<div class="body one"><div><div class="tl">{evs}</div><div class="note" style="margin-top:44px">{cites(s.get("src"))}</div></div></div>'
        elif kind == "quiz":
            qs = ""
            for q in s["quiz"]:
                btns = "".join(f"<button>{tx(o)}</button>" for o in q["options"])
                qs += f'<div class="q" data-ans="{q["answer"]}"><p>{tx(q["q"])}</p>{btns}<div>{cites(q.get("src"))}</div></div>'
            body = f'<div class="body one"><div><p class="note" style="margin:0 0 20px">點選答案，會顯示正確選項。</p><div class="quiz">{qs}</div></div></div>'
        elif kind == "refs":
            lis = "".join(f'<li><b>{k}</b>　{html.escape(m["title"])}<br><a href="{m["url"]}" target="_blank">'
                          f'{html.escape(m["url"].split("//")[1])}</a></li>' for k, m in raw_meta.items())
            acc = sorted({str(m["accessed"]) for m in raw_meta.values()})
            body = (f'<div class="body one"><div><ul class="pts refs">{lis}</ul><div class="note">存取日：{"、".join(acc)}。'
                    f'每頁的「wiki · …」標籤都可以點，會打開對應的 wiki 頁面。</div></div></div>')
        else:
            raise ValueError(f"未知的投影片類型 {kind}")
        out.append(f'<section class="slide" data-id="{s["id"]}">{head}{body}{foot}</section>')

    doc = ("<!DOCTYPE html><html lang=\"zh-Hant\"><head><meta charset=\"utf-8\">"
           "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
           f"<title>{html.escape(goal['title'])}｜OFDM LLM Wiki 教學簡報</title><style>{CSS}</style></head><body>"
           f'<div id="stage">{"".join(out)}</div><div id="bar"></div>'
           '<div id="nav"><button onclick="show(cur-1)" aria-label="上一頁">‹</button>'
           '<button onclick="show(cur+1)" aria-label="下一頁">›</button></div>'
           f"<script>{JS}</script></body></html>")
    doc = restore_math(doc, found_math, errors)
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "slides.html").write_text(doc, encoding="utf-8")
    if errors:
        for t, e in errors:
            print(f"  FAIL  數學式無法解析：{t} → {e}")
        return 1
    print(f"  PASS  產生 docs/slides.html：{n} 頁，數學式 {len(found_math)} 個")
    import build_site
    return build_site.main()


if __name__ == "__main__":
    sys.exit(main())
