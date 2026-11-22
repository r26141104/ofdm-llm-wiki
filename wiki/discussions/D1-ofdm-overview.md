---
title: 討論 D1：Ingest S1（OFDM 總覽）之前
type: discussion
---

**來源**：[[S1-wikipedia-ofdm]]　**當時 wiki 狀態**：空的，這是第一篇。

## 這篇最重要的點
1. OFDM 的核心想法：把一條快的資料流拆成很多條慢的，放在彼此正交、頻譜重疊的子載波上。
2. 正交的條件是 Δf = 1/T_U，所以不需要保護頻帶。
3. 符號變長 + 保護區間（循環前綴）→ 多路徑造成的 ISI 被擋掉。
4. 實作靠 IFFT/FFT；接收端每個子載波一個乘法就能等化。
5. 代價：PAPR 高、怕頻率偏移、CP 浪費時間。

## 疑點
- 頁面談 802.11a 有 52 個子載波，但沒說資料／導頻各幾個；常見說法是 48 + 4，但**這篇來源沒有**，先不寫進 wiki。
- 「Peled & Ruiz 1980 提出循環前綴」是我原本的印象，S1 沒有提到，不寫。

## 決定（要生成哪些頁）
- 新增概念頁：`ofdm-basics`、`multipath-isi`、`subcarrier-orthogonality`、`ifft-fft`、`cyclic-prefix`、`one-tap-equalization`、`pilots-channel-estimation`、`papr`、`applications-history`、`wifi-80211a-example`。
- CFO 只在 S1 提一句，等 S3 進來再開 `cfo` 頁。
- 超出入門範圍、先不寫：COFDM 編碼細節、SFN 單頻網、DVB-T 的計算時間預算。
- 802.11a 的 CP 開銷可以自己算：0.8 /(3.2 + 0.8) = 20%，標為（推導）。
