from fastapi import FastAPI, Request, Response, WebSocket
from pytubefix import YouTube
from threading import Thread
import mimetypes
import os
import json
import time
import uvicorn

DIR_ROOT        = os.path.dirname(__file__)
DIR_WWW         = os.path.join(DIR_ROOT, "www")
DIR_DOWNLOAD    = os.path.join(DIR_ROOT, "download")
INDEX_DIRECTORY = "index.htm"
app             = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        video_hash = data
        video_file = os.path.join(DIR_DOWNLOAD, video_hash+'.mp4')
        status_file= os.path.join(DIR_DOWNLOAD, video_hash+'.json')
        if os.path.isfile(video_file):
            print('[Youtube downloader] ({}) Video already downloaded'.format(video_hash))
            await websocket.send_text(json.dumps({
                "hash": video_hash,
                "status": "complete",
            }))
        elif os.path.isfile(status_file):
            await websocket.send_text(json.dumps({
                "hash": video_hash,
                "status": "error",
                "error": "already in progress"
            }))
        else:

            def update_progress(stream, chunk, bytes_remaining):
                filesize = stream.filesize
                downloaded = filesize - bytes_remaining
                print('[Youtube downloader] ({}) Download progress {}/{}'.format(video_hash, downloaded, filesize))
                with open(status_file, 'wb') as fd:
                    if downloaded==filesize:
                        fd.write(json.dumps({
                            "hash": video_hash,
                            "status": "complete",
                            "total": filesize,
                            "downloaded": downloaded
                        }).encode('utf8'))
                    else:
                        fd.write(json.dumps({
                            "hash": video_hash,
                            "status": "progress",
                            "total": filesize,
                            "downloaded": downloaded
                        }).encode('utf8'))

            yt = YouTube(
                "https://www.youtube.com/watch?v="+video_hash,
                on_progress_callback=update_progress
            )
            await websocket.send_text(json.dumps({
                "hash": video_hash,
                "status": "started",
                "title": yt.title
            }))
            stream = yt.streams.get_highest_resolution()
            thread = Thread(
                target=stream.download, 
                kwargs={
                    "output_path":DIR_DOWNLOAD, 
                    "filename":video_hash+".mp4"
                })
            thread.start()

            progress = True
            while progress:
                if os.path.isfile(status_file):
                    with open(status_file, 'r') as fd:
                        data_json = fd.read()
                        await websocket.send_text(data_json)
                        data = json.loads(data_json)
                        if data['status']=="complete":
                            progress = False
                        else:
                            time.sleep(1)

            os.unlink(status_file)

@app.get("/{path:path}")
async def catch_all(request: Request, path: str = ""):
    if path=="":
        path = INDEX_DIRECTORY
    local_path: str = os.path.normpath(os.path.join(DIR_WWW, path.replace("/", os.path.sep)))
    # no xss leak
    if len(local_path)>len(DIR_WWW) and local_path.startswith(DIR_WWW):
        if os.path.isfile(local_path):
            mime, _ = mimetypes.guess_file_type(os.path.basename(local_path), strict=True)
            with open(local_path, 'rb') as fd:
                content = fd.read()
                return Response(content=content, media_type=mime)
    return Response(content=b"""
    <!doctype html>
    <html>
        <body>
            <h1>404 Not found</h1><hr />
        </body>
    </html>
    """, media_type="text/html")

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
