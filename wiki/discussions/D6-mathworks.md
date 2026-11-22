---
title: 討論 D6：Ingest S6（MathWorks：What Is OFDM?）之前
type: discussion
---

**來源**：[[S6-mathworks-ofdm]]　**相關現有頁**：幾乎全部的基礎頁

## 這篇最重要的點
1. 跟 S1 大致重疊，但**用工程流程**講：編碼 → QAM → IFFT → 加 CP → 通道 → 等化。很適合做簡報的方塊圖。
2. 第二個獨立來源確認「CP ≥ 通道脈衝響應 → 一個複數乘法等化」。
3. 新資訊：每個子載波是平坦衰落 → 很適合 MIMO；LTE 資源塊 = 12 子載波 × 14 符號。

## 跟現有頁的關係
- `ifft-fft`、`one-tap-equalization`、`pilots-channel-estimation` 各加上 S6 作為第二個來源（交叉驗證）。
- `ofdma` 可補一句 LTE 資源塊的大小。
- 沒有衝突。

## 決定
- 不新增概念頁，只更新上述頁面的 sources 與內容。
- MATLAB 工具清單不寫進概念頁，只留在來源摘要頁。
