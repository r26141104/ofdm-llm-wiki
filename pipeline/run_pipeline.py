"""把整條 graph 跑一次，並把每個節點的結果追加到 runs/run-log.md。

節點：N3 lint_wiki → N4 query_wiki → N6 check_outline → N7 build_slides → N8 check_slides
（N1 取得資料、N2 ingest、N5 整理重點由 LLM 依 CLAUDE.md 執行，這裡只跑可以自動化的節點與檢查。）
某個節點失敗就停下來，並在紀錄中寫出「應該回到哪個節點」。
"""
import datetime as dt
import io
import json
import sys
from contextlib import redirect_stdout

import build_slides
import check_outline
import check_slides
import lint_wiki
import query_wiki
from wikilib import ROOT

NODES = [
    ("N3 Wiki lint", lint_wiki.main, "N2 Ingest（修 wiki 頁面）"),
    ("N4 查詢 Wiki", query_wiki.main, "N1 取得資料 → N2 Ingest（補缺少的主題）"),
    ("N6 檢查內容", check_outline.main, "N5 整理重點（改 outline.yaml）；若 wiki 缺資料則回 N2"),
    ("N7 產生簡報", build_slides.main, "N5 整理重點（數學式語法錯誤）"),
    ("N8 檢查成品", check_slides.main, "N7 產生簡報（版面）或 N5（內容太多）"),
]


def main(note=""):
    state_file = ROOT / "runs" / "state.json"
    state = json.loads(state_file.read_text()) if state_file.exists() else {"iteration": 0}
    state["iteration"] += 1
    it = state["iteration"]
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    log = [f"\n## 第 {it} 次執行　{now}" + (f"　— {note}" if note else ""), ""]
    ok_all = True
    for name, fn, back in NODES:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = fn()
        out = buf.getvalue().rstrip()
        print(f"[{name}] {'PASS' if code == 0 else 'FAIL'}")
        print(out)
        log.append(f"### {name}：{'✅ PASS' if code == 0 else '❌ FAIL'}")
        log.append("```\n" + out + "\n```")
        if code != 0:
            log.append(f"**→ 回到：{back}**")
            ok_all = False
            break
    if ok_all:
        log.append("**全部節點通過，已輸出 docs/slides.html 與 docs/wiki/。**")
    path = ROOT / "runs" / "run-log.md"
    if not path.exists():
        path.write_text("# 執行與檢查紀錄（由 run_pipeline.py 自動追加）\n", encoding="utf-8")
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n".join(log) + "\n")
    state_file.write_text(json.dumps(state))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main(" ".join(sys.argv[1:])))
