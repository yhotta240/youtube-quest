from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def youtube_api(api_key):
    if api_key:
        youtube = build("youtube", "v3", developerKey=api_key)
        return youtube
    else:
        
        raise ValueError("APIキーが見つかりません")


def get_channel_search(
    youtube, channel_id=None, channel_name=None, channel_url=None, user_id=None
):
    if channel_id:
        return _get_channel_info(youtube, channel_id)
    if channel_name:
        channel_id = _get_channel_id_by_name(youtube, channel_name)
        return _get_channel_info(youtube, channel_id) if channel_id else {}
    # チャンネルURLからチャンネルIDを取得する処理を追加する
    if channel_url:
        pass
    if user_id:
        channel_id = _get_channel_id_by_user_id(youtube, user_id)
        return _get_channel_info(youtube, channel_id) if channel_id else {}
    return {}


def _get_channel_id_by_name(youtube, channel_name):
    request = youtube.channels().list(part="id", forUsername=channel_name)
    response = request.execute()
    if "items" in response and response["items"]:
        return response["items"][0]["id"]
    return None


def _get_channel_id_by_user_id(youtube, user_id):
    request = youtube.channels().list(part="id", forHandle=user_id)
    response = request.execute()
    if "items" in response and response["items"]:
        return response["items"][0]["id"]
    return None


def _get_channel_info(youtube, channel_id):
    channel_data = {}
    request = youtube.channels().list(part="snippet,statistics", id=channel_id)
    response = request.execute()
    print("チャンネル情報")
    print(response)
    if "items" in response and response["items"]:
        channel = response["items"][0]
        channel_data["channel_icon"] = channel["snippet"]["thumbnails"]["default"][
            "url"
        ]
        channel_data["channel_id"] = channel["id"]
        channel_data.update(channel["snippet"])
        channel_data.update(channel["statistics"])
    return channel_data


def get_channel_info(
    youtube,
    channel_id,
    videos_count,
    order,
    content_type,
    category_id,
    min_duration,
    max_duration,
    min_views,
    max_views,
):

    videos = []

    try:
        # チャンネルから最新の動画を取得
        request = (
            youtube.search()
            .list(
                part="snippet",  # snippetとstatisticsの両方を取得する
                channelId=channel_id,
                maxResults=videos_count,
                type=content_type,
                videoCategoryId=category_id,
                order=order,
                # publishedAfter=min_duration,
                # publishedBefore=max_duration,
            )
            .execute()
        )
        print("チャンネルの動画")
        print(request)
        # 取得した動画のURLをリストに追加
        for item in request["items"]:
            # print(item)
            if item["id"]["kind"] == "youtube#video":
                video_info = {}
                video_info["title"] = item["snippet"]["title"]
                video_info["id"] = item["id"]["videoId"]
                video_info["description"] = item["snippet"]["description"]
                video_info["publishedAt"] = item["snippet"]["publishedAt"]

                # 動画の詳細な情報を取得
                video_details_request = (
                    youtube.videos()
                    .list(
                        part="statistics, snippet",
                        id=video_info["id"],
                    )
                    .execute()
                )
                print("video_details_request")
                print(video_details_request)
                # 応答から動画の詳細な情報を取り出し、video_info に結合
                if "items" in video_details_request:
                    if 'tags' in video_details_request["items"][0]["snippet"]:
                        tags = video_details_request["items"][0]['snippet']['tags']
                        print(tags)
                        video_info['tags'] = tags
                    else:
                        print("Tags not found")
                    if 'categoryId' in video_details_request["items"][0]["snippet"]:
                        categoryId = video_details_request["items"][0]["snippet"]["categoryId"]
                        print(categoryId)
                        video_info['categoryId'] = categoryId
                    else:
                        print("categoryId not found")
                    video_statistics = video_details_request["items"][0]["statistics"]
                    video_info.update(video_statistics)
                videos.append(video_info)
                print("結果")
                print(videos)

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")

    return videos



