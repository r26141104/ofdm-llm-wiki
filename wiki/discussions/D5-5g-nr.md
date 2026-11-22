---
title: 討論 D5：Ingest S5（5G NR）之前
type: discussion
---

**來源**：[[S5-wikipedia-5g-nr]]　**相關現有頁**：[[subcarrier-orthogonality]]、[[cyclic-prefix]]

## 這篇最重要的點
1. 5G NR 的子載波間距不是固定的：15、30、60、120、240（以及 480、960）kHz，每次加倍。
2. 間距加倍 → slot 長度減半、CP 也變短（15 kHz 時 4.7 µs，240 kHz 時約 0.29 µs）。
3. 這正好呼應 Δf = 1/T_U：間距越大，符號越短。

## 疑點（衝突）
- 來源表格中 960 kHz 的 slot 長度寫 0.01565 ms，但依「每加倍就減半」應為 1/64 = 0.015625 ms。判斷為來源誤植，wiki 寫 0.015625（推導）並註明原文數字。
- 來源沒有寫出 15·2^μ 這個公式，但表格完全符合。wiki 寫成「15 × 2^μ（推導，由表格歸納）」。

## 決定
- 新增 `nr-numerology` 頁，prereq = `subcarrier-orthogonality`、`cyclic-prefix`。
- FR1/FR2 頻段範圍只放在這頁，不放進簡報（對初學者不是重點）。
