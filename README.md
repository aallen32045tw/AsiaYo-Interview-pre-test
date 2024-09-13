#AsiaYo - Jr Backend Engineer - 何艾倫

##資料庫測驗

###題目一
請寫出一條查詢語句 (SQL)，列出在 2023 年 5 月下訂的訂單，使用台幣付款且5月總金額最多的前 10 筆的旅宿 ID (bnb_id), 旅宿名稱 (bnb_name), 5 月總金額 (may_amount)

```sql
SELECT o.bnb_id, b.name AS bnb_name, SUM(o.amouont) AS may_amount
FROM orders o
JOIN bnbs b ON o.bnb_id = b.id
WHERE 
    o.currency = 'TWD'
    AND o.created_at >= '2023-05-01' 
    AND o.created_at < '2023-06-01'
GROUP BY o.bnb_id, b.name
ORDER BY may_amount DESC
LIMIT 10;
```

###題目二
在題目一的執行下，我們發現 SQL 執行速度很慢，您會怎麼去優化？請闡述您怎麼判斷與優化的方式
1.  查詢重寫：
    * 可以執行 EXPLAIN 來分析 SQL，這樣可以查看是否存在進行全表掃描的情況。
    * 使用子查詢或 CTE 簡化查詢並提高可讀性和性能。
2.  考慮分區：
    * 如果 orders 表非常大，可以考慮按月份或年份進行分區。
    * 分區後，查詢只需要掃描相關的分區，而不是整個表，這可以提高查詢速度。
3.  索引優化：
    * 為 orders 表的 bnb_id, currency, 和 created_at 列創建複合索引。
---
##API實作測驗

###SOLID
1.  單一職責原則 (SRP)：
    * `OrderController` 專注於處理 HTTP 請求和回應，不涉及業務邏輯。
    * `OrderService` 負責處理訂單的業務邏輯。
    * `OrderTransformer` 專門負責數據的轉換和驗證。
    * 各種驗證策略（如 `NameValidationStrategy`, `PriceValidationStrategy`, `CurrencyValidationStrategy`）各自負責特定字段的驗證邏輯。
2.  開放封閉原則 (OCP)：
    * `OrderTransformer` 使用策略模式實現驗證邏輯，允許添加新的驗證規則而無需修改現有代碼。
    * 新的驗證策略可以通過實現 `ValidationStrategy` 接口來輕鬆添加，不需要修改 `OrderTransformer` 的核心邏輯。
3.  里氏替換原則 (LSP)：
    * 所有的驗證策略類都實現了 `ValidationStrategy` 接口，確保它們可以互相替換而不影響程序的正確性。
4.  介面隔離原則 (ISP)：
    * `ValidationStrategy` 接口只定義了一個 `validate` 方法，保持了接口的簡潔性。
    * `OrderServiceInterface` 只定義了必要的方法，避免了冗余的接口設計。
5.  依賴反向原則 (DIP):
    * `OrderController` 依賴於 `OrderServiceInterface` 而不是具體的 `OrderService` 實現，允許輕鬆替換或模擬服務實現。
    
###設計模式
1. 策略模式 (Strategy Pattern)：
   * 在 `OrderTransformer` 中，不同的驗證邏輯（如名稱、價格、貨幣檢查）被實現為獨立的策略類。
   * 這些策略類都實現了 `ValidationStrategy` 接口，可以根據需要靈活替換或擴展。
   * `OrderTransformer` 使用一個策略字典來存儲和使用這些驗證策略，使得添加新的驗證邏輯變得簡單。

2. 依賴注入 (Dependency Injection)：
   * `OrderController` 通過構造函數接收 `OrderServiceInterface` 的實例，實現了依賴注入。
   * 這種設計提高了代碼的可測試性，允許輕鬆替換不同的 `OrderService` 實現或進行單元測試。