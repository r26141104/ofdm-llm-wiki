# OFDM LLM Wiki — 用 LLM Wiki 做一份教學 HTML 簡報

以「OFDM（正交分頻多工）」為主題的 LLM Wiki（Karpathy 的 LLM Wiki 模式：raw → wiki → schema），
並用這個 wiki 當唯一的知識來源，產生給初學者的教學簡報「OFDM 是什麼？」。

- 網站首頁：`docs/index.html`
- Wiki：`docs/wiki/index.html`（markdown 原檔在 `wiki/`）
- 教學簡報：`docs/slides.html`（← → 換頁；每一點都有連回 wiki 的標籤）
- 維護規則：`CLAUDE.md`
- 執行與檢查紀錄：`runs/run-log.md`，每頁截圖在 `runs/screens/`

## 資料夾

```
raw/            6 篇來源的擷取重點（S1–S6），只新增不修改
wiki/
  discussions/  每篇來源 ingest 前的討論紀錄（先討論）
  sources/      來源摘要頁（後生成）
  concepts/     13 個概念頁
  index.md  glossary.md  log.md
slides/         goal.yaml（學習目標）→ query_result.md（查詢結果）→ outline.yaml（整理重點）
pipeline/       各節點的程式（lint、查詢、檢查、產生、瀏覽器檢查、整條流程）
docs/           產生出來的網站（GitHub Pages 用這個資料夾）
runs/           每次執行的紀錄與截圖
```

## 重新執行整條流程

```bash
pip install pyyaml markdown numpy playwright
cd pipeline && npm install          # 安裝 KaTeX（數學式在建置時轉成 MathML，成品不需網路）
python run_pipeline.py "這次改了什麼"
```

`check_slides.py` 預設用 `/usr/bin/google-chrome`，Windows 請改成自己的 Chrome 路徑。

## 發布到 GitHub Pages

1. 在 GitHub 建立 repo（例如 `ofdm-llm-wiki`），把整個資料夾推上去（`pipeline/node_modules` 不用上傳）。
2. Settings → Pages → Source 選 `Deploy from a branch`，Branch 選 `main`、資料夾選 `/docs`。
3. 網址：`https://<帳號>.github.io/ofdm-llm-wiki/`，簡報在 `.../slides.html`。
