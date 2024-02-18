#!/usr/bin/python
import argparse
import httplib2
import os
import random
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError


httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def initialize_upload(youtube, options):
    tags = options.keywords.split(',') if options.keywords else None
    body = dict(
        snippet=dict(
            title=options.title,
            description=options.description,
            tags=tags,
            categoryId=options.category
        ),
        status=dict(
            privacyStatus=options.privacyStatus
        )
    )
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
    )
    resumable_upload(insert_request)

def resumable_upload(request):
    response = None
    retry = 0
    while response is None:
        try:
            status, response = request.next_chunk()
            if response and 'id' in response:
                print('Видео с id "%s" успешно загружено.' % response['id'])
            elif response:
                exit('Загрузка завершилась неудачей с неожиданным ответом: %s' % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = 'Произошла восстанавливаемая ошибка HTTP %d:\n%s' % (e.resp.status, e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = 'Произошла восстанавливаемая ошибка: %s' % e
        if error:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit('Больше не пытаемся повторить.')
            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print('Ожидание %f секунд перед повторной попыткой...' % sleep_seconds)
            time.sleep(sleep_seconds)

if __name__ == '__main__':
    file = input('Введите файл видео для загрузки: ')
    title = input('Введите заголовок видео (по умолчанию "Test Title"): ') or 'Test Title'
    description = input('Введите описание видео (по умолчанию "Test Description"): ') or 'Test Description'
    category = input('Введите числовую категорию видео (по умолчанию "22"): ') or '22'
    keywords = input('Введите ключевые слова для видео, через запятую (по умолчанию пусто): ') or ''
    privacy_status = input('Введите статус конфиденциальности видео (public, private, unlisted; по умолчанию "private"): ') or 'private'

    args = argparse.Namespace(
        file=file,
        title=title,
        description=description,
        category=category,
        keywords=keywords,
        privacyStatus=privacy_status
    )

    youtube = get_authenticated_service()
    try:
        initialize_upload(youtube, args)
    except HttpError as e:
        print('Произошла ошибка HTTP %d:\n%s' % (e.resp.status, e.content))
