FROM python:3-alpine
USER root
ADD ./dist/* /dist/
RUN apk add \
      --no-cache --update --virtual .build-deps build-base libffi-dev openssl-dev \
    && pip3 install /dist/nexus3_cli*.whl \
    && apk del .build-deps \
    && rm -rf ~/.cache/pip
CMD ["/usr/local/bin/nexus3"]
