---
id: S5
title: 5G NR（Wikipedia）
url: https://en.wikipedia.org/wiki/5G_NR
accessed: 2026-11-22
license: CC BY-SA 4.0
---

# S5 擷取重點（以自己的話整理）

## 波形
- 5G NR 以 OFDM 為基礎，和 4G LTE 用同一種基本波形。
- 循環前綴長度與子載波間距成反比：15 kHz 時 4.7 µs，240 kHz 時約 4.7/16 ≈ 0.29 µs。
- 60 kHz 可用一般 CP 或延伸 CP。

## 子載波間距與 slot 長度
| 間距 (kHz) | slot 長度 (ms) | 頻段 |
|---|---|---|
| 15 | 1 | FR1（與 LTE 相同） |
| 30 | 0.5 | FR1 |
| 60 | 0.25 | FR1 與 FR2 |
| 120 | 0.125 | FR2 |
| 240 | 0.0625 | FR2（只用於搜尋與量測） |
| 480 | 0.03125 | FR2 |
| 960 | 0.01565（原文數字） | FR2 |

- 間距每加倍，slot 長度減半。
- 較大的間距可降低延遲，也適合高頻段。

## 頻段
- FR1：410 MHz – 7,125 MHz
- FR2：24,250 MHz – 71,000 MHz
