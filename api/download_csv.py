import csv
from io import StringIO

def convert_to_csv(videos, display_settings, csv_encode):
    # CSVデータを書き込むためのバッファ
    csv_buffer = StringIO()

    # 使用するフィールドのリストを作成
    fieldnames = []
    if display_settings["display_title"]:
        fieldnames.append("Title")
    if display_settings["display_youtube_url"]:
        fieldnames.append("Video URL")
    if display_settings["display_youtube_id"]:
        fieldnames.append("Video ID")
    if display_settings["display_description"]:
        fieldnames.append("Description")
    if display_settings["display_views_counts"]:
        fieldnames.append("Views")
    if display_settings["display_publishedAt"]:
        fieldnames.append("Published At")
    if display_settings["display_like_count"]:
        fieldnames.append("Likes")
    if display_settings["display_dislike_count"]:
        fieldnames.append("Dislikes")
    if display_settings["display_comment_count"]:
        fieldnames.append("Comments")
    if display_settings["display_tags"]:
        fieldnames.append("Tags")
    if display_settings["display_categoryId"]:
        fieldnames.append("Category ID")

    # CSVライターを初期化
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)

    # ヘッダーを書き込む
    writer.writeheader()

    # 動画データをCSVに書き込む
    for video in videos:
        row = {}
        if display_settings["display_title"]:
            row["Title"] = video.get("title", "")
        if display_settings["display_youtube_url"]:
            row["Video URL"] = f"https://www.youtube.com/watch?v={video['id']}"
        if display_settings["display_youtube_id"]:
            row["Video ID"] = video.get("id", "")
        if display_settings["display_description"]:
            row["Description"] = video.get("description", "")
        if display_settings["display_views_counts"]:
            row["Views"] = video.get("viewCount", "")
        if display_settings["display_publishedAt"]:
            row["Published At"] = video.get("publishedAt", "")
        if display_settings["display_like_count"]:
            row["Likes"] = video.get("likeCount", "")
        if display_settings["display_dislike_count"]:
            row["Dislikes"] = video.get("dislikeCount", "")
        if display_settings["display_comment_count"]:
            row["Comments"] = video.get("commentCount", "")
        if display_settings["display_tags"]:
            row["Tags"] = ", ".join(video.get("tags", []))
        if display_settings["display_categoryId"]:
            row["Category ID"] = video.get("categoryId", "")
        # CSV に行を書き込む
        writer.writerow(row)

     # バッファからCSVデータを取得して返す
    try:
        csv_data = csv_buffer.getvalue().encode(csv_encode)
    except UnicodeEncodeError:
        # エンコードエラーが発生した場合、バッファのエンコードエラーを無視する
        csv_buffer.seek(0)
        csv_data = csv_buffer.read().encode(errors='ignore')

    return csv_data