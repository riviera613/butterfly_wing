```bash
# 安装依赖
pip3 install -r requirement.txt

# 构建数据库（先在settings.py中写好数据库连接配置）
# 如果发现缺少其他依赖可手动通过pip3安装
python3 manage.py makemigrations
python3 manage.py migrate

# 创建管理员账号
python3 manage.py createsuperuser

# 调试环境启动
python3 manage.py runserver

# 生产环境部署
# 收集静态文件
python3 manage.py collectstatic
# 修改uwsgi.ini文件，修改其中的配置项为当前环境的内容
vi uwsgi.ini
# 修改settings.py中的 DUBUG 为 False
vi env_protect/setting.spy
# 启动服务
uwsgi --ini uwsgi.ini
```