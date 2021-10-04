FROM alpine:3.13.6 as base

RUN apk add python3 libxml2 libxslt

WORKDIR /app

# create agora user
RUN ["adduser", "-D", "agora"]

FROM base as dev

RUN apk add py3-pip npm yarn make g++ libxml2-dev libxslt-dev python3-dev musl-dev gcc linux-headers
RUN yarn global add parcel

USER agora

ENV FLASK_ENV development
CMD ["tail", "-f", "/dev/null"]

FROM dev as builder

USER root

COPY . .

RUN ["make", "clean"]
RUN ["make", "build"]

FROM base as prod

RUN apk add nginx

COPY --from=builder /app/app ./app
COPY --from=builder /app/venv ./venv
COPY --from=builder /app/conf/prod.ini .
COPY --from=builder /app/conf/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/scripts/run-prod.sh .

ENV FLASK_ENV production
ENTRYPOINT ["./run-prod.sh"]