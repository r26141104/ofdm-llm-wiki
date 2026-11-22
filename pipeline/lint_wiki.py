"""節點 N3：Wiki 健康檢查（lint）。任何一項失敗 → 回到 Ingest 修頁面。"""
import re
import sys

from wikilib import (concept_pages, links, load_pages, load_raw, normalized,
                     numbers, topo_order)


def lint():
    pages, raw = load_pages(), load_raw()
    concepts = concept_pages(pages)
    issues = {k: [] for k in ["L1 front matter", "L2 連結", "L3 孤兒頁", "L4 來源 ID",
                              "L5 prereq 圖", "L6 術語表", "L7 數字有來源"]}

    glossary_terms = {row.split("|")[1].strip()
                      for row in pages["glossary"]["body"].splitlines()
                      if row.startswith("|") and not row.startswith("|---")}

    inbound = {pid: set() for pid in pages}
    for pid, pg in pages.items():
        for t in links(pg["body"]):
            if t not in pages:
                issues["L2 連結"].append(f"{pid} → [[{t}]] 不存在")
            else:
                inbound[t].add(pid)

    for pid, pg in concepts.items():
        m = pg["meta"]
        for key in ["title", "sources", "prereq", "terms"]:
            if key not in m:
                issues["L1 front matter"].append(f"{pid} 缺少 {key}")
        if not m.get("sources"):
            issues["L1 front matter"].append(f"{pid} 沒有任何來源")
        if "index" not in inbound[pid]:
            issues["L3 孤兒頁"].append(f"{pid} 沒有列在 index")
        if not (inbound[pid] - {"index", "glossary", "log"}):
            issues["L3 孤兒頁"].append(f"{pid} 沒有被其他內容頁連到")
        for s in m.get("sources") or []:
            if s not in raw:
                issues["L4 來源 ID"].append(f"{pid} 引用不存在的來源 {s}")
        for q in m.get("prereq") or []:
            if q not in concepts:
                issues["L5 prereq 圖"].append(f"{pid} 的 prereq {q} 不是概念頁")
        for t in m.get("terms") or []:
            if t not in glossary_terms:
                issues["L6 術語表"].append(f"{pid} 定義的術語「{t}」不在 glossary")
        # L7：每個數字都要能在宣告的來源原文找到；寫了（推導）的那一行除外
        src_text = normalized(" ".join(raw.get(s, "") for s in m.get("sources") or []))
        for line in pg["body"].splitlines():
            if "推導" in line:
                continue
            for n in numbers(line):
                if n not in src_text:
                    issues["L7 數字有來源"].append(f"{pid}：「{n}」在來源 {m.get('sources')} 找不到 → {line.strip()[:50]}")

    try:
        topo_order(pages, list(concepts))
    except ValueError as e:
        issues["L5 prereq 圖"].append(str(e))
    return issues


def main():
    issues = lint()
    total = sum(len(v) for v in issues.values())
    lines = []
    for k, v in issues.items():
        lines.append(f"  {'PASS' if not v else 'FAIL'}  {k}" + (f"（{len(v)}）" if v else ""))
        lines += [f"        - {x}" for x in v]
    print("\n".join(lines))
    print(f"lint：{'通過' if total == 0 else f'{total} 個問題'}")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
