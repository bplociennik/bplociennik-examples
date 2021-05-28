FROM golang:1.16.4-stretch

ENV PROJECT_DIR=/project/app \
    GO111MODULE=auto \
    CGO_ENABLED=0

## Install required packages
## - git to fetch golang dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
    && rm -rf /var/lib/apt/lists/*

## Set the current working directory inside the container
WORKDIR $PROJECT_DIR

## Install dependencies from go.mod file and verify it also
COPY go.mod .
COPY go.sum .
RUN go mod download
RUN go mod verify

## Install additional dependencies
RUN go get github.com/githubnemo/CompileDaemon

## Run watcher to automatically rebuild app after any change in code
CMD CompileDaemon --build="go build src/main.go" --command="./main" --color
