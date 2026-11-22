"""節點 N8：檢查成品。用真的瀏覽器打開 docs/slides.html，一頁一頁檢查並截圖。
失敗時：P2 版面溢出 → 回 N5 刪減內容或 N7 調版面；P3 數學式 → 回 N5；P4 連結 → 回 N7；P5 → 回 N7。"""
import sys
from pathlib import Path

import yaml
from playwright.sync_api import sync_playwright

from wikilib import ROOT

CHROME = "/usr/bin/google-chrome"

MEASURE = r"""
(idx) => {
  show(idx);
  const s = document.querySelectorAll('.slide')[idx];
  const sr = s.getBoundingClientRect();
  const bad = [];
  s.querySelectorAll('.body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    if (r.bottom > sr.bottom - 46 || r.right > sr.right - 20 || r.left < sr.left + 20) {
      const t = (el.innerText || el.tagName).trim().slice(0, 24);
      bad.push(`${el.tagName.toLowerCase()}「${t}」超出 ${Math.round(Math.max(r.bottom - (sr.bottom - 46), r.right - (sr.right - 20), 0))}px`);
    }
  });
  const body = s.querySelector('.body');
  if (body && body.scrollHeight > body.clientHeight + 2) bad.unshift(`內容高度 ${body.scrollHeight}px > 可用 ${body.clientHeight}px`);
  return {bad: [...new Set(bad)].slice(0, 4), mathErr: s.querySelectorAll('.math-error').length,
          links: [...s.querySelectorAll('a[href]')].map(a => a.getAttribute('href'))};
}
"""


def main():
    outline = yaml.safe_load(open(ROOT / "slides" / "outline.yaml", encoding="utf-8"))["slides"]
    shots = ROOT / "runs" / "screens"
    shots.mkdir(parents=True, exist_ok=True)
    issues = {k: [] for k in ["P1 頁數正確", "P2 每頁內容不超出畫面", "P3 數學式正常顯示",
                              "P4 wiki 連結有效", "P5 沒有 JavaScript 錯誤"]}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        pg = br.new_page(viewport={"width": 1280, "height": 720})
        pg.on("pageerror", lambda e: issues["P5 沒有 JavaScript 錯誤"].append(str(e)))
        pg.goto((ROOT / "docs" / "slides.html").as_uri())
        pg.wait_for_timeout(400)
        n = pg.evaluate("document.querySelectorAll('.slide').length")
        if n != len(outline):
            issues["P1 頁數正確"].append(f"HTML 有 {n} 頁，大綱有 {len(outline)} 頁")
        for i in range(n):
            r = pg.evaluate(MEASURE, i)
            sid = outline[i]["id"] if i < len(outline) else f"#{i+1}"
            for b in r["bad"]:
                issues["P2 每頁內容不超出畫面"].append(f"{sid}：{b}")
            if r["mathErr"]:
                issues["P3 數學式正常顯示"].append(f"{sid}：{r['mathErr']} 個數學式錯誤")
            for h in r["links"]:
                if h.startswith("wiki/") and not (ROOT / "docs" / h).exists():
                    issues["P4 wiki 連結有效"].append(f"{sid}：{h} 不存在")
            pg.wait_for_timeout(120)
            pg.screenshot(path=str(shots / f"{i+1:02d}-{sid}.png"))
        br.close()
    total = sum(len(v) for v in issues.values())
    for k, v in issues.items():
        print(f"  {'PASS' if not v else 'FAIL'}  {k}" + (f"（{len(v)}）" if v else ""))
        for x in v:
            print(f"        - {x}")
    print(f"check_slides：{'通過' if total == 0 else f'{total} 個問題'}（截圖在 runs/screens/）")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
