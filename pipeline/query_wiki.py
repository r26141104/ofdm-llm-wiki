"""節點 N4：查詢 Wiki。依學習目標沿 prereq 圖找齊頁面、排出教學順序，輸出 slides/query_result.md。
若某個目標在 wiki 找不到對應頁 → 回到「取得資料 / Ingest」。"""
import re
import sys

import yaml
from pathlib import Path

from wikilib import ROOT, load_pages, topo_order


def main(goal_path=ROOT / "slides" / "goal.yaml", out_path=None):
    out_path = out_path or ROOT / "slides" / "query_result.md"
    goal = yaml.safe_load(open(goal_path, encoding="utf-8"))
    pages = load_pages()
    wanted = [o["id"] for o in goal["objectives"]]
    missing = [w for w in wanted if w not in pages]
    if missing:
        print("FAIL  以下學習目標在 wiki 沒有頁面，需要先 ingest 資料：", ", ".join(missing))
        return 1

    order = topo_order(pages, wanted)
    extra = [p for p in order if p not in wanted]
    out = [f"# 查詢結果：{goal['title']}", "",
           f"- 對象：{goal['audience']}",
           f"- 學習目標 {len(wanted)} 項；依 prereq 圖補上的前置／延伸頁：{', '.join(extra) or '無'}",
           "", "## 建議教學順序（拓撲排序）", ""]
    for i, pid in enumerate(order, 1):
        pg = pages[pid]
        m = pg["meta"]
        out.append(f"### {i}. {m['title']}  `[[{pid}]]`")
        out.append(f"- 前置：{', '.join(m.get('prereq') or []) or '無'}　來源：{', '.join(m['sources'])}")
        body = pg["body"].split("## 來源")[0]
        facts = [ln.strip() for ln in body.splitlines()
                 if ln.strip().startswith(("- ", "1.", "2.", "3.", "$$", "|"))][:8]
        out += ["- 重點：" ] + [f"  {f}" for f in facts]
        out.append("")
    # ---- 第 2 版新增：把檢查往前移到「查詢」這一步 ----
    # (1) 術語：列出這次會用到的縮寫，以及第一次出現時該怎麼寫（避免 N6 的 O4 錯誤）
    rows = [r.split("|")[1:4] for r in pages["glossary"]["body"].splitlines()
            if r.startswith("|") and not r.startswith("|---")][1:]
    # 第 3 版：不只列「這些頁面負責定義的術語」，也列「這些頁面內文有提到的縮寫」
    # （第 7 次執行發現：5G 頁內文提到 LTE，但 LTE 是在別頁定義的，清單漏列）
    terms_used = {t for pid in order for t in (pages[pid]["meta"].get("terms") or [])}
    text = " ".join(pages[pid]["body"] for pid in order)
    terms_used |= {a.strip() for a, _, _ in rows
                   if re.search(rf"(?<![A-Za-z]){re.escape(a.strip())}(?![A-Za-z])", text)}
    out += ["## 寫大綱前必看 ①：縮寫第一次出現要這樣寫", "",
            "| 縮寫 | 第一次出現時寫成 |", "|---|---|"]
    out += [f"| {a.strip()} | {a.strip()}（{c.strip()}） |" for a, b, c in rows
            if a.strip() in terms_used and a.strip().isascii() and a.strip().isupper()]
    # 第 3 版：名字互相包含的縮寫要特別提醒（第 7 次執行發現：解釋了 IFFT，就以為 FFT 也解釋過）
    listed = sorted(a.strip() for a, _, _ in rows
                    if a.strip() in terms_used and a.strip().isascii() and a.strip().isupper())
    pairs = [(a, b) for a in listed for b in listed if a != b and a in b]
    if pairs:
        out += ["", "⚠ 以下縮寫名字互相包含，但要**各自**在第一次出現時解釋：" +
                "、".join(f"{b} 和 {a}" for a, b in pairs)]
    # (2) 地雷：討論時決定「來源沒有、不要寫」的內容（避免 N6 的 O2 錯誤）
    out += ["", "## 寫大綱前必看 ②：來源沒有、不要寫的內容", ""]
    for pid, pg in pages.items():
        if pg["meta"].get("type") == "source":
            for ln in pg["body"].splitlines():
                if "可信度備註" in ln:
                    out.append(f"- {pid}：{ln.split('**', 2)[-1].strip('：: ')}")
    Path(out_path).write_text("\n".join(out), encoding="utf-8")
    print(f"PASS  找到 {len(order)} 個頁面，教學順序：{' → '.join(order)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
