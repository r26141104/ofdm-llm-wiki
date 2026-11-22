---
title: 用 IFFT／FFT 實作 OFDM
type: concept
sources: [S1, S6]
prereq: [subcarrier-orthogonality]
terms: [IFFT, FFT]
---

## 一句話
發射端用 **IFFT（Inverse Fast Fourier Transform，反快速傅立葉轉換）** 一次產生所有子載波疊加後的時域波形；接收端用 **FFT（快速傅立葉轉換）** 一次把所有子載波分開。

## 發射端流程
1. 位元 → 分成平行串流 → 各自對應成 QAM／PSK 符號 $X_k$。
2. 把 $X_k$ 放到等間距的頻率格上，做 N 點 IFFT → N 個時域樣本 = 一個 OFDM 符號。
3. 加上 [[cyclic-prefix]] → DAC → 升頻送出。

## 接收端流程
1. 降頻 → ADC → 丟掉 CP。
2. N 點 FFT → 得到每個子載波上的 $Y_k$。
3. 每個子載波各自等化與判斷（見 [[one-tap-equalization]]）→ 還原位元。

## 為什麼這很重要
如果不用 IFFT，就要 N 組獨立的振盪器與濾波器；IFFT／FFT 讓「很多子載波」變成一個數位運算，實作成本大幅下降。這個想法在 1971 年由 Weinstein 與 Ebert 提出（見 [[applications-history]]）。

## 來源
S1、S6
