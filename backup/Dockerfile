FROM alpine:latest

RUN apk add --no-cache \
    bash \
    postgresql-client \
    tzdata \
    curl \
    coreutils \
    gettext

COPY backup.sh /usr/local/bin/backup.sh
COPY crontab.tpl /app/crontab.tpl

RUN chmod +x /usr/local/bin/backup.sh

CMD sh -c "\
    envsubst < /app/crontab.tpl > /etc/crontabs/root && \
    crond -f -l 2"
