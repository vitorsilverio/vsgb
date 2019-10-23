FROM gitpod/workspace-full

RUN sudo add-apt-repository ppa:pypy/ppa \
 && sudo apt-get update \
 && sudo apt-get install -y \
    libgdbm5 \
    freeglut3-dev \
    pypy3 \
    libjack-dev \
    libasound-dev \
 && sudo rm -rf /var/lib/apt/lists/*
