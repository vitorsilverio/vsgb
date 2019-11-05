FROM gitpod/workspace-full-vnc

RUN sudo apt-get update \
 && sudo apt-get install -y \
    freeglut3-dev \
    libjack-dev \
    libasound-dev \
 && sudo rm -rf /var/lib/apt/lists/*
