# API websocket used tyo download Youtube video locally

## Requirements
* docker

## How to run it
depending your system, build & run

* watcher ll see new file from ../volume/subtitles
* compose chapters with file .srt throught ollama/mistral
* write it into ../volume/chapters

## Build
```bash
[Windows] docker build -t chapter-synthesis:1.00 .
[Powershell] docker build -t chapter-synthesis:1.00 .
[Linux] sudo docker build -t chapter-synthesis:1.00 .
```

## Run
```bash 
[Windows] docker run -it --rm --name "chapter-synthesis_1.00" -v "%cd%\..\volumes\subtitles":/etc/chapter-synthesis/subtitles -v "%cd%\..\volumes\chapters":/etc/chapter-synthesis/chapters chapter-synthesis:1.00
[Powershell] docker run -it --rm --name "chapter-synthesis_1.00" -v "$($PWD.Path)\..\volumes\subtitles:/etc/chapter-synthesis/subtitles" -v "$($PWD.Path)\..\volumes\chapters:/etc/chapter-synthesis/chapters" chapter-synthesis:1.00
[Linux] sudo docker run -it --rm --name "chapter-synthesis_1.00" -v "`pwd`/../volumes/subtitles":/etc/chapter-synthesis/subtitles -v "`pwd`/../volumes/chapters":/etc/chapter-synthesis/chapters chapter-synthesis:1.00
```
