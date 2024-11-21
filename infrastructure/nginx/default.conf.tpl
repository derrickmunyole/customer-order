server {
    listen ${LISTEN_PORT};
    server_name _;

    location /static/ {
        alias /vol/static/;
        autoindex off;
    }

    location / {
        proxy_pass http://${APP_HOST}:${APP_PORT};
        proxy_redirect off;
        client_max_body_size 10M;
    }
}