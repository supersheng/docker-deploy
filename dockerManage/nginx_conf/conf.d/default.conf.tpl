server {
    listen       80;
    server_name  reboot.linrc.com;

#apps = [{
#   "name": "vote",
#       "upstream": [{
#           "host":"127.0.0.1",
#           "port":1122
#       },]
#},]

#upstream backend {
#    server backup1.example.com:8080;
#    server backup2.example.com:8080;
#}
#
#server {
#    location / {
#        proxy_pass http://backend;
#    }
#}



    {% for app in apps %}
        location /{{ app["name"] }} {
        # proxy_pass   http://127.0.0.1;
        {% for up in app["upstream"] %}
            proxy_pass   http://{{ up["host"] }}:{{ up["port"] }};
        {% endfor %}
        }
    {% endfor %}
    

    location = /50x.html {
        root   /usr/share/nginx/html;
    }

}

