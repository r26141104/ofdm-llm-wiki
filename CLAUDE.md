# CLAUDE.md — OFDM LLM Wiki 的維護規則（schema）

這個檔案告訴 LLM：這個 wiki 怎麼長、每個操作要做什麼、什麼時候要停下來檢查。

## 三層結構

| 層 | 資料夾 | 誰可以改 | 說明 |
|---|---|---|---|
| 原始資料 | `raw/` | 只能新增，不能修改 | 每篇來源一個檔（S1、S2…），記錄網址、存取日期、擷取重點 |
| Wiki | `wiki/` | LLM 維護 | 概念頁、來源摘要頁、討論紀錄、index、log、glossary |
| 規則 | `CLAUDE.md` | 人與 LLM 一起修訂 | 就是這份檔案 |

## 頁面格式

每個 wiki 頁面開頭都要有 front matter：

```yaml
---
title: 頁面標題
type: concept | source | discussion | meta
sources: [S1, S2]        # concept 頁必填，至少一個
prereq: [page-id, ...]   # concept 頁：理解本頁前要先懂哪些頁（可空）
terms: [縮寫, ...]        # 本頁負責定義的術語（要出現在 glossary.md）
---
```

- 頁內連結一律寫 `[[page-id]]`，page-id 就是檔名（不含 .md）。
- 概念頁的每個數字都必須能在 `raw/` 找到；若是自己算出來的，在數字後加「（推導）」並寫出算式。
- 寫自己的話，不照抄來源句子。

## 操作一：Ingest（先討論、後生成）

1. 把來源擷取重點存到 `raw/Sx-*.md`。
2. **先討論**：在 `wiki/discussions/Dx-*.md` 寫下
   - 這篇來源最重要的 3–5 點是什麼
   - 跟現有 wiki 哪些頁重疊、哪裡衝突或有疑點
   - 決定：要新增／更新哪些頁、哪些內容超出入門範圍先不寫
3. **後生成**：依照討論的決定，建立 `wiki/sources/Sx-*.md` 摘要頁，新增或更新概念頁。
4. 更新 `wiki/index.md`、`wiki/glossary.md`，在 `wiki/log.md` 追加一行。
5. 跑 `python pipeline/lint_wiki.py`，沒過就回到第 3 步修。

## 操作二：Query（為簡報查詢 wiki）

`python pipeline/query_wiki.py slides/goal.yaml` 會依學習目標，沿著 prereq 圖把需要的頁面找齊，
排出「先教什麼、後教什麼」的順序，輸出 `slides/query_result.md`。

## 操作三：整理重點 → 檢查 → 產生簡報

1. 依 `query_result.md` 寫 `slides/outline.yaml`：每一點都要標註 `src`（引用哪個 wiki 頁）。
   **動筆前先讀 query_result.md 最後的「必看 ①②」**（縮寫寫法、來源沒有的內容）。
   這是第 1 次實際執行後加上的規則：第一版大綱的 12 個錯誤全部屬於這兩類。
2. `python pipeline/check_outline.py`：沒過就回到第 1 步修；若是 wiki 本身缺資料，回到 Ingest。
3. `python pipeline/build_slides.py` 產生 `docs/slides.html`。
4. `python pipeline/check_slides.py`：用瀏覽器實際打開每一頁檢查；沒過就回到第 3 步（版面）或第 1 步（內容太多）。
5. **看截圖**（`runs/screens/`）：自動檢查只抓得到「超出畫面」，圖裡的文字互相壓到、標題斷行醜，只有看圖才發現。
   發現的問題寫進 `runs/run-log.md`，再回到第 3 步。

整條流程可以用 `python pipeline/run_pipeline.py` 一次執行，結果會追加到 `runs/run-log.md`。

## 寫給初學者的規則

- 縮寫第一次出現時必須寫出全名或中文（例如「ISI（符號間干擾）」）。
- 每頁投影片最多 5 點，每點最多 60 個字元。
- 每一頁只能用「前面已經教過」的概念（依 prereq 圖檢查）。
