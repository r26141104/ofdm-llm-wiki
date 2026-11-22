---
id: S4
title: Orthogonal frequency-division multiple access（Wikipedia）
url: https://en.wikipedia.org/wiki/Orthogonal_frequency-division_multiple_access
accessed: 2026-11-22
license: CC BY-SA 4.0
---

# S4 擷取重點（以自己的話整理）

## 是什麼
- OFDMA 是 OFDM 的多使用者版本：把子載波分成好幾組，分給不同使用者，讓多個低速使用者同時傳。
- 資源在「時間（OFDM 符號）× 頻率（子載波）」兩個維度上切分與分配。

## 優點
- 多個低速使用者可同時傳輸。
- 低速使用者可以低功率連續傳，不必用高功率短脈衝。
- 延遲較短、較穩定。
- 子載波分散在整個頻帶，有頻率分集。
- 依通道回報調整子載波分配，可對抗衰落與窄頻干擾。
- 每個使用者分到的子載波數不同，可提供不同服務品質。

## 缺點
- 對頻率偏移與相位雜訊更敏感。
- 鄰近細胞的同頻干擾比 CDMA 難處理。
- 快速通道回報與動態分配比較複雜。

## 使用的系統
- WiMAX（IEEE 802.16 行動版）
- Wi-Fi 6/6E（IEEE 802.11ax）
- LTE 下行
- 5G NR 上下行
