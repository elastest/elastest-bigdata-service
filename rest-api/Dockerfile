FROM gliderlabs/alpine

# Set labels
LABEL maintainer="s.gioldasis@gmail.com"
LABEL description="Builds the Elastest Bigdata service docker image."
ARG GIT_COMMIT=unspecified
LABEL git_commit=$GIT_COMMIT
ARG COMMIT_DATE=unspecified
LABEL commit_date=$COMMIT_DATE
ARG VERSION=unspecified
LABEL version=$VERSION

WORKDIR /app
COPY . /app

# RUN apk --update add python3 py3-pip openssl ca-certificates \
#     && pip3 install -r /app/requirements.txt && rm /app/requirements.txt
RUN apk --update add python py-pip openssl ca-certificates xz \
    && pip install -r /app/src/requirements.txt && rm /app/src/requirements.txt

ENV EBS_PORT 5000
# ENV ESM_CHECK_PORT 5000
# ENV ESM_MONGO_HOST localhost

# EXPOSE 8080
EXPOSE 5000

CMD ["/usr/bin/python", "/app/src/runebs.py"]
