# For githook project
# @version 1.0

FROM python:3.11
LABEL maintainer="chariothy@gmail.com"

ARG UNAME=henry
ARG UID=1000
ARG GID=1000

EXPOSE 8000

ENV HOST=0.0.0.0

ENV GITHOOK_MAIL_FROM="Henry TIAN <chariothy@gmail.com>"
ENV GITHOOK_MAIL_TO="Henry TIAN <chariothy@gmail.com>"

ENV GITHOOK_SMTP_HOST=smtp.gmail.com
ENV GITHOOK_SMTP_PORT=25
ENV GITHOOK_SMTP_USER=chariothy@gmail.com
ENV GITHOOK_SMTP_PWD=password

ENV GITHOOK_PROJECT_BASE_DIR=/app

ENV GITHOOK_NOTIFY_MAIL=1
ENV GITHOOK_NOTIFY_DINGTALK=1

ENV GITHOOK_DINGTALK_TOKEN=DINGTALK_BOT_TOKEN
ENV GITHOOK_DINGTALK_SECRET=DINGTALK_BOT_SECRET

ENV GITHOOK_RELOAD=0

COPY ./requirements.txt .

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
  && echo 'Asia/Shanghai' > /etc/timezone \
  && pip install -U pip \
  && pip install --no-cache-dir -r ./requirements.txt \
  && groupadd -g $GID -o $UNAME \
  && useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME \
  && usermod -G root $UNAME
  
USER $UNAME

WORKDIR /app/githook

CMD [ "python", "main.py" ]