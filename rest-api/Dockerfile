FROM gliderlabs/alpine

LABEL maintainer="ns.gavalas@gmail.com"
LABEL version="0.1.0"
LABEL description="Builds the Elastest Bigdata service docker image."

WORKDIR /app
COPY . /app

# RUN apk --update add python3 py3-pip openssl ca-certificates \
#     && pip3 install -r /app/requirements.txt && rm /app/requirements.txt
RUN apk --update add python py-pip openssl ca-certificates xz \
    && pip install -r /app/src/requirements.txt 

ENV EBS_PORT 5000
# ENV ESM_CHECK_PORT 5000
# ENV ESM_MONGO_HOST localhost

# EXPOSE 8080
EXPOSE 5000

CMD ["/usr/bin/python", "/app/src/runebs.py"]
