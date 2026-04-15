import requests
import json
import time
from datetime import datetime

API_KEY = "your_api_key"
DEVICE_ID = "your_device_id"
TARGET_URL = f"https://cloud.zectrix.com/open/v1/devices/{DEVICE_ID}/display/structured-text"
INTERVAL = 600

DATA_SOURCES = [
    {
        "name": "weibo",
        "url": "http://newsnow.busiyi.world/api/s?id=weibo",
        "pageId": "2",
        "title": "微博热榜TOP10"
    },
    {
        "name": "toutiao",
        "url": "https://newsnow.busiyi.world/api/s?id=toutiao",
        "pageId": "4",
        "title": "今日头条热榜TOP10"
    },
    {
        "name": "cls",
        "url": "http://newsnow.busiyi.world/api/s?id=cls-telegraph",
        "pageId": "3",
        "title": "财联社实时榜TOP10"
    },
    {
        "name": "cankaoxiaoxi",
        "url": "https://newsnow.busiyi.world/api/s?id=cankaoxiaoxi",
        "pageId": "1",
        "title": "参考消息热榜TOP10",
        "max_length": 22
    }
]

def fetch_data(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None

def format_top10(data, source):
    title = source.get("title", "")
    max_length = source.get("max_length", 0)
    
    if isinstance(data, list):
        items = data
    elif "items" in data:
        items = data["items"]
    elif "data" in data:
        items = data["data"]
    else:
        return None
    
    if not items:
        return None
    
    top10 = items[:10]
    
    formatted_items = []
    for i, item in enumerate(top10, 1):
        if isinstance(item, dict):
            item_title = item.get("title", "").strip()
        else:
            item_title = str(item).strip()
        if item_title:
            if max_length > 0 and len(item_title) > max_length:
                item_title = item_title[:max_length-2] + "..."
            formatted_items.append(f"{i}.{item_title}")
    
    update_time = datetime.now().strftime("%Y/%m/%d %H:%M")
    body = f"{title}        更新时间：{update_time}\n" + "\n".join(formatted_items)
    
    return {
        "body": body,
        "pageId": ""
    }

def send_to_api(payload):
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    params = {
        "deviceId": DEVICE_ID
    }
    
    try:
        response = requests.post(TARGET_URL, params=params, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        print(f"推送成功: {response.status_code}")
        return True
    except Exception as e:
        print(f"推送失败: {e}")
        return False

def main():
    print(f"开始运行 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    for source in DATA_SOURCES:
        print(f"\n获取 {source['name']} 数据...")
        data = fetch_data(source["url"])
        if data:
            payload = format_top10(data, source)
            if payload:
                payload["pageId"] = source["pageId"]
                print(f"数据内容:\n{payload['body']}")
                send_to_api(payload)
            else:
                print(f"{source['name']} 数据格式错误")
        else:
            print(f"{source['name']} 获取数据失败")
    
    print(f"\n等待{INTERVAL}秒后再次执行...")
    time.sleep(INTERVAL)

if __name__ == "__main__":
    while True:
        main()