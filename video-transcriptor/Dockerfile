FROM debian:trixie-slim
EXPOSE 	8080

RUN set -eux; \
    apt update; \
    apt install -y build-essential \
                   zlib1g-dev \
                   libncurses-dev \
                   libgdbm-dev \
                   libnss3-dev \
                   libssl-dev \
                   libreadline-dev \
                   libffi-dev \
                   libsqlite3-dev \
                   wget \
                   curl \
                   llvm \
                   libbz2-dev \
                   xz-utils \
                   tk-dev \
                   liblzma-dev \
                   libncursesw6; \
    \
    apt install -y python3.13 \
                   python3.13-venv \
                   python3-pip \
                   ffmpeg;\
    \
    mkdir -p /etc/video-transcriptor

COPY ./src/ /etc/video-transcriptor/

WORKDIR /etc/video-transcriptor
RUN chmod -R 0775 /etc/video-transcriptor; \
    pip install -r requirements.txt --break-system-packages; \
    \
    rm -rf /tmp/*; \
    rm -rf /var/lib/apt/lists/*

VOLUME 	["/etc/video-transcriptor/videos", "/etc/video-transcriptor/subtitles"]
CMD 	["python3", "."]