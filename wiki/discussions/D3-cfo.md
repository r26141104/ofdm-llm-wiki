---
title: 討論 D3：Ingest S3（載波頻率偏移）之前
type: discussion
---

**來源**：[[S3-wikipedia-cfo]]　**相關現有頁**：[[subcarrier-orthogonality]]、[[pilots-channel-estimation]]

## 這篇最重要的點
1. CFO 的主因是兩端振盪器不同頻，一定存在，不只是都卜勒。
2. 有具體數字：802.11 允許 ±20 ppm → 最壞 ±40 ppm → 5.2 GHz 時約 ±208 kHz。
3. 正規化 CFO = 偏移 / 子載波間距，拆成整數部分與小數部分，兩者效果不同。
4. 殘餘 CFO 容許量：64QAM 約 0.01，QPSK 約 0.03。

## 跟現有頁的關係
- 可以順便做一個好懂的對照（推導）：±208 kHz ÷ 802.11a 的 312.5 kHz ≈ 0.67 個子載波間距，遠大於 0.01 的容許量 → 所以一定要估計並補償。
- `pilots-channel-estimation` 要補一句：導頻也用來追蹤殘餘 CFO 與 SCO。

## 決定
- 新增 `cfo` 頁，prereq = `subcarrier-orthogonality`。
- 估計演算法（Moose、BLUE、匹配濾波）只列名字與一句話，不展開推導——對初學者太深。
