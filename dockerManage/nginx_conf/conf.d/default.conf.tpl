{% for app in apps %}
upstream {{ app["name"] }}_backend {
{% for up in app["upstream"] %}
    server {{ up["host"] }}:{{ up["port"] }};
{% endfor %}
}
{% endfor %}
server {
    listen       80;
    server_name  reboot.linrc.com;

{% for app in apps %}

    location /{{ app["name"] }} {
        proxy_pass   http://{{ app["name"] }}_backend;
    }
{% endfor %}
    
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

}
