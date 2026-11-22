---
title: OFDM 基本概念
type: concept
sources: [S1, S6]
prereq: [multipath-isi]
terms: [OFDM, 子載波, QAM]
---

## 一句話
**OFDM（Orthogonal Frequency-Division Multiplexing，正交分頻多工）**：把一條高速資料流拆成很多條低速資料流，每一條放在一個**子載波**上同時傳送。

## 重點
- 每個子載波各自用一般的調變方式，例如 **QAM（Quadrature Amplitude Modulation，正交振幅調變）** 或 PSK。
- 在同樣頻寬下，總資料率和單載波差不多，但每個子載波的符號變長，對 [[multipath-isi]] 強很多。
- 它是 FDM 的一種，但子載波的頻譜**彼此重疊**——能重疊而不互相干擾，靠的是 [[subcarrier-orthogonality]]。
- 每個窄子載波內，通道衰落近似平坦，所以等化很簡單（見 [[one-tap-equalization]]）。

## 比喻
一條很快的單線道（單載波）換成很多條慢車道並排（多載波）。每台車慢慢開，前面的車揚起的灰塵（回音）就不會蓋到後面的車。

## 相關
[[ifft-fft]]、[[cyclic-prefix]]、[[ofdma]]、[[applications-history]]

## 來源
S1、S6
