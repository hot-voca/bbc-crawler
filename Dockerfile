FROM alpine:edge
MAINTAINER Dominic Lee
RUN apk --update --no-cache add py2-pip ca-certificates musl-dev musl-utils musl-dbg gcc libevent-dev python2-dev \
  libxml2-dev libxslt-dev libffi-dev openssl-dev
RUN pip install --no-cache-dir --upgrade pip
RUN cp -r /usr/include/libxml2/libxml/ /usr/include
RUN pip install --no-cache-dir scrapy scrapyd pymongo