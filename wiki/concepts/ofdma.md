---
title: OFDMA（多使用者 OFDM）
type: concept
sources: [S4, S6]
prereq: [ofdm-basics]
terms: [OFDMA]
---

## 一句話
**OFDMA（Orthogonal Frequency-Division Multiple Access，正交分頻多重存取）**：把子載波（以及時間）切成小塊，分給不同使用者同時使用。

## 和 OFDM 的差別
- OFDM：一個時間點，全部子載波都給同一個使用者。
- OFDMA：資源是一張「時間 × 頻率」的格子，每個使用者分到其中幾格。
- 例：LTE 的資源塊是 12 個子載波 × 14 個符號。

## 好處
- 很多低速使用者可以同時傳，延遲較短、較穩定。
- 依各使用者的通道狀況分配子載波，能避開衰落。
- 分到的子載波數不同，就能提供不同的服務品質。

## 代價
- 對頻率偏移與相位雜訊更敏感（見 [[cfo]]）。
- 分配與通道回報比較複雜。

## 誰在用
LTE 下行、5G NR 上下行、Wi-Fi 6（IEEE 802.11ax）、WiMAX。

## 來源
S4、S6
