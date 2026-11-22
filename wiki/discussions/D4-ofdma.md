---
title: 討論 D4：Ingest S4（OFDMA）之前
type: discussion
---

**來源**：[[S4-wikipedia-ofdma]]　**相關現有頁**：[[ofdm-basics]]、[[applications-history]]

## 這篇最重要的點
1. OFDMA = 把子載波（以及時間）分給不同使用者；OFDM 本身是「一個使用者用全部子載波」。
2. 好處：多人同時傳、延遲穩定、可依通道狀況分配。
3. 代價：對頻率偏移與相位雜訊更敏感。

## 疑點
- 我原本以為 LTE 上行用 SC-FDMA，S4 沒有這樣寫，S5 也沒提 DFT-s-OFDM → 不寫，避免沒有來源的說法。

## 決定
- 新增 `ofdma` 頁，prereq = `ofdm-basics`。
- 在 `applications-history` 補上 Wi-Fi 6（802.11ax）、LTE 下行、5G NR 使用 OFDMA。
