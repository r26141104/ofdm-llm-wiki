---
id: S6
title: What Is OFDM?（MathWorks Discovery）
url: https://www.mathworks.com/discovery/ofdm.html
accessed: 2026-11-22
license: 版權屬 MathWorks；此處僅保留自己的重點筆記
---

# S6 擷取重點（以自己的話整理）

## 定義
- OFDM 是多載波調變：把資料放到許多彼此正交的窄頻子載波上傳送。
- 建立在 QAM 等單載波調變之上，資料率相近，但更能對抗頻率選擇性衰落。

## 運作流程
- 資料先編碼，通常對應成 QAM 符號。
- 把符號放到等間距的頻率格上，用 IFFT 轉成時域中互相重疊的正弦波。
- IFFT 的 N 個輸出樣本組成一個 OFDM 符號。
- 每個符號加上循環前綴；只要 CP 不短於通道脈衝響應，線性卷積就像循環卷積，接收端每個子載波用一個複數乘法就能處理。
- 用已知的導頻符號做通道估計與等化。

## 優點
- 能處理寬頻通道中的頻率選擇性衰落與多路徑。
- 每個子載波可以獨立做通道估計與等化。
- 容易在多個資料流之間分享資源。
- 每個子載波看到的是平坦衰落，只需一個等化器係數，因此很適合 MIMO 與 Massive MIMO。

## 應用
- Wi-Fi、LTE、5G。LTE/5G 把多個 OFDM 符號組成 slot 或 subframe。
- LTE 的資源塊（resource block）是 12 個子載波 × 14 個符號（一個 subframe）。

## 工具
- MATLAB 的 Communications、WLAN、LTE、5G Toolbox 可做 OFDM 波形的鏈路層模擬。
