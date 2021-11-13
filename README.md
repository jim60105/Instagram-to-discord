# Instagram to discord post images

This script executes 2 actions:

1. Monitors for new image posted / new story in a instagram account.
1. If found new image / story, a bot posts it to a discord channel.
1. Repeat after set interval.

## Difference from upstream

1. Change instagram scraper implementation from html parsing to [Instaloader](https://github.com/instaloader/instaloader) python module
1. Add monitoring Instagram Stories (login needed)
1. Structure Rewritten by AltF2 [> Commit](https://github.com/NewCircuit/Instagram-to-discord/commit/53e174232cf11e066a4d743872227149862dd1cd)
1. "Skip first run" feature: If set to true, the status of the last post will be detected when started, instead of sending the last post.
1. Dockerized

## Requirements

- Python v3

## Usage

- Copy over the config.example.yml

    ```shell
    cp config.example.yml config.yml
    ```

- Fill out config.yml

- Docker Compose up

    ```shell
    docker-compose up -d
    ```

## Collaborations

Collaborations to improve script are always welcome.
