import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def authenticate(client_secrets_path):
    credentials = None
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json')
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, ['https://www.googleapis.com/auth/youtube.upload'])
            credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())
    return credentials

def upload_video(client_secrets_path, video_path, title, description, privacy_status='public'):
    credentials = authenticate(client_secrets_path)
    youtube = build('youtube', 'v3', credentials=credentials)

    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': [],  # Добавьте теги, если необходимо
            'categoryId': 22,  # Категория видео (22 - People & Blogs)
        },
        'status': {
            'privacyStatus': privacy_status,
        },
    }

    media_file = MediaFileUpload(video_path)

    upload_request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media_file
    )

    response = upload_request.execute()

    print(f"Видео успешно загружено! ID видео: {response['id']}")

if __name__ == "__main__":
    client_secrets_path = 'client_secret_123498228155-t7dmbh3ro0qn0tmpagmb206c3aim41ei.apps.googleusercontent.com.json'
    video_path = 'asd.mp4'
    title = 'sdafgо'
    description = 'Вsdggfgидео'
    privacy_status = 'public'  # или 'private' или 'unlisted'

    upload_video(client_secrets_path, video_path, title, description, privacy_status)
