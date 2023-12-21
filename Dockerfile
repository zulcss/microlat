FROM debian:bookworm

RUN apt-get update -y && \
    apt-get install -y python3 \
                      python3-pip \
                      python3-stevedore \
                      python3-click \
                      python3-rich \
                      python3-yaml \
                      mmdebstrap \
                      git