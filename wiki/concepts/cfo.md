---
title: 載波頻率偏移（CFO）
type: concept
sources: [S1, S3]
prereq: [subcarrier-orthogonality]
terms: [CFO, ICI]
---

## 一句話
**CFO（Carrier Frequency Offset，載波頻率偏移）**：接收端振盪器和發射端不完全同頻，整個訊號在頻域被平移一點點。

## 為什麼一定會有
- 兩個振盪器不可能完全一樣快——即使完全不動也會有 CFO。
- 移動造成的都卜勒效應也會產生 CFO（通常比振盪器誤差小）。

## 有多大
- IEEE 802.11 允許每個振盪器 ±20 ppm → 收發兩端合起來最壞 ±40 ppm。
- 在 5.2 GHz：約 ±208 kHz。
- 和 802.11a 的子載波間距 312.5 kHz 相比：208 / 312.5 ≈ 0.67 個間距（推導）。

## 對 OFDM 的影響
- 子載波平移後，峰值不再對準其他子載波的零點 → 正交性被破壞 → **ICI（Inter-Carrier Interference，子載波間干擾）**。
- 正規化 CFO $\varepsilon$ = 頻率偏移 ÷ 子載波間距，拆成**整數部分**（子載波索引整個平移）與**小數部分**（振幅衰減、相位旋轉、ICI）。
- 補償後剩下的殘餘 CFO 要很小：64QAM 約 0.01，QPSK 約 0.03。

## 怎麼處理（只列名字）
- Moose 的 ML 估計（估小數部分）、BLUE 估計、用長 preamble 做匹配濾波（估整數部分）。
- 殘餘 CFO 用導頻追蹤（見 [[pilots-channel-estimation]]）。

## 來源
S1、S3
