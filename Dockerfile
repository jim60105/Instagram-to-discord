FROM python:alpine

WORKDIR /usr/src/app
COPY requirements.txt .

RUN apk add --no-cache --virtual build-deps \
      gcc \
      libc-dev && \
    apk add --no-cache \
      dumb-init && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del build-deps

ENV FIRST_RUN=true

COPY main.py .
ADD src src/
COPY config.example.yml config.yml


ENTRYPOINT [ "/usr/bin/dumb-init", "--", "python", "-u", "main.py" ]