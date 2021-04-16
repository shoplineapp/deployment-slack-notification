FROM alpine:3.13.5

RUN apk update && apk add curl bash jq && rm -rf /var/cache/apk/*

COPY pipe.sh /

ENTRYPOINT ["/pipe.sh"]
