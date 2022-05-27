from googleapiclient.http import MediaFileUpload
from Google import Create_Service
import socket

API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
global service


def setter(CLIENT_SECRET_FILE):
    global service
    socket.setdefaulttimeout(30000)
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def upload_video(request_body, current_dir):

    print(service)

    render_path = current_dir + "render.mp4"
    media_file = MediaFileUpload(render_path)
    thumbnail_path = current_dir + "thumbnail.jpg"
    socket.setdefaulttimeout(30000)

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media_file
    ).execute()

    service.thumbnails().set(
        videoId=response_upload.get('id'),
        media_body=MediaFileUpload(thumbnail_path)
    ).execute()
