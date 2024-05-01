import os
import copy
from flask import Flask, render_template, request, Response, session
from youtube_api import youtube_api, get_channel_search, get_channel_info
from download_csv import convert_to_csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# デフォルトの表示設定
DEFAULT_DISPLAY_SETTINGS = {
    "display_title": True,
    "display_youtube_url": True,
    "display_youtube_id": True,
    "display_description": False,
    "display_views_counts": True,
    "display_publishedAt": True,
    "display_like_count": True,
    "display_dislike_count": False,
    "display_comment_count": True,
    "display_tags": False,
    "display_categoryId": False,
}


def normalize_date(date_string):
    date_string_without_tz = date_string.replace("Z", "")
    date_string_without_ms = date_string_without_tz.split(".")[0]
    dt_object = datetime.strptime(date_string_without_ms, "%Y-%m-%dT%H:%M:%S")
    return dt_object.strftime("%Y/%m/%d %H:%M:%S")


@app.route("/", methods=["GET", "POST"])
def search():
    # フォームから取得したデータの初期化
    videos = []
    channel_data = {}
    channel_id = ""
    # 表示設定のデフォルト値を設定
    display_settings = DEFAULT_DISPLAY_SETTINGS.copy()
    search_type = None

    if request.method == "POST":
        # 検索条件の取得
        api_key = request.form.get("api_key")
        session["api_key"] = api_key
        youtube = youtube_api(api_key)
        search_type = request.form.get("search_type")
        channel = request.form.get("channel")

        # 検索タイプに応じて条件を設定
        channel_data = get_channel_search(
            youtube,
            channel if search_type == "channel_id" else None,
            channel if search_type == "channel_name" else None,
            channel if search_type == "channel_url" else None,
            channel if search_type == "user_id" else None,
        )
        channel_id = channel_data.get("channel_id")

        channel_data_copy = copy.deepcopy(channel_data)
        session["channel_data"] = channel_data_copy
        
        if "publishedAt" in channel_data:
            channel_data["publishedAt"] = normalize_date(channel_data["publishedAt"])

        if not api_key:
            return render_template("search.html")
        if not channel_id:
            return render_template("search.html")

        # 表示設定のデフォルト値を設定
        display_settings = {
            key: bool(request.form.get(key, DEFAULT_DISPLAY_SETTINGS[key]))
            for key in DEFAULT_DISPLAY_SETTINGS
        }
        # 表示設定は既に取得済み
        session["display_settings"] = display_settings

        # 詳細設定の取得
        maxResults = int(request.form.get("maxResults"))
        order = request.form.get("order")
        content_type = request.form.get("content_type")
        category_id = request.form.get("category_id")
        if "all" in category_id:
            category_id = None
        min_duration = request.form.get("min_duration")
        max_duration = request.form.get("max_duration")
        min_views = request.form.get("min_views")
        max_views = request.form.get("max_views")
        csv_encode = request.form.get("encode")
        session["csv_encode"] = csv_encode
        
        # 検索条件をセッションに保存
        session["search_conditions"] = {
            "channel_id": channel_id,
            "maxResults": maxResults,
            "order": order,
            "content_type": content_type,
            "category_id": category_id,
            "min_duration": min_duration,
            "max_duration": max_duration,
            "min_views": min_views,
            "max_views": max_views,
        }

        # 動画情報の取得
        videos = get_channel_info(
            youtube,
            channel_id,
            maxResults,
            order,
            content_type,
            category_id,
            min_duration,
            max_duration,
            min_views,
            max_views,
        )

        for video in videos:
            video["publishedAt"] = normalize_date(video["publishedAt"])

    return render_template(
        "search.html",
        videos=videos,
        channel_data=channel_data,
        search_type=search_type,
        **display_settings,
    )


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/download_csv", methods=["POST"])
def download_csv():
    # 検索結果を取得
    api_key = session.get("api_key")
    display_settings = session.get("display_settings", DEFAULT_DISPLAY_SETTINGS)
    channel_data = session.get("channel_data")
    # 検索条件を取得
    search_conditions = session.get("search_conditions")
    # videos = session.get("videos")
    youtube = youtube_api(api_key)
    # 動画情報の取得
    videos = get_channel_info(
        youtube,
        search_conditions.get("channel_id"),
        search_conditions.get("maxResults"),
        search_conditions.get("order"),
        search_conditions.get("content_type"),
        search_conditions.get("category_id"),
        search_conditions.get("min_duration"),
        search_conditions.get("max_duration"),
        search_conditions.get("min_views"),
        search_conditions.get("max_views"),
    )

    csv_filename = search_conditions.get("channel_id")
    csv_encode = session.get("csv_encode")
    # 動画情報を修正
    if videos is not None:
        for video in videos:
            if isinstance(video, dict) and "title" in video:
                video["title"] = video["title"].replace("\u25bb", "")
            if isinstance(video, dict) and "description" in video:
                video["description"] = video["description"].replace("\u25bb", "")

    # CSVに変換
    csv_data = convert_to_csv(videos, display_settings, csv_encode)

    # CSVデータをファイルとしてダウンロードさせる
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={csv_filename}.csv"},
    )
