# 环境
1. Python3 + Django 2
2. djangorestframework 3
3. requests 2
4. lxml 4

# 安装依赖包
- pip install -r requirements.txt

# 配置
## 代理池配置
- 代理池在spider/data_getter.py中，修改变量proxy_pool数组则可更改代理池

## 数据服务器设置
- 如果更改数据服务器地址则更改spider/dump.py中变量server

# 部署问题
- 目前已经将Django+Spider+tinyproxy部署到23.83.243.75
- 172.93.33.29与138.128.199.17仅部署tinyproxy

# 启动
## 启动Django
    python3 manage.py runserver 0.0.0.0:8000 >> log &2>&1 &

## 启动爬虫
    cd spider
    python3 controller.py >> spider.log &2>&1 &

## 启动代理
    python3 tinyproxy 8989 >> proxy.log &2>&1 &

# 日志
## API日志
- log
## 爬虫日志（主要为脏数据）
- spider/spider.log
## 代理日志
- proxy.log