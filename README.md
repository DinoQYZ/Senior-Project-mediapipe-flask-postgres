# Senior-project
AI pose estimation using Mediapipe x Flask

## Step 1 資料庫設定

### method 1 自建資料庫
建立資料庫：
使用的是[postgresql](https://www.postgresql.org/)資料庫 <br>
程式碼內預設連線資料為

- host: 192.168.56.1
- dbname: dino
- user: dino
- password: dinopwd
- sslmode: disable

### method 2 Docker-compose
若已安裝過Docker可以直接docker compose up裡面有已經設定好的database <br>
![image](https://user-images.githubusercontent.com/104751397/210291331-335e4d3e-8593-4124-b93f-a8d00c4a05ad.png)
Windows 安裝 [Docker](https://learn.microsoft.com/zh-tw/virtualization/windowscontainers/manage-docker/configure-docker-daemon)

## Step 2 執行app.py
執行完後會出現ip位置
點擊或複製後從瀏覽器連線進入

![image](https://user-images.githubusercontent.com/104751397/208838629-6e34cb6a-ab09-4cf0-8276-0debd633d0e9.png)

## Step 3 操作

主要功能
- 開始健身
- 主頁
- 動作
- 使用教學(X)
- 使用者

### 主頁
![image](https://user-images.githubusercontent.com/104751397/208839093-b4317c63-de90-4edb-b3ad-63421cd7b92a.png)

### 動作選擇
- 手臂
![image](https://user-images.githubusercontent.com/104751397/208841052-b46356d7-039f-431c-bfe6-a572df539bc8.png)

- 胸部
![image](https://user-images.githubusercontent.com/104751397/208841266-3942295a-0ed5-47f2-8b32-08832bd0d3f4.png)

- 健身
![image](https://user-images.githubusercontent.com/104751397/208844575-89c3da37-57a7-4f61-b1ff-ed8dbe189a49.png)

### 使用者
- 登入
![image](https://user-images.githubusercontent.com/104751397/208841889-00ea9aa3-873e-40c7-a482-30a96c33670d.png)

- 註冊
![image](https://user-images.githubusercontent.com/104751397/208841788-45f705f3-f64d-4b7d-bcfd-f5d85fa97197.png)

- 使用者首頁
![image](https://user-images.githubusercontent.com/104751397/208843060-f2887c9e-6394-4e94-9b6f-4ae31d8ef913.png)

- 使用者紀錄 (可選擇時間區間)
![image](https://user-images.githubusercontent.com/104751397/208843409-e42b9d98-287c-4485-90de-5874c35321f1.png)

- 使用者目標 (可選擇時間區間)
![image](https://user-images.githubusercontent.com/104751397/208843507-8db6681c-2840-4de8-851d-90a55087a177.png)

- 編輯目標 (目前僅新增)
![image](https://user-images.githubusercontent.com/104751397/208843661-7d30e3bb-9e02-4339-9fb8-325560f345e7.png)

- 刪除帳號
![image](https://user-images.githubusercontent.com/104751397/208843717-d0683e1f-d99a-43fb-910e-3417339a1ac6.png)
