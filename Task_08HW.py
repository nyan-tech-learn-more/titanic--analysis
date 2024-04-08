import sqlite3
import datetime
import requests
import json

#計算的「各地區的藥局數量」存入資料庫的 `pharmacies` 表格，欄位包含「地區」、「數量」、「新增時間」
conn = sqlite3.connect('example.db')  
#這行創建了一個 SQLite 資料庫連接物件 (conn)，並連接到名為 example.db 的 SQLite 資料庫。
#如果 example.db 不存在，則會在同一個目錄下創建一個新的資料庫。
c = conn.cursor()  
#創建了一個 cursor 物件 c，它可以用來執行 SQL 查詢和操作資料庫。conn.cursor() 是一個方法
#，用於建立一個 cursor 物件，這個 cursor 物件可以用來執行 SQL 查詢並處理查詢結果。

# 新增pharmacies表格且清空資料表
c.execute('''CREATE TABLE IF NOT EXISTS pharmacies
             (city text, counts text, createdAt datetime)''')
c.execute('''DELETE FROM pharmacies''')
conn.commit()

# 新增資料

# 利用 requests 對 API 來源發送一個請求
url = 'https://raw.githubusercontent.com/kiang/pharmacies/master/json/points.json'
response = requests.get(url)

# 將請求回應的內容存成一個字串格式
dic = response.text


# 將長得像 json 格式的字串解析成字典或列表
#python json字串轉成python物件需要使用json模塊的loads()
data = json.loads(dic)
#print(data)

#3.計算各地區的藥局數量-------------------------
med_count = {} #建立一個空字典med_count
print(med_count) #印出空字典

# 填入欄位名稱
for dic in data['features']:# 從 data['features'] 取出一個 dic 資料
    conunty = dic['properties']['county'] #取出字典的properties的county欄位
#    print(conunty)
    if conunty not in med_count: #如果county不在med_count中
         med_count[conunty] = 0 #則將county加入med_count,設為0,ex:med_count = {"台北市": 0, "新北市": 1}
         #dictionary[key] = value
    else:
        med_count[conunty] += 1 #如果county在med_count中，則med_count[county] + 1
print
(med_count)

#-------------------新增到資料庫內
for city, counts in med_count.items(): 
  #Your Code # item()把將每一筆Med_count資料的Key, value分別取出來新增到資料庫
  t = datetime.datetime.now()
  print(f"INSERT INTO stocks VALUES ('{city}', {counts}, '{t}')")
  c.execute(f"INSERT INTO pharmacies VALUES ('{city}', {counts}, '{t}')")
  conn.commit()

# 查詢資料
c.execute("SELECT * FROM pharmacies")
print(c.fetchall())

conn.commit()
conn.close()
