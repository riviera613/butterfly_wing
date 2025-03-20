```bash
pip3 install -r requirement.txt

# 构建数据库（先在settings.py中写好数据库连接配置）
# 如果发现缺少其他依赖可手动通过pip3安装
python3 manage.py makemigrations
python3 manage.py migrate

# 修改settings.py中的数据库连接、微信登录等为当前使用的配置，如有必要可把修改合入git
vi env_protect/setting.py

# 创建管理员账号
python3 manage.py createsuperuser

# 调试环境启动
DJ_CONF=DEBUG python3 manage.py runserver

# 生产环境启动
# 方法1：使用uwsgi
# 收集静态文件
python3 manage.py collectstatic
# 修改uwsgi.ini文件，修改其中的配置项为当前环境的内容
vi uwsgi.ini
# 启动服务
uwsgi --ini uwsgi.ini

# 方法2：使用gunicorn（端口换成实际使用的）
gunicorn env_protect.wsgi:application --bind 0.0.0.0:$PORT
```