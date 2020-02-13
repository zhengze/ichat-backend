# ichat-backend

ichat  
是一款基于muse-ui和vue.js的移动端聊天应用，融合了单聊和群聊等功能.  


## 功能

- [x] 注册登录功能
- [x] 聊天功能
- [x] 查看历史记录
- [x] 群聊
- [x] 单聊
- [x] 好友列表
- [x] 群组列表

## 环境
- 系统 ubuntu18.04
- 框架 flask
- 接口协议 restful API和websocket
- 数据库 mysql5.7

## 依赖包
- flask-restful
- flask-cors
- flask-mysql
- flask-sqlalchemy
- flask-socketio
- flask-migrate
- flask-jwt-extended
- pymysql

## 配置
### .flaskenv

### .env

### config.py

### 数据库创建

## python依赖安装
```
$pipenv install
```

## 数据库初始化
```
$flask db init
```

## 数据库迁移
```
$flask db migrate
$flask db upgrade
```

## 运行
```
$python manage.py run
```
