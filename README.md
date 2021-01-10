# githook

## 功能

- 响应git网站的push事件，并将代码拉取到本地
- 以邮件或钉钉机器人的方式推送消息响应
- 目前仅支持github

## 注意

- 因为需要以本地用户身份在docker中运行，因为不提供docker hub镜像，需要在本地编译镜像

## 说明

- 推荐使用docker-compose运行

    - 请参考[docker-compose.yml](https://github.com/chariothy/githook/blob/main/docker-compose.yml)，并修改其中的相应变量

    - 运行 `docker-compose config` 查看变量是否正确替换

    - 运行 `docker-compose up --build -d && docker-compose logs -f --tail=10`

- 也可以使用docker运行，请参考
``` 
docker run --name ${CON_NAME:-githook} \
    --restart unless-stopped \
    -p ${PORT:-8000}:8000 \
    -v ${PROJ_ROOT:-/www}:/app \
    -v /usr/bin/git:/usr/bin/git \
    -v ~/.ssh:/home/$(whoami)/.ssh \
    -w /app/${PROJ_NAME:-githook} \
    -e GITHOOK_MAIL_FROM=${MAIL_FROM:-"Henry TIAN <chariothy@gmail.com>"} \
    -e GITHOOK_MAIL_TO=${MAIL_TO:-"Henry TIAN <chariothy@gmail.com>"} \
    -e GITHOOK_SMTP_HOST=${SMTP_HOST:-smtp.gmail.com} \
    -e GITHOOK_SMTP_PORT=${SMTP_PORT:-25} \
    -e GITHOOK_SMTP_USER=${SMTP_USER:-chariothy@gmail.com} \
    -e GITHOOK_SMTP_PWD=${SMTP_PWD} \
    -e GITHOOK_PROJECT_BASE_DIR=/app \
    -e GITHOOK_NOTIFY_MAIL=1 \
    -e GITHOOK_NOTIFY_DINGTALK=1 \
    -e GITHOOK_DINGTALK_TOKEN=${DINGTALK_TOKEN} \
    -e GITHOOK_DINGTALK_SECRET=${DINGTALK_SECRET} \
    -itd chariothy/githook:${PYTHON_VER:-3.8} \
    uvicorn main:app --host '${HOST:-0.0.0.0}'
```

- 也可以直接使用python运行，请参考[start.sh](https://github.com/chariothy/githook/blob/main/start.sh)，并修改其中的相应变量

## TODO

- 支持更多的git托管网站