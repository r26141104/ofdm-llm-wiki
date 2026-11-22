---
title: 實例：IEEE 802.11a 的 OFDM 參數
type: concept
sources: [S1]
prereq: [subcarrier-orthogonality, cyclic-prefix]
terms: [802.11a]
---

## 參數表
| 參數 | 值 |
|---|---|
| FFT 大小 | 64 |
| 實際使用的子載波 | 52 |
| 有效符號長度 $T_U$ | 3.2 µs |
| 保護區間（CP） | 0.8 µs（= $T_U$ 的 1/4） |
| 子載波間距 | 312.5 kHz |
| 通道寬度 | 20 MHz（= 64 × 312.5 kHz） |
| 子載波調變 | BPSK、QPSK、16-QAM、64-QAM |
| 資料率 | 6–54 Mbit/s |

## 用參數驗證概念
- 正交條件：1 / 3.2 µs = 312.5 kHz ✔（見 [[subcarrier-orthogonality]]）
- 一個完整 OFDM 符號 = 3.2 + 0.8 = 4.0 µs（推導）
- CP 開銷 = 0.8 / 4.0 = 20%（推導）（見 [[cyclic-prefix]]）

## 注意
來源沒有說 52 個子載波中資料與導頻各幾個，這裡不寫。

## 來源
S1
