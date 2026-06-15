import signal
import os
import time
import datetime
import ollama

DIR_ROOT            = os.path.dirname(__file__)
FILE_PROMPT_TPL     = os.path.join(DIR_ROOT, "prompt.txt")
DIR_SUBTITLES       = os.path.join(DIR_ROOT, "subtitles")
DIR_CHAPTERS        = os.path.join(DIR_ROOT, "chapters")

class Server():

    def __init__(self):

        self.running = True

        def handler(signum, frame):
            self.running = False
        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)

        with open(FILE_PROMPT_TPL, 'r') as fd:
            self.prompt_template = fd.read()

        print('[Chapter synthesis] Start watcher')
        self.watch()

    def watch(self):

        while self.running:

            now_utc = datetime.datetime.now(datetime.timezone.utc).timestamp()

            # List existing chapters
            chapters: list[str] = []
            items = os.listdir(DIR_CHAPTERS)
            for item in items:
                if item.endswith('.txt'):
                    chapters.append(item[0:-4])

            # Look at subtitles
            items = os.listdir(DIR_SUBTITLES)
            for item in items:
                if item.endswith('.srt'):
                    path = os.path.join(DIR_SUBTITLES, item)
                    stat = os.stat(path)
                    aged = int(now_utc) - int(stat.st_mtime)
                    if aged > 30:
                        video_hash = item[0:-4]
                        if video_hash not in chapters:
                            self.process(video_hash)

            time.sleep(1)

    def process(self, video_hash: str):
        srt_path = os.path.join(DIR_SUBTITLES, video_hash+'.srt')
        chp_path = os.path.join(DIR_CHAPTERS, video_hash+'.txt')

        # skip if chapter exists
        if os.path.isfile(chp_path):
            return

        content_srt = ""
        with open(srt_path, 'r', encoding='utf-8') as fd:
            content_srt = fd.read() 
        if content_srt=="":
            return

        print('[Chapter synthesis] ({}) Start process'.format(video_hash))
        response = ollama.generate(
            model='mistral',
            prompt=self.prompt_template.replace('{srt_content_file}', content_srt)
        )
        with open(chp_path, "w", encoding="utf-8") as fd:
            fd.write(response['response'].strip())

        print('[Chapter synthesis] ({}) Process complete'.format(video_hash))

if __name__ == "__main__":
    Server()