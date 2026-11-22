---
title: OFDM LLM Wiki — 索引
type: meta
---

這是一個以 **OFDM（正交分頻多工）** 為主題的 LLM Wiki：由 LLM 讀取 6 篇來源、先討論後生成，維護成互相連結的 markdown 頁面。規則見 `CLAUDE.md`，變更紀錄見 [[log]]，術語見 [[glossary]]。

## 概念頁（建議閱讀順序）

| 頁面 | 一句話 | 來源數 |
|---|---|---|
| [[multipath-isi]] | 回音疊到下一個符號 = ISI | 2 |
| [[ofdm-basics]] | 一條快車道拆成很多條慢車道 | 2 |
| [[subcarrier-orthogonality]] | Δf = 1/T_U，重疊但不干擾 | 2 |
| [[ifft-fft]] | 一次 IFFT 產生所有子載波 | 2 |
| [[cyclic-prefix]] | 尾巴貼到頭：擋 ISI、讓等化變乘法 | 4 |
| [[one-tap-equalization]] | 每個子載波除以一個複數 | 3 |
| [[pilots-channel-estimation]] | 用已知符號估出通道 | 3 |
| [[wifi-80211a-example]] | 用 802.11a 的真實數字驗證 | 1 |
| [[papr]] | 波形尖峰讓功率放大器很辛苦 | 1 |
| [[cfo]] | 頻率偏一點，正交就壞掉 | 2 |
| [[ofdma]] | 把子載波分給多個使用者 | 2 |
| [[nr-numerology]] | 5G 用可調的子載波間距 | 1 |
| [[applications-history]] | 從 1966 到 5G | 4 |

## 來源摘要頁

| ID | 頁面 | 討論紀錄 |
|---|---|---|
| S1 | [[S1-wikipedia-ofdm]] | [[D1-ofdm-overview]] |
| S2 | [[S2-wikipedia-cyclic-prefix]] | [[D2-cyclic-prefix]] |
| S3 | [[S3-wikipedia-cfo]] | [[D3-cfo]] |
| S4 | [[S4-wikipedia-ofdma]] | [[D4-ofdma]] |
| S5 | [[S5-wikipedia-5g-nr]] | [[D5-5g-nr]] |
| S6 | [[S6-mathworks-ofdm]] | [[D6-mathworks]] |
