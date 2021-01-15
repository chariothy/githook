#! /bin/bash
SERVICE=githook

dump() 
{
    VARNAME=$1
    VARVAL=`eval echo '$'"$VARNAME"`
    DEFAULT="(default: $2)"
    printf "    %15s = %-35s %s\n" "$VARNAME" "$VARVAL" "$DEFAULT"
}

usage()
{
    echo ================================================================================
    echo "请为docker添加以下环境变量 (如果直接使用python，请在变量前加上前缀 GITHOOK_ )"
    dump 'MAIL_FROM' 'Henry TIAN <chariothy@gmail.com>'
    dump 'MAIL_FROM' 'Henry TIAN <chariothy@gmail.com>'
    dump 'MAIL_TO' 'Henry TIAN <chariothy@gmail.com>'
    dump 'SMTP_HOST' 'smtp.gmail.com'
    dump 'SMTP_PORT' 25
    dump 'SMTP_USER' 'chariothy@gmail.com'
    dump 'SMTP_PWD'
    dump 'PROJ_ROOT' '/app'
    dump 'NOTIFY_MAIL' '1'
    dump 'NOTIFY_DINGTALK' '1'
    dump 'GITHOOK_RELOAD' '1'
    dump 'DINGTALK_TOKEN'
    dump 'DINGTALK_SECRET'
    echo ================================================================================

exit
}

if [ -z $SMTP_PWD ];then
    usage
fi

if [ -z $DINGTALK_TOKEN ];then
    usage
fi

if [ -z $DINGTALK_SECRET ];then
    usage
fi

command -v docker-compose
if [ $? -eq 0 ]; then
    echo -------------------------------------------

    if [ "$DEBUG" == "1" ]; then
        DC_COMMAND="docker-compose up"
        printf "|         !!! DEBUG mode !!!\n"
    else
        DC_COMMAND="docker-compose up -d"
    fi
    printf "| Command           : $DC_COMMAND\n"
    echo -------------------------------------------
    docker-compose down
    docker-compose build \
        --build-arg UNAME=$(whoami) \
        --build-arg UID=$(id -u) \
        --build-arg GID=$(id -g) $SERVICE \
    && $DC_COMMAND

    if [ "$DEBUG" != "1" ]; then
        docker-compose logs -f --tail=10
    fi
else
    pip3 install -r ./requirements.txt
    python3 main.py
fi