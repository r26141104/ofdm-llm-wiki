---
title: 5G NR 的子載波間距（Numerology）
type: concept
sources: [S5]
prereq: [subcarrier-orthogonality, cyclic-prefix]
terms: [numerology, NR]
---

## 一句話
5G **NR（New Radio）** 不只用一種子載波間距，而是 15 kHz × 2^μ（推導，由來源表格歸納）：間距越大，符號越短、slot 越短。

## 表格
| μ | 子載波間距 | slot 長度 | 頻段 |
|---|---|---|---|
| 0 | 15 kHz | 1 ms | FR1（和 LTE 相同） |
| 1 | 30 kHz | 0.5 ms | FR1 |
| 2 | 60 kHz | 0.25 ms | FR1、FR2 |
| 3 | 120 kHz | 0.125 ms | FR2 |
| 4 | 240 kHz | 0.0625 ms | FR2（只用於搜尋與量測） |

（480、960 kHz 也在表中；960 kHz 原文寫 0.01565 ms，依加倍減半規律應為 0.015625 ms（推導）。）

## 為什麼要這樣設計
- 由 [[subcarrier-orthogonality]]：$\Delta f = 1/T_U$，間距加倍 → 符號長度減半 → 延遲更低。
- [[cyclic-prefix]] 也跟著變短：15 kHz 時 4.7 µs，240 kHz 時約 0.29 µs。
- 低頻、大範圍覆蓋（延遲擴散長）→ 用小間距、長 CP；高頻、低延遲應用 → 用大間距。

## 頻段
- FR1：410 MHz – 7,125 MHz
- FR2：24,250 MHz – 71,000 MHz

## 來源
S5
