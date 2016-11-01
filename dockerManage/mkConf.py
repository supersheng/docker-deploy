#!/usr/bin/env python
# coding=utf-8
from startContainer import Container
from jinja2 import Template
import os,sys,json

image = 'tiangolo/uwsgi-nginx-flask'
service_port = 80

# 命令行传入一个app_name的参数，比如vote或是check，对应各自的app程序
if len(sys.argv) != 2:
    print "You must input 1 Argument for app name!"
else:
    app_name = sys.argv[1]
    app_parent_path = os.path.split(os.getcwd())[0]
    app_path = app_parent_path + '/app/' + app_name # 获取到 app_name 所在的路径
    app_new_ip = Container().start(image, app_name=app_name, app_path=app_path, service_port=service_port) # 新建app容器返回容器IP

app_list = []
apps = json.load(file(app_parent_path + '/app/apps.json'))

#以下判断apps是否存在传入的app_name，存在则只加upstream里的host信息，不存在则apps加name和upstream组成的字典
if len(apps):
    for app in apps:
        app_list.append(app['name'])
    if app_name in app_list:
        app_name_index = app_list.index(app_name)
        apps[app_name_index]['upstream'].append({'host': app_new_ip, 'port': service_port})
    else:
        apps.append({'name': app_name, 'upstream': [{'host': app_new_ip, 'port': service_port}]})
else:
    apps.append({'name': app_name, 'upstream': [{'host': app_new_ip, 'port': service_port}]})

with open("nginx_conf/conf.d/default.conf.tpl") as f:
    with open("nginx_conf/conf.d/default.conf", "w") as fw:
        temp = Template(f.read())
        fw.write(temp.render(apps=apps))

json.dump(apps, open(app_parent_path + '/app/apps.json', 'w'))
print os.popen("docker exec nginx /usr/sbin/nginx -s reload").read()
