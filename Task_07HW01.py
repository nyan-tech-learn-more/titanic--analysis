# 資料中提供詳細的全台藥局資訊，包含藥局名稱、地址、電話、營業時間等相關基本訊息，
# 以及各藥局的note與成人和孩童的口罩數量，還有藥局所在的經緯度資訊。
# 延伸應用：藥局口罩庫存查詢、補充庫存提醒、庫存地圖視覺化、預測口罩需求、預約系統


import requests
from requests import get
import json

# json.dumps()
# 將python物件轉成json字串，返回type為str
# 從python物件轉換為json字串

# json.loads()
# 將json字串，返回python物件，返回type為dict
# 從json字串轉換為python物件



# 利用 requests 對 API 來源發送一個請求
url = 'https://raw.githubusercontent.com/kiang/pharmacies/master/json/points.json'
response = requests.get(url)

# 將請求回應的內容存成一個字串格式
dic = response.text


# 將長得像 json 格式的字串解析成字典或列表
#python json字串轉成python物件需要使用json模塊的loads()
data = json.loads(dic)   
print(data)


med_count = {} #建立一個空字典med_count
print(med_count) #印出空字典

# 填入欄位名稱
for dic in data['features']:# 從 data['features'] 取出一個 dic 資料  
    conunty = dic['properties']['county'] #取出字典的properties與county欄位  
#    print(conunty)
    if conunty not in med_count: #如果county不在med_count中
         med_count[conunty] = 0 #則將county加入med_count,設為0
    else:
        med_count[conunty] += 1 #如果county在med_count中，則med_count[county] + 1 
print(med_count)

# {'臺北市': 338, '': 48, '高雄市': 421, '臺中市': 419, '臺南市': 270, '基隆市': 56, '新竹市': 38, '嘉義市': 66, '新北市': 500, '桃園市': 263, '新竹縣': 45, '宜蘭縣': 75, '苗栗縣': 55, '彰化縣': 178, '南投縣': 66, '雲林縣': 128, '嘉義縣': 83, '屏東縣': 139, '澎湖縣': 10, '花蓮縣': 45, '臺東縣': 22, '金門縣': 5, '連江縣': 0}


#---4. 接下來請你計算出每個地區的成人剩餘口罩數量，並且將結果從大到小排列，完成後 Commit 第三個版本：
mask_count = {}

# 填入欄位名稱
for d in data['features']:
    conunty = d['properties']['county'] #取出字典的properties與county欄位  
    adult_mask_count = d['properties']['mask_adult'] #取出字典的properties與mask_adult（成人口罩) 欄位
  
#d['properties']['country'] 是一層一層找的，先找 properties 再找 properties 底下的 country；跟 properties 同階層的 key 也叫 country 不會怎樣
  
    if conunty not in mask_count: #如果county不在mask_count中
      mask_count[conunty] = adult_mask_count #則將county加入mask_count,設為adult_mask_count, 不會變了
    else:
      mask_count[conunty] += adult_mask_count #如果county在mask_count中，則mask_count[county] + adult_mask_count,持續累加總數

# 將結果從大到小排列
med_count = dict(sorted(mask_count.items(), key=lambda item: item[1]))

print(mask_count)
# {'台北市': 12345, '新北市': 45678 ...}
