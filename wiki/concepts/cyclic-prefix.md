---
title: 循環前綴（Cyclic Prefix, CP）
type: concept
sources: [S1, S2, S5, S6]
prereq: [multipath-isi, ifft-fft]
terms: [CP, 循環前綴]
---

## 一句話
**CP（Cyclic Prefix，循環前綴）**：把 OFDM 符號的**尾端複製一段，貼到開頭**，當作保護區間。接收端收到後把這段丟掉。

## 它做了兩件事
1. **擋住 ISI**：前一個符號的回音只會落在 CP 裡，而 CP 會被丟掉。見 [[multipath-isi]]。
2. **讓等化變成一個乘法**：因為 CP 是符號自己的尾巴，通道的線性卷積在 CP 之後看起來就像**循環卷積**；而循環卷積做 DFT 之後會變成**逐點相乘**。見 [[one-tap-equalization]]。

## 長度條件
CP 的長度至少要等於通道的長度（多路徑延遲擴散）。太短 → 回音漏進有效符號 → ISI 和子載波間干擾又回來了。

## 代價
CP 不帶新資料，是純粹的開銷。以 802.11a 為例，CP 0.8 µs、有效符號 3.2 µs，開銷 = 0.8 /(3.2 + 0.8) = 20%（推導）。見 [[wifi-80211a-example]]。

## 在 5G 裡
CP 長度和子載波間距成反比：15 kHz 時 4.7 µs，240 kHz 時約 0.29 µs。見 [[nr-numerology]]。

## 來源
S1、S2、S5、S6
