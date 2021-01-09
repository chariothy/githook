PROJ_NAME=githook
AUTHOR=chariothy
IMG_NAME=githook
CON_NAME=githook
COMMAND="uvicorn main:app --host '${HOST:-0.0.0.0}' --reload"

echo -------------------------------------------
printf "| Project           : $PROJ_NAME\n"
printf "| Author            : $AUTHOR\n"
printf "| Image             : $IMG_NAME\n"
printf "| Container         : $CON_NAME\n"
printf "| Command           : $COMMAND\n"
echo -------------------------------------------

command -v docker-compose
if [ $? -eq 0 ]; then
    export UNAME=$(whoami)
    docker-compose -f docker-compose-dev.yml build \
        --build-arg UNAME=$(whoami) \
        --build-arg UID=$(id -u) \
        --build-arg GID=$(id -g) \
    && docker-compose -f docker-compose-dev.yml up
else
    command -v docker
    if [ $? -eq 0 ]; then
        docker run --name $CON_NAME \
            --restart unless-stopped \
            -p ${PORT:-8000}:8000 \
            -v ${PROJ_ROOT:-/www}:/app \
            -v /usr/bin/git:/usr/bin/git \
            -v ~/.ssh:/home/$(whoami)/.ssh \
            -w /app/$PROJ_NAME \
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
            -itd $AUTHOR/$IMG_NAME \
            $COMMAND
    else
        pip3 install -r ./requirements.txt
        COMMAND=$COMMAND --port ${PORT:-8000}
        $COMMAND
    fi
fi