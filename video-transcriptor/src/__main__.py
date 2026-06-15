import signal
import os
import time
import sys
import datetime
from moviepy.editor import VideoFileClip
import whisper

DIR_ROOT            = os.path.dirname(__file__)
DIR_VIDEOS          = os.path.join(DIR_ROOT, "videos")
DIR_TRANSCRIPTIONS  = os.path.join(DIR_ROOT, "subtitles")

class Server():

    def __init__(self):

        self.running = True

        def handler(signum, frame):
            self.running = False
        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)

        print('[Video transcriptor] Load whisper model')
        self.whisper_model = whisper.load_model("base")
        print('[Video transcriptor] Start watcher')
        self.watch()

    def watch(self):

        while self.running:

            now_utc = datetime.datetime.now(datetime.timezone.utc).timestamp()

            # List existing transcriptions
            transcriptions: list[str] = []
            items = os.listdir(DIR_TRANSCRIPTIONS)
            for item in items:
                if item.endswith('.srt'):
                    transcriptions.append(item[0:-4])

            # Look at videos
            items = os.listdir(DIR_VIDEOS)
            for item in items:
                if item.endswith('.mp4'):
                    path = os.path.join(DIR_VIDEOS, item)
                    stat = os.stat(path)
                    aged = int(now_utc) - int(stat.st_mtime)
                    if aged > 30:
                        video_hash = item[0:-4]
                        if video_hash not in transcriptions:
                            self.process(video_hash)

            time.sleep(1)

    def process(self, video_hash: str):
        mp4_path = os.path.join(DIR_VIDEOS, video_hash+'.mp4')
        mp3_path = os.path.join(DIR_TRANSCRIPTIONS, video_hash+'.mp3')
        srt_path = os.path.join(DIR_TRANSCRIPTIONS, video_hash+'.srt')

        # skip if transcription exists
        if os.path.isfile(srt_path):
            return

        # mp4 to mp3
        if not os.path.isfile(mp3_path):
            print('[Video transcriptor] ({}) Convert mp4 to mp3'.format(video_hash))
            video = VideoFileClip(mp4_path)
            video.audio.write_audiofile(mp3_path, logger=None)
            video.close()

        # transcriptions
        print('[Video transcriptor] ({}) Transcript mp3 to srt'.format(video_hash))
        results = self.whisper_model.transcribe(mp3_path, fp16=False)
        with open(srt_path, "w+", encoding="utf-8") as fd:
            # convert transcription as subtitles
            index = 0
            for segment in results["segments"]:
                index += 1
                fd.write("{index}\n{start} --> {finish}\n{text}\n\n".format(
                    index   = index,
                    start   = self.srt_time_format(segment["start"]),
                    finish  = self.srt_time_format(segment["end"]),
                    text    = segment["text"].strip()
                ))

        # remove mp3
        os.remove(mp3_path)

        print('[Video transcriptor] ({}) Process complete'.format(video_hash))

    def srt_time_format(self, seconds):
        # Format time to SRT (HH:MM:SS,mmm)
        hours       = int(seconds / 3600)
        minutes     = int((seconds % 3600) / 60)
        secs        = int(seconds % 60)
        millisecs   = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

if __name__ == "__main__":
    Server()