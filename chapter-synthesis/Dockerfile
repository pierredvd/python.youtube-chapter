FROM debian:trixie-slim

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
                   libncursesw6 \
                   procps \
                   zstd; \
    \
    apt install -y python3.13 \
                   python3.13-venv \
                   python3-pip; \
    \
    cd /tmp; \
    curl -fsSL https://ollama.com/install.sh | sh

RUN ollama serve & > /dev/null && sleep 1 && ollama pull mistral

RUN mkdir -p /etc/chapter-synthesis

COPY ./src/ /etc/chapter-synthesis/
COPY ./init.sh /usr/bin/init.sh

WORKDIR /etc/chapter-synthesis

RUN chmod 0775 /usr/bin/init.sh; \
    chmod -R 0775 /etc/chapter-synthesis; \
    pip install -r requirements.txt --break-system-packages; \
    \
    rm -rf /tmp/*; \
    rm -rf /var/lib/apt/lists/*

VOLUME 	["/etc/chapter-synthesis/subtitles", "/etc/chapter-synthesis/chapters"]
CMD 	["sh", "/usr/bin/init.sh"]