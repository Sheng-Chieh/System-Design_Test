# Web Test

## 專案簡介
本專案是一個基於 Django (版本 6.0.2) 建立的 Web 測試應用程式。

## 系統環境與依賴
- **程式語言**: Python 3.x
- **網頁框架**: Django 6.0.2
- **資料庫系統**: MySQL

## 主要功能
- **使用者登入 (`/login/`)**: 提供左右分欄設計的登入介面，後端透過 Raw SQL 查詢與資料庫進行帳號及密碼的比對驗證。
- **狀態管理**: 登入成功後，系統會將使用者帳號寫入 Cookie 中 (有效期限設定為 1 小時)，藉此維持使用者的登入狀態。
- **歡迎頁面 (`/function1/`)**: 登入成功後會跳轉至此頁面，顯示當前時間與歡迎訊息；若未登入則會自動將使用者導向登入頁面。

## 資料庫設定
在執行此專案前，請確認本機 MySQL 環境已啟動，專案預設的資料庫連線設定如下：
- **Host**: localhost
- **Port**: 3306
- **Username**: root
- **Password**: 0000
- **Database Name**: `dbms_project`

### 資料表建置
需要在 MySQL 中建立對應的資料庫與資料表，請在 MySQL 終端機執行以下 SQL 語法：

```sql
-- 1. 建立資料庫
CREATE DATABASE dbms_project;
USE dbms_project;

-- 2. 建立使用者資料表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

-- 3. 新增一筆測試帳號供登入使用
INSERT INTO users (username, password) VALUES ('testuser', 'testpass');
