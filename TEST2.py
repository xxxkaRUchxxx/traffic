from googleapiclient.discovery import build


def is_shorts_video(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(
        part='snippet,contentDetails',
        id=video_id
    )
    response = request.execute()

    if 'items' in response and response['items']:
        content_details = response['items'][0]['contentDetails']
        duration = content_details['duration']

        # Проверяем только длительность
        return duration <= 'PT1M'

    return False


def search_youtube_videos(api_key, query, max_results=5):
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=max_results,
        videoDuration='short'
    )

    response = request.execute()
    print(response)
    video_info = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_url = f'https://www.youtube.com/shorts/{video_id}'
        title = item['snippet']['title']
        description = item['snippet']['description']

        is_shorts = is_shorts_video(video_id, api_key)

        video_info.append({
            'url': video_url,
            'title': title,
            'description': description,
            'is_shorts': is_shorts
        })
    if video_info[0]['is_shorts'] == False:
        search_youtube_videos(api_key, query, max_results)
    return video_info


if __name__ == "__main__":
    api_key = 'AIzaSyA509jQ27WpVLqmO6oRgnsDbF8VsLS4iSA'
    query = 'товары с вб'
    max_results = 10

    videos = search_youtube_videos(api_key, query, max_results)

    for i, video in enumerate(videos, start=1):
        print(f"Video {i}:")
        print(f"  URL: {video['url']}")
        print(f"  Title: {video['title']}")
        print(f"  Description: {video['description']}")
        print(f"  Is Shorts: {video['is_shorts']}")
        print()

pohui = {'kind': 'youtube#searchListResponse',
         'etag': 'BCyB6hVZa-4GClWbqyehPGTAT24',
         'nextPageToken': 'CAEQAA',
         'regionCode': 'RU',
         'pageInfo': {'totalResults': 154242,
                      'resultsPerPage': 1},
         'items': [{'kind': 'youtube#searchResult',
                    'etag': 'aj7wyW0l08dWbAFUaieUdYBIsBc',
                    'id': {'kind': 'youtube#video',
                           'videoId': 'njl-HAVefzc'},
                    'snippet': {'publishedAt': '2023-06-11T16:44:36Z',
                                'channelId': 'UCjareCWWGUep0fZjlFSYEMg',
                                'title': 'Офигенные Товары С WILDBERRIES💜😈 #shortvideo #бьюти #wildberries #а4 #красота #shirts #обзор #asmr',
                                'description': 'shortvideo #бьюти #wildberries #красота #а4 #shirts #а4 #обзор #покупки #красотаиздоровье #распаковка #куроми #асмр ...',
                                'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/njl-HAVefzc/default.jpg',
                                                           'width': 120,
                                                           'height': 90},
                                               'medium': {'url': 'https://i.ytimg.com/vi/njl-HAVefzc/mqdefault.jpg',
                                                          'width': 320,
                                                          'height': 180},
                                               'high': {'url': 'https://i.ytimg.com/vi/njl-HAVefzc/hqdefault.jpg',
                                                        'width': 480,
                                                        'height': 360}},
                                'channelTitle': 'Demixova',
                                'liveBroadcastContent': 'none',
                                'publishTime': '2023-06-11T16:44:36Z'}}]}
