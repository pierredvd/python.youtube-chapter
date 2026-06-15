# Generate chapter file from youtube video

## Requirements
* docker

## Global Stac
- Docker
- Python 3.9+
- FFMEG (convert mp4 to mp3)
- Whisper (transcript mp3 to text)
- Ollama + Mistral (chapter synthesis)

## How to run it
```
docker-compose --build
docker compose up -d
```
_Select youtube to download at http://localhost:8080 in tour browser_

_All volumes into ./volumes_

## Process pipeline

* youtube-downloader
    - api-rest [http://localhost:8080]
    - download video mp4 through API
    - write video into /volumes/videos
* video-transcriptor
    - read video from /volumes/videos
    - convert mp4 to mp3 with ffmpeg
    - transcript mp3 to segments (whisper)
    - pack segments into subtitle .srt
    - write subtitle into /volumes/subtitles
* chapter-composer
    - read subtitle into /volumes/subtitles
    - chapter synthesis (ollama/mistral)
    - write chapter into /volumes/chapters

## Note:
The model used for the chapter summary is Mistral 2B so that even those with less powerful machines can start the project and see results in minutes. However, this model is somewhat too limited for the task at hand. The goal of this demonstrator is to show how to structure a complex process quite simply by breaking it down into simpler steps.