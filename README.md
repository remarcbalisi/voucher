## How to Deploy

#### Install Nginx Web Server

```shell
apt-get install nginx -y
```

Once the Nginx is installed, start and enable the Nginx service using the following command:
```shell
systemctl start nginx
systemctl enable nginx
```

#### Create a WSGI Entry Point for Gunicorn

`nano ./voucher/wsgi.py`

Add the following lines:
```python
from voucher.index import app
if __name__ == "__main__":
    app.run()
```

Save and close the file then verify whether Gunicorn can serve the application correctly using the command below:
`gunicorn --bind 0.0.0.0:5000 wsgi:app`

#### Create a Systemd Service File for Flask Application
`vim /etc/systemd/system/flask.service`

Add the following lines:

```shell
[Unit]
Description=Gunicorn instance to serve Flask
After=network.target
[Service]
User=root
Group=www-data
WorkingDirectory=/root/project
Environment="PATH=/root/project/venv/bin"
ExecStart=/root/project/venv/bin/gunicorn --bind 0.0.0.0:5000 wsgi:app
[Install]
WantedBy=multi-user.target
```

Save and close the file then set proper ownership and permission to flask project:
```shell
chown -R root:www-data /root/project
chmod -R 775 /root/project
```

Next, reload the systemd daemon with the following command:

```shell
systemctl daemon-reload
```

Next, start the flask service and enable it to start at system reboot:

```shell
systemctl start flask
systemctl enable flask
```

Next, verify the status of the flask with the following command:
```shell
systemctl status flask
```

Output:
```shell
● flask.service - Gunicorn instance to serve Flask
     Loaded: loaded (/etc/systemd/system/flask.service; disabled; vendor preset: enabled)
     Active: active (running) since Thu 2021-12-23 10:38:26 UTC; 8s ago
   Main PID: 9376 (gunicorn)
      Tasks: 2 (limit: 2353)
     Memory: 27.8M
     CGroup: /system.slice/flask.service
             ├─9376 /root/project/venv/bin/python3 /root/project/venv/bin/gunicorn --bind 0.0.0.0:5000 wsgi:app
             └─9393 /root/project/venv/bin/python3 /root/project/venv/bin/gunicorn --bind 0.0.0.0:5000 wsgi:app

Dec 23 10:38:26 ubuntu2004 systemd[1]: Started Gunicorn instance to serve Flask.
Dec 23 10:38:26 ubuntu2004 gunicorn[9376]: [2021-12-23 10:38:26 +0000] [9376] [INFO] Starting gunicorn 20.1.0
Dec 23 10:38:26 ubuntu2004 gunicorn[9376]: [2021-12-23 10:38:26 +0000] [9376] [INFO] Listening at: http://0.0.0.0:5000 (9376)
Dec 23 10:38:26 ubuntu2004 gunicorn[9376]: [2021-12-23 10:38:26 +0000] [9376] [INFO] Using worker: sync
Dec 23 10:38:26 ubuntu2004 gunicorn[9393]: [2021-12-23 10:38:26 +0000] [9393] [INFO] Booting worker with pid: 9393
```

#### Configure Nginx as a Reverse Proxy for Flask Application
Next, you will need to configure Nginx as a reverse proxy to serve the Flask application through port 80. To do so, create an Nginx virtual host configuration file:

```shell
vim /etc/nginx/conf.d/flask.conf
```

Add the following lines:

```shell
server {
    listen 80;
    server_name flask.example.com;
    location / {
        include proxy_params;
        proxy_pass  http://127.0.0.1:5000;
    }
}
```

Save and close the file then verify the Nginx for any syntax error:

```shell
nginx -t
```

You should see the following output:

```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

Finally, restart the Nginx service to apply the changes:

```shell
systemctl restart nginx
```

## Running migrations

```shell
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```