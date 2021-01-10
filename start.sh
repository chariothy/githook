#! /bin/bash
SERVICE=githook

command -v docker-compose
if [ $? -eq 0 ]; then
    echo -------------------------------------------
    printf "|         !!! DEBUG mode !!!\n"

    if [ "$DEBUG" == "1" ]; then
        DC_COMMAND="docker-compose up"
    else
        DC_COMMAND="docker-compose up -d"
    fi
    printf "| Command           : $DC_COMMAND\n"
    echo -------------------------------------------
    docker-compose build \
        --build-arg UNAME=$(whoami) \
        --build-arg UID=$(id -u) \
        --build-arg GID=$(id -g) $SERVICE \
    && $DC_COMMAND

    if [ "$DEBUG" == "0" ]; then
        docker-compose logs -f --tail=10
    fi
else
    pip3 install -r ./requirements.txt
    python3 main.py
fi