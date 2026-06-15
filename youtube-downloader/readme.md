# API websocket used tyo download Youtube video locally

## Requirements
* docker

## How to run it
depending your system, build & run

## How it works
* API exposed at http://localhost:8080
* videos selected ll be downloaded into ../volume/videos

## Build
```bash
[Windows] docker build -t youtube-downloader:1.00 .
[Powershell] docker build -t youtube-downloader:1.00 .
[Linux] sudo docker build -t youtube-downloader:1.00 .
```

## Run
```bash 
[Windows] docker run -it --rm --name "youtube-downloader_1.00" -p 8080:8080 -v "%cd%\..\volumes\videos":/etc/youtube-downloader/download youtube-downloader:1.00
[Powershell] docker run -it --rm --name "youtube-downloader_1.00" -p 8080:8080 -v "$($PWD.Path)\..\volumes\videos:/etc/youtube-downloader/download" youtube-downloader:1.00
[Linux] sudo docker run -it --rm --name "youtube-downloader_1.00" -p 8080:8080 -v "`pwd`/../volumes/videos":/etc/youtube-downloader/download youtube-downloader:1.00
```