---
title: 討論 D2：Ingest S2（循環前綴）之前
type: discussion
---

**來源**：[[S2-wikipedia-cyclic-prefix]]　**相關現有頁**：[[cyclic-prefix]]、[[one-tap-equalization]]、[[multipath-isi]]

## 這篇最重要的點
1. CP 長度至少要等於通道長度（S1 說的是「延遲擴散比保護區間短」，兩者講同一件事）。
2. **為什麼**一個乘法就能等化：CP 把線性卷積變成循環卷積，DFT 之後變成逐點相乘。S1 只說「可以」，S2 說了「為什麼」。
3. 接收端會把 CP 丟掉。

## 跟現有頁的關係
- `cyclic-prefix` 頁目前只有「是什麼」，要補「為什麼有效」與「長度條件」。
- `one-tap-equalization` 要加上 $Y_k = H_k X_k + W_k$ 的式子，並連回 `cyclic-prefix`。
- 沒有衝突。

## 決定
- 更新 `cyclic-prefix`、`one-tap-equalization`。
- 不新增頁。卷積定理的完整證明超出入門範圍，只寫結論與直覺。
