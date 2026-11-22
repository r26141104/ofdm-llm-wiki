"""節點 N6：檢查內容（整理重點的產出 slides/outline.yaml）。
失敗時的回頭路：
  O1/O2 引用或數字對不上 → 回 N5 改大綱；若 wiki 本身缺這項資料 → 回 N1/N2 ingest
  O3 教學順序錯 → 回 N5 調整投影片順序
  O4/O5 初學者可讀性 → 回 N5 改寫
  O6 學習目標沒涵蓋 → 回 N4 重新查詢 / N5 補投影片
"""
import re
import sys

import yaml

from wikilib import ROOT, load_pages, normalized, numbers

MAX_BULLETS, MAX_CHARS = 5, 60
NEEDS_SRC = {"bullets", "summary"}
SLIDE_SRC = {"table", "timeline"}


def slide_texts(s):
    """依投影片上出現的順序回傳 [(文字, 引用頁)]。"""
    out = [(s.get("title", ""), []), (s.get("subtitle", ""), [])]
    for b in s.get("bullets") or []:
        out.append((b["t"], b.get("src") or []))
    for row in s.get("table") or []:
        out.append((" ".join(map(str, row)), s.get("src") or []))
    for row in s.get("timeline") or []:
        out.append((" ".join(map(str, row)), s.get("src") or []))
    if s.get("note"):
        out.append((s["note"], s.get("src") or []))
    for q in s.get("quiz") or []:
        out.append((q["q"] + " " + " ".join(q["options"]), q.get("src") or []))
    return out


def check(outline_path=ROOT / "slides" / "outline.yaml"):
    pages = load_pages()
    outline = yaml.safe_load(open(outline_path, encoding="utf-8"))["slides"]
    goal = yaml.safe_load(open(ROOT / "slides" / "goal.yaml", encoding="utf-8"))
    issues = {k: [] for k in ["O1 每點有引用且頁面存在", "O2 數字與 wiki 一致", "O3 教學順序符合 prereq",
                              "O4 縮寫第一次出現有解釋", "O5 份量適合一頁", "O6 學習目標都有涵蓋"]}

    abbrs = [row.split("|")[1].strip() for row in pages["glossary"]["body"].splitlines()
             if row.startswith("|") and not row.startswith("|---")]
    abbrs = [a for a in abbrs if re.fullmatch(r"[A-Z]{2,}[A-Z]*", a)]
    seen_abbr, taught = set(), set()

    for s in outline:
        sid, kind = s["id"], s["kind"]
        # O1
        if kind in NEEDS_SRC:
            for b in s.get("bullets") or []:
                if not b.get("src"):
                    issues["O1 每點有引用且頁面存在"].append(f"{sid}「{b['t'][:20]}…」沒有 src")
        if kind in SLIDE_SRC and not s.get("src"):
            issues["O1 每點有引用且頁面存在"].append(f"{sid} 表格／時間軸沒有 src")
        for q in s.get("quiz") or []:
            if not q.get("src"):
                issues["O1 每點有引用且頁面存在"].append(f"{sid} 題目「{q['q'][:15]}…」沒有 src")
        for text, src in slide_texts(s):
            for p in src:
                if p not in pages:
                    issues["O1 每點有引用且頁面存在"].append(f"{sid} 引用不存在的頁面 {p}")
            # O2：這一點裡的每個數字，都要在它引用的 wiki 頁找得到
            if src:
                ref = normalized(" ".join(pages[p]["body"] for p in src if p in pages))
                for n in numbers(text):
                    if n not in ref:
                        issues["O2 數字與 wiki 一致"].append(f"{sid}：「{n}」不在 {src} → {text[:40]}")
            # O4
            for a in abbrs:
                m = re.search(rf"(?<![A-Za-z]){re.escape(a)}(?![A-Za-z])", text)
                if m and a not in seen_abbr:
                    seen_abbr.add(a)
                    after = text[m.end():m.end() + 1]
                    if after not in ("（", "("):
                        issues["O4 縮寫第一次出現有解釋"].append(f"{sid}：「{a}」第一次出現沒有加（全名／中文）→ {text[:30]}")
        # O3
        for c in s.get("concepts") or []:
            if c not in pages:
                issues["O3 教學順序符合 prereq"].append(f"{sid} 的概念 {c} 不存在")
                continue
            for q in pages[c]["meta"].get("prereq") or []:
                if q not in taught and q not in (s.get("concepts") or []):
                    issues["O3 教學順序符合 prereq"].append(f"{sid} 講 {c}，但前置概念 {q} 還沒教")
        taught.update(s.get("concepts") or [])
        # O5
        bl = s.get("bullets") or []
        if len(bl) > MAX_BULLETS:
            issues["O5 份量適合一頁"].append(f"{sid} 有 {len(bl)} 點（上限 {MAX_BULLETS}）")
        for b in bl:
            if len(b["t"]) > MAX_CHARS:
                issues["O5 份量適合一頁"].append(f"{sid} 有一點 {len(b['t'])} 字（上限 {MAX_CHARS}）")

    # O6
    for o in goal["objectives"]:
        if o["id"] not in taught:
            issues["O6 學習目標都有涵蓋"].append(f"目標「{o['goal']}」（{o['id']}）沒有任何投影片")
    return issues


def main():
    issues = check()
    total = sum(len(v) for v in issues.values())
    for k, v in issues.items():
        print(f"  {'PASS' if not v else 'FAIL'}  {k}" + (f"（{len(v)}）" if v else ""))
        for x in v:
            print(f"        - {x}")
    print(f"check_outline：{'通過' if total == 0 else f'{total} 個問題'}")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
