# For githook project
# @version 1.0

FROM python:3.8
LABEL maintainer="chariothy@gmail.com"

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

ARG TARGETPLATFORM
ARG BUILDPLATFORM

LABEL maintainer="chariothy" \
  org.opencontainers.image.created=$BUILD_DATE \
  org.opencontainers.image.url="https://github.com/chariothy/githook.git" \
  org.opencontainers.image.source="https://github.com/chariothy/githook.git" \
  org.opencontainers.image.version=$VERSION \
  org.opencontainers.image.revision=$VCS_REF \
  org.opencontainers.image.vendor="chariothy" \
  org.opencontainers.image.title="githook" \
  org.opencontainers.image.description="Githook" \
  org.opencontainers.image.licenses="MIT"

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

COPY . .

CMD [ "uvicorn", "main:app", "--host ${HOST}" ]