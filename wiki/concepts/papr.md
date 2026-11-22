---
title: 峰均功率比（PAPR）
type: concept
sources: [S1]
prereq: [ifft-fft]
terms: [PAPR]
---

## 一句話
**PAPR（Peak-to-Average Power Ratio，峰均功率比）**：OFDM 的時域波形是很多子載波相加，偶爾很多子載波同時同相，就會冒出一個比平均高很多的尖峰。

## 為什麼是問題
- 功率放大器要能「線性地」放大這些尖峰，否則會失真 → 必須用更線性、效率較差的放大器。
- DAC／ADC 需要更高的解析度。
- 對手機這類靠電池的裝置特別吃虧。

## 不能直接削掉嗎？
直接削峰（clipping）不是好解法：後面的濾波會把尖峰又帶回來，而且削峰本身會造成失真。

## 來源
S1
