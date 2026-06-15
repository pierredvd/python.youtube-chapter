# API websocket used tyo download Youtube video locally

## Requirements
* docker

## How to run it
depending your system, build & run

## How it works
* watcher ll see new file from ../volume/videos
* extract mp3
* transcript it to substitile file .srt using whisper
* write it into ../volume/subtitles

## Build
```bash
[Windows] docker build -t video-transcriptor:1.00 .
[Powershell] docker build -t video-transcriptor:1.00 .
[Linux] sudo docker build -t video-transcriptor:1.00 .
```

## Run
```bash 
[Windows] docker run -it --rm --name "video-transcriptor_1.00" -v "%cd%\..\volumes\videos":/etc/video-transcriptor/videos -v "%cd%\..\volumes\subtitles":/etc/video-transcriptor/subtitles video-transcriptor:1.00
[Powershell] docker run -it --rm --name "video-transcriptor_1.00" -v "$($PWD.Path)\..\volumes\videos:/etc/video-transcriptor/videos" -v "$($PWD.Path)\..\volumes\subtitles:/etc/video-transcriptor/subtitles" video-transcriptor:1.00
[Linux] sudo docker run -it --rm --name "video-transcriptor_1.00" -v "`pwd`/../volumes/videos":/etc/video-transcriptor/videos -v "`pwd`/../volumes/subtitles":/etc/video-transcriptor/subtitles video-transcriptor:1.00
```
