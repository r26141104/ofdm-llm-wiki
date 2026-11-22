---
title: 一階等化（One-tap Equalization）
type: concept
sources: [S1, S2, S6]
prereq: [cyclic-prefix]
terms: [等化, one-tap]
---

## 一句話
有了 CP，多路徑通道在頻域變成「每個子載波各自乘上一個複數」，所以接收端每個子載波**只要除以那個複數**就能還原。

## 式子
第 $k$ 個子載波：

$$Y_k = H_k X_k + W_k$$

- $X_k$：傳出去的符號　$H_k$：通道在這個子載波上的複數增益　$W_k$：雜訊
- 等化：$\hat{X}_k = Y_k / H_k$

## 為什麼叫 one-tap
每個子載波只需要**一個**係數（一個 tap）。相比之下，單載波系統在時域等化常常需要很長的濾波器。

## 前提
- [[cyclic-prefix]] 長度 ≥ 通道長度。
- 通道在一個符號時間內變化不大。
- 要知道 $H_k$ → 見 [[pilots-channel-estimation]]。

## 額外好處
每個子載波看到的是平坦衰落，只需一個係數，所以很容易和 MIMO 結合。

## 來源
S1、S2、S6
