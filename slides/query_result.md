# 查詢結果：OFDM 是什麼？

- 對象：大學部、沒有修過通訊系統的同學（知道正弦波與「頻率」是什麼即可）
- 學習目標 10 項；依 prereq 圖補上的前置／延伸頁：ifft-fft

## 建議教學順序（拓撲排序）

### 1. 多路徑與符號間干擾（Multipath & ISI）  `[[multipath-isi]]`
- 前置：無　來源：S1, S2
- 重點：
  - 像在山谷裡講話：你講得越快，上一個字的回音越容易蓋到下一個字。
  - 回音拖多長叫做**延遲擴散**（delay spread）。符號越短（傳得越快），延遲擴散相對越長，ISI 越嚴重。
  - 把一條快速資料流拆成很多條慢速資料流 → 每個符號變長，延遲擴散相對變得很短。見 [[ofdm-basics]]。
  - 在符號之間加保護區間（實際放的是 [[cyclic-prefix]]）。只要延遲擴散比保護區間短，就不會有 ISI。
  - 例子：1 ms 的符號配 1/8 的保護區間 = 125 µs，可以容忍約 37.5 km 的路徑差。

### 2. OFDM 基本概念  `[[ofdm-basics]]`
- 前置：multipath-isi　來源：S1, S6
- 重點：
  - 每個子載波各自用一般的調變方式，例如 **QAM（Quadrature Amplitude Modulation，正交振幅調變）** 或 PSK。
  - 在同樣頻寬下，總資料率和單載波差不多，但每個子載波的符號變長，對 [[multipath-isi]] 強很多。
  - 它是 FDM 的一種，但子載波的頻譜**彼此重疊**——能重疊而不互相干擾，靠的是 [[subcarrier-orthogonality]]。
  - 每個窄子載波內，通道衰落近似平坦，所以等化很簡單（見 [[one-tap-equalization]]）。

### 3. 子載波正交性  `[[subcarrier-orthogonality]]`
- 前置：ofdm-basics　來源：S1, S6
- 重點：
  $$\Delta f = \frac{1}{T_U}$$
  - 在長度 $T_U$ 的時間裡，每個子載波都剛好跑整數圈。兩個不同子載波相乘再積分，正負剛好抵消 → 正交。
  - 頻域上看，每個子載波是一個 sinc 形狀；某個子載波的峰值，正好落在其他所有子載波的零點上。
  - 不需要傳統 FDM 的保護頻帶，也不需要每個子通道各自的濾波器 → 頻譜利用率高。
  - N 個子載波的總頻寬約為 $B \approx N\,\Delta f$。

### 4. 用 IFFT／FFT 實作 OFDM  `[[ifft-fft]]`
- 前置：subcarrier-orthogonality　來源：S1, S6
- 重點：
  1. 位元 → 分成平行串流 → 各自對應成 QAM／PSK 符號 $X_k$。
  2. 把 $X_k$ 放到等間距的頻率格上，做 N 點 IFFT → N 個時域樣本 = 一個 OFDM 符號。
  3. 加上 [[cyclic-prefix]] → DAC → 升頻送出。
  1. 降頻 → ADC → 丟掉 CP。
  2. N 點 FFT → 得到每個子載波上的 $Y_k$。
  3. 每個子載波各自等化與判斷（見 [[one-tap-equalization]]）→ 還原位元。

### 5. 循環前綴（Cyclic Prefix, CP）  `[[cyclic-prefix]]`
- 前置：multipath-isi, ifft-fft　來源：S1, S2, S5, S6
- 重點：
  1. **擋住 ISI**：前一個符號的回音只會落在 CP 裡，而 CP 會被丟掉。見 [[multipath-isi]]。
  2. **讓等化變成一個乘法**：因為 CP 是符號自己的尾巴，通道的線性卷積在 CP 之後看起來就像**循環卷積**；而循環卷積做 DFT 之後會變成**逐點相乘**。見 [[one-tap-equalization]]。

### 6. 一階等化（One-tap Equalization）  `[[one-tap-equalization]]`
- 前置：cyclic-prefix　來源：S1, S2, S6
- 重點：
  $$Y_k = H_k X_k + W_k$$
  - $X_k$：傳出去的符號　$H_k$：通道在這個子載波上的複數增益　$W_k$：雜訊
  - 等化：$\hat{X}_k = Y_k / H_k$
  - [[cyclic-prefix]] 長度 ≥ 通道長度。
  - 通道在一個符號時間內變化不大。
  - 要知道 $H_k$ → 見 [[pilots-channel-estimation]]。

### 7. 導頻與通道估計  `[[pilots-channel-estimation]]`
- 前置：one-tap-equalization　來源：S1, S3, S6
- 重點：
  - 在導頻子載波上：$\hat{H}_k = Y_k / X_k$（$X_k$ 已知）。
  - 其他子載波的 $H_k$ 用鄰近導頻的估計值內插。
  - 估出來的 $\hat{H}_k$ 交給 [[one-tap-equalization]] 使用。
  - 追蹤殘餘的頻率偏移（見 [[cfo]]）。
  - 追蹤取樣時脈偏移（SCO）：SCO 造成的相位旋轉與子載波索引成正比，所以能和 CFO 分開。

### 8. 峰均功率比（PAPR）  `[[papr]]`
- 前置：ifft-fft　來源：S1
- 重點：
  - 功率放大器要能「線性地」放大這些尖峰，否則會失真 → 必須用更線性、效率較差的放大器。
  - DAC／ADC 需要更高的解析度。
  - 對手機這類靠電池的裝置特別吃虧。

### 9. 載波頻率偏移（CFO）  `[[cfo]]`
- 前置：subcarrier-orthogonality　來源：S1, S3
- 重點：
  - 兩個振盪器不可能完全一樣快——即使完全不動也會有 CFO。
  - 移動造成的都卜勒效應也會產生 CFO（通常比振盪器誤差小）。
  - IEEE 802.11 允許每個振盪器 ±20 ppm → 收發兩端合起來最壞 ±40 ppm。
  - 在 5.2 GHz：約 ±208 kHz。
  - 和 802.11a 的子載波間距 312.5 kHz 相比：208 / 312.5 ≈ 0.67 個間距（推導）。
  - 子載波平移後，峰值不再對準其他子載波的零點 → 正交性被破壞 → **ICI（Inter-Carrier Interference，子載波間干擾）**。
  - 正規化 CFO $\varepsilon$ = 頻率偏移 ÷ 子載波間距，拆成**整數部分**（子載波索引整個平移）與**小數部分**（振幅衰減、相位旋轉、ICI）。
  - 補償後剩下的殘餘 CFO 要很小：64QAM 約 0.01，QPSK 約 0.03。

### 10. OFDMA（多使用者 OFDM）  `[[ofdma]]`
- 前置：ofdm-basics　來源：S4, S6
- 重點：
  - OFDM：一個時間點，全部子載波都給同一個使用者。
  - OFDMA：資源是一張「時間 × 頻率」的格子，每個使用者分到其中幾格。
  - 例：LTE 的資源塊是 12 個子載波 × 14 個符號。
  - 很多低速使用者可以同時傳，延遲較短、較穩定。
  - 依各使用者的通道狀況分配子載波，能避開衰落。
  - 分到的子載波數不同，就能提供不同的服務品質。
  - 對頻率偏移與相位雜訊更敏感（見 [[cfo]]）。
  - 分配與通道回報比較複雜。

### 11. OFDM 的歷史與應用  `[[applications-history]]`
- 前置：ofdm-basics　來源：S1, S4, S5, S6
- 重點：
  - **1966**：Robert W. Chang（Bell Labs）提出 OFDM 概念並取得專利。
  - **1971**：Weinstein 與 Ebert 提出用 DFT 實作，並加入保護區間（見 [[ifft-fft]]）。
  - **1997**：DVB-T 數位電視標準化。
  - **1999**：IEEE 802.11a（Wi-Fi）標準化（見 [[wifi-80211a-example]]）。
  - **2005–2007**：LTE 下行採用 OFDMA（見 [[ofdma]]）。
  - **5G NR**：上下行都以 OFDM 為基礎，並使用可調整的子載波間距（見 [[nr-numerology]]）。
  - **Wi-Fi**：IEEE 802.11a/g/n/ac/ax（ax = Wi-Fi 6，加入 OFDMA）
  - **行動通訊**：**LTE**（4G）、5G NR

## 寫大綱前必看 ①：縮寫第一次出現要這樣寫

| 縮寫 | 第一次出現時寫成 |
|---|---|
| ISI | ISI（符號間干擾） |
| OFDM | OFDM（正交分頻多工） |
| QAM | QAM（正交振幅調變） |
| IFFT | IFFT（反快速傅立葉轉換） |
| FFT | FFT（快速傅立葉轉換） |
| CP | CP（循環前綴） |
| PAPR | PAPR（峰均功率比） |
| CFO | CFO（載波頻率偏移） |
| ICI | ICI（子載波間干擾） |
| OFDMA | OFDMA（正交分頻多重存取） |
| NR | NR（5G 的空中介面） |
| LTE | LTE（4G 行動通訊標準） |

⚠ 以下縮寫名字互相包含，但要**各自**在第一次出現時解釋：IFFT 和 FFT、OFDMA 和 OFDM

## 寫大綱前必看 ②：來源沒有、不要寫的內容

- S1-wikipedia-ofdm：802.11a 的 52 個子載波沒有拆分資料／導頻數量，wiki 不寫 48/4。
- S2-wikipedia-cyclic-prefix：頁面沒有給具體數字；公式在擷取時沒有正確顯示，所以 wiki 只寫結論。
- S5-wikipedia-5g-nr：960 kHz 的 slot 長度原文寫 0.01565 ms，判斷為誤植，wiki 以 0.015625 ms（推導）記錄。