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

ENV GITHOOK_SMTP_PWD=password

VOLUME [ "/etc/localtime", "/usr/bin/git", "/home/$UNAME/.ssh"]  /etc/localtime
COPY ./requirements.txt .

RUN pip install -U pip \
  && pip install --no-cache-dir -r ./requirements.txt \
  && groupadd -g $GID -o $UNAME \
  && useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME \
  && usermod -G root $UNAME
USER $UNAME

WORKDIR /app

COPY . .

CMD [ "uvicorn", "main:app", "--host 0.0.0.0", "--reload" ]