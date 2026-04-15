# 每日热点推送

自动获取微博、今日头条、财联社热榜并推送到设备显示。

## 功能

- 微博热榜 TOP10（pageId: 1）
- 今日头条热榜 TOP10（pageId: 2）
- 财联社实时榜 TOP10（pageId: 3）
- 每条数据显示更新时间
- 每 10 分钟自动刷新

## 配置

在 `zectrix_hot.py` 中修改以下配置：

```python
API_KEY = "your_api_key"
DEVICE_ID = "your_device_id"
TARGET_URL = "your_target_url"
```

## 运行

### Windows

```bash
py zectrix_hot.py
```

### Linux

```bash
chmod +x start.sh stop.sh restart.sh

./start.sh     # 启动
./stop.sh      # 停止
./restart.sh   # 重启
```

日志文件: `/var/log/zectrix_hot.log`

## 依赖

```bash
pip install requests
```