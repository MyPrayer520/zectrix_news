import os
import requests
import json
import time
from datetime import datetime

# ==========================================
# 核心参数：从 GitHub Actions 环境变量读取
# ==========================================
API_KEY = os.environ.get("API_KEY", "")
DEVICE_ID = os.environ.get("DEVICE_ID", "")
TARGET_URL = f"https://cloud.zectrix.com/open/v1/devices/{DEVICE_ID}/display/structured-text"

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
    
    # 注意：Actions 服务器默认是 UTC 时间，比北京时间慢 8 小时
    # 为了在屏幕上显示正确的北京时间，需要增加 8 小时的时差补偿
    from datetime import timedelta
    beijing_time = datetime.utcnow() + timedelta(hours=8)
    update_time = beijing_time.strftime("%Y/%m/%d %H:%M")
    
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
    beijing_time = datetime.utcnow() + timedelta(hours=8)
    print(f"开始运行 - {beijing_time.strftime('%Y-%m-%d %H:%M:%S')} (北京时间)")
    
    if not API_KEY or not DEVICE_ID:
        print("致命错误：API_KEY 或 DEVICE_ID 未找到，请检查 GitHub Secrets 配置！")
        return

    for source in DATA_SOURCES:
        print(f"\n获取 {source['name']} 数据...")
        data = fetch_data(source["url"])
        if data:
            payload = format_top10(data, source)
            if payload:
                payload["pageId"] = source["pageId"]
                print(f"准备推送数据内容:\n{payload['body']}")
                send_to_api(payload)
            else:
                print(f"{source['name']} 数据格式解析错误")
        else:
            print(f"{source['name']} 获取网络数据失败")

if __name__ == "__main__":
    from datetime import timedelta
    main()
