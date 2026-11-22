# 執行與檢查紀錄（由 run_pipeline.py 自動追加）

## 第 1 次執行　2026-11-22 15:23:09　— 第一版大綱（未修改）

### N3 Wiki lint：✅ PASS
```
  PASS  L1 front matter
  PASS  L2 連結
  PASS  L3 孤兒頁
  PASS  L4 來源 ID
  PASS  L5 prereq 圖
  PASS  L6 術語表
  PASS  L7 數字有來源
lint：通過
```
### N4 查詢 Wiki：✅ PASS
```
PASS  找到 11 個頁面，教學順序：multipath-isi → ofdm-basics → subcarrier-orthogonality → ifft-fft → cyclic-prefix → one-tap-equalization → pilots-channel-estimation → papr → cfo → ofdma → applications-history
```
### N6 檢查內容：❌ FAIL
```
  PASS  O1 每點有引用且頁面存在
  FAIL  O2 數字與 wiki 一致（1）
        - s10：「48」不在 ['wifi-80211a-example'] → 子載波 52 個（48 個資料 + 4 個導頻）
  PASS  O3 教學順序符合 prereq
  FAIL  O4 縮寫第一次出現有解釋（11）
        - s01：「OFDM」第一次出現沒有加（全名／中文）→ OFDM 是什麼？
        - s02：「IFFT」第一次出現沒有加（全名／中文）→ 實作：IFFT、循環前綴、一個除法的等化
        - s03：「ISI」第一次出現沒有加（全名／中文）→ 晚到的回音會疊到下一個符號上，叫做 ISI
        - s04：「QAM」第一次出現沒有加（全名／中文）→ 每一路放在一個子載波上，用 QAM 等方式調變
        - s06：「FFT」第一次出現沒有加（全名／中文）→ 接收端：去掉循環前綴 → FFT → 每個子載波各自處理
        - s07：「CP」第一次出現沒有加（全名／中文）→ CP 把符號尾端複製一段，貼在開頭
        - s11：「PAPR」第一次出現沒有加（全名／中文）→ 代價一：PAPR 太高
        - s12：「CFO」第一次出現沒有加（全名／中文）→ 兩端振盪器不可能完全同頻 → 一定有 CFO
        - s12：「ICI」第一次出現沒有加（全名／中文）→ 偏移後峰值對不準零點 → 產生 ICI
        - s13：「OFDMA」第一次出現沒有加（全名／中文）→ OFDMA：讓很多人同時用
        - s13：「LTE」第一次出現沒有加（全名／中文）→ LTE 的資源塊是 12 個子載波 × 14 個符號
  PASS  O5 份量適合一頁
  PASS  O6 學習目標都有涵蓋
check_outline：12 個問題
```
**→ 回到：N5 整理重點（改 outline.yaml）；若 wiki 缺資料則回 N2**

## 第 2 次執行　2026-11-22 15:23:26　— 修正 O2（刪除來源沒有的 48/4）與 O4（11 個縮寫補上中文）

### N3 Wiki lint：✅ PASS
```
  PASS  L1 front matter
  PASS  L2 連結
  PASS  L3 孤兒頁
  PASS  L4 來源 ID
  PASS  L5 prereq 圖
  PASS  L6 術語表
  PASS  L7 數字有來源
lint：通過
```
### N4 查詢 Wiki：✅ PASS
```
PASS  找到 11 個頁面，教學順序：multipath-isi → ofdm-basics → subcarrier-orthogonality → ifft-fft → cyclic-prefix → one-tap-equalization → pilots-channel-estimation → papr → cfo → ofdma → applications-history
```
### N6 檢查內容：✅ PASS
```
  PASS  O1 每點有引用且頁面存在
  PASS  O2 數字與 wiki 一致
  PASS  O3 教學順序符合 prereq
  PASS  O4 縮寫第一次出現有解釋
  PASS  O5 份量適合一頁
  PASS  O6 學習目標都有涵蓋
check_outline：通過
```
### N7 產生簡報：✅ PASS
```
  PASS  產生 docs/slides.html：18 頁，數學式 5 個
  PASS  產生 docs/wiki/（28 頁）與 docs/index.html
```
### N8 檢查成品：❌ FAIL
```
  PASS  P1 頁數正確
  FAIL  P2 每頁內容不超出畫面（4）
        - s18：內容高度 723px > 可用 501px
        - s18：div「S1　Orthogonal frequency-」超出 205px
        - s18：ul「S1　Orthogonal frequency-」超出 149px
        - s18：li「S5　5G NR（Wikipedia）
http」超出 48px
  PASS  P3 數學式正常顯示
  PASS  P4 wiki 連結有效
  PASS  P5 沒有 JavaScript 錯誤
check_slides：4 個問題（截圖在 runs/screens/）
```
**→ 回到：N7 產生簡報（版面）或 N5（內容太多）**

### N8 補充：截圖人工（LLM 看圖）檢查 — 第 2 次執行的 18 張截圖
自動檢查只抓得到「超出畫面」，以下是看截圖才發現的問題：
- s01 標題在「是什｜麼？」中間斷行 → 縮小標題字級
- s01 右下角換頁按鈕蓋住頁碼「1 / 18」→ 頁尾右側留空間
- s03 圖中「直射（先到）」文字壓在直射線上 → 移到線的下方
- s07 圖中虛線（FFT 視窗起點）穿過說明文字 → 重新排位置
- s11 圖中「峰值」標籤壓在峰值圓圈上、「平均功率」壓在波形上 → 標籤移開
- s18 參考資料太長（自動檢查已抓到）→ 改成兩欄、縮小字級
**→ 回到：N7 產生簡報（版面），內容不用改**

## 第 3 次執行　2026-11-22 15:24:11　— 依截圖檢查修正版面（N7）

### N3 Wiki lint：✅ PASS
```
  PASS  L1 front matter
  PASS  L2 連結
  PASS  L3 孤兒頁
  PASS  L4 來源 ID
  PASS  L5 prereq 圖
  PASS  L6 術語表
  PASS  L7 數字有來源
lint：通過
```
### N4 查詢 Wiki：✅ PASS
```
PASS  找到 11 個頁面，教學順序：multipath-isi → ofdm-basics → subcarrier-orthogonality → ifft-fft → cyclic-prefix → one-tap-equalization → pilots-channel-estimation → papr → cfo → ofdma → applications-history
```
### N6 檢查內容：✅ PASS
```
  PASS  O1 每點有引用且頁面存在
  PASS  O2 數字與 wiki 一致
  PASS  O3 教學順序符合 prereq
  PASS  O4 縮寫第一次出現有解釋
  PASS  O5 份量適合一頁
  PASS  O6 學習目標都有涵蓋
check_outline：通過
```
### N7 產生簡報：✅ PASS
```
  PASS  產生 docs/slides.html：18 頁，數學式 5 個
  PASS  產生 docs/wiki/（28 頁）與 docs/index.html
```
### N8 檢查成品：❌ FAIL
```
  PASS  P1 頁數正確
  FAIL  P2 每頁內容不超出畫面（4）
        - s18：內容高度 602px > 可用 501px
        - s18：div「S1　Orthogonal frequency-」超出 84px
        - s18：ul「S1　Orthogonal frequency-」超出 28px
        - s18：li「S5　5G NR（Wikipedia）
http」超出 8px
  PASS  P3 數學式正常顯示
  PASS  P4 wiki 連結有效
  PASS  P5 沒有 JavaScript 錯誤
check_slides：4 個問題（截圖在 runs/screens/）
```
**→ 回到：N7 產生簡報（版面）或 N5（內容太多）**

## 第 4 次執行　2026-11-22 15:24:23　— 縮短參考資料頁（N7）

### N3 Wiki lint：✅ PASS
```
  PASS  L1 front matter
  PASS  L2 連結
  PASS  L3 孤兒頁
  PASS  L4 來源 ID
  PASS  L5 prereq 圖
  PASS  L6 術語表
  PASS  L7 數字有來源
lint：通過
```
### N4 查詢 Wiki：✅ PASS
```
PASS  找到 11 個頁面，教學順序：multipath-isi → ofdm-basics → subcarrier-orthogonality → ifft-fft → cyclic-prefix → one-tap-equalization → pilots-channel-estimation → papr → cfo → ofdma → applications-history
```
### N6 檢查內容：✅ PASS
```
  PASS  O1 每點有引用且頁面存在
  PASS  O2 數字與 wiki 一致
  PASS  O3 教學順序符合 prereq
  PASS  O4 縮寫第一次出現有解釋
  PASS  O5 份量適合一頁
  PASS  O6 學習目標都有涵蓋
check_outline：通過
```
### N7 產生簡報：✅ PASS
```
  PASS  產生 docs/slides.html：18 頁，數學式 5 個
  PASS  產生 docs/wiki/（28 頁）與 docs/index.html
```
### N8 檢查成品：✅ PASS
```
  PASS  P1 頁數正確
  PASS  P2 每頁內容不超出畫面
  PASS  P3 數學式正常顯示
  PASS  P4 wiki 連結有效
  PASS  P5 沒有 JavaScript 錯誤
check_slides：通過（截圖在 runs/screens/）
```
**全部節點通過，已輸出 docs/slides.html 與 docs/wiki/。**

## 第 5 次執行　2026-11-22 15:24:48　— 最終確認（wiki log 補上 query 紀錄後重跑）

### N3 Wiki lint：✅ PASS
```
  PASS  L1 front matter
  PASS  L2 連結
  PASS  L3 孤兒頁
  PASS  L4 來源 ID
  PASS  L5 prereq 圖
  PASS  L6 術語表
  PASS  L7 數字有來源
lint：通過
```
### N4 查詢 Wiki：✅ PASS
```
PASS  找到 11 個頁面，教學順序：multipath-isi → ofdm-basics → subcarrier-orthogonality → ifft-fft → cyclic-prefix → one-tap-equalization → pilots-channel-estimation → papr → cfo → ofdma → applications-history
```
### N6 檢查內容：✅ PASS
```
  PASS  O1 每點有引用且頁面存在
  PASS  O2 數字與 wiki 一致
  PASS  O3 教學順序符合 prereq
  PASS  O4 縮寫第一次出現有解釋
  PASS  O5 份量適合一頁
  PASS  O6 學習目標都有涵蓋
check_outline：通過
```
### N7 產生簡報：✅ PASS
```
  PASS  產生 docs/slides.html：18 頁，數學式 5 個
  PASS  產生 docs/wiki/（28 頁）與 docs/index.html
```
### N8 檢查成品：✅ PASS
```
  PASS  P1 頁數正確
  PASS  P2 每頁內容不超出畫面
  PASS  P3 數學式正常顯示
  PASS  P4 wiki 連結有效
  PASS  P5 沒有 JavaScript 錯誤
check_slides：通過（截圖在 runs/screens/）
```
**全部節點通過，已輸出 docs/slides.html 與 docs/wiki/。**

## 第 6 次執行　2026-11-22 15:25:15　— workflow 第 2 版：查詢步驟加入「必看 ①②」後重跑

### N3 Wiki lint：✅ PASS
```
  PASS  L1 front matter
  PASS  L2 連結
  PASS  L3 孤兒頁
  PASS  L4 來源 ID
  PASS  L5 prereq 圖
  PASS  L6 術語表
  PASS  L7 數字有來源
lint：通過
```
### N4 查詢 Wiki：✅ PASS
```
PASS  找到 11 個頁面，教學順序：multipath-isi → ofdm-basics → subcarrier-orthogonality → ifft-fft → cyclic-prefix → one-tap-equalization → pilots-channel-estimation → papr → cfo → ofdma → applications-history
```
### N6 檢查內容：✅ PASS
```
  PASS  O1 每點有引用且頁面存在
  PASS  O2 數字與 wiki 一致
  PASS  O3 教學順序符合 prereq
  PASS  O4 縮寫第一次出現有解釋
  PASS  O5 份量適合一頁
  PASS  O6 學習目標都有涵蓋
check_outline：通過
```
### N7 產生簡報：✅ PASS
```
  PASS  產生 docs/slides.html：18 頁，數學式 5 個
  PASS  產生 docs/wiki/（28 頁）與 docs/index.html
```
### N8 檢查成品：✅ PASS
```
  PASS  P1 頁數正確
  PASS  P2 每頁內容不超出畫面
  PASS  P3 數學式正常顯示
  PASS  P4 wiki 連結有效
  PASS  P5 沒有 JavaScript 錯誤
check_slides：通過（截圖在 runs/screens/）
```
**全部節點通過，已輸出 docs/slides.html 與 docs/wiki/。**
