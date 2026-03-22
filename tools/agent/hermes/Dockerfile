FROM debian:trixie-slim

RUN apt update -y && apt install -y curl git xz-utils

RUN curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash