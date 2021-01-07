IMG_NAME=githook
CON_NAME=githook
RUN="uvicorn main:app --host 0.0.0.0 --reload"
PORT=8000
PROJ_ROOT=/www

echo -------------------------------------------
printf "| IMAGE NAME     : $IMG_NAME\n"
printf "| CONTAINER NAME : $CON_NAME\n"
printf "| PORT           : $PORT\n"
printf "| PROJECT ROOT   : $PROJ_ROOT\n"
printf "| COMMAND        : $RUN\n"
echo -------------------------------------------

docker stop $CON_NAME && docker rm $CON_NAME
docker build --build-arg UNAME=$(whoami) --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t $IMG_NAME .

# If successfully building docker image
if [ $? -eq 0 ]; then
    docker run --name $CON_NAME \
        --restart unless-stopped \
        -p $PORT:8000 \
        -v $PROJ_ROOT:/app \
        -v /etc/localtime:/etc/localtime \
        -v /usr/bin/git:/usr/bin/git \
        -v ~/.ssh:/home/$(whoami)/.ssh
        -w /app/$CON_NAME \
        -e GITHOOK_SMTP_PWD=$SMTP_PASSWORD
        -itd $IMG_NAME \
        $RUN