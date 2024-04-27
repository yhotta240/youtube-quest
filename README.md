# Youtube Quest

このアプリは、YouTube Data API v3を使用して指定されたチャンネルの情報を取得するWebアプリケーションです。Flaskフレームワークを使用しています。

## プレビュー

<div align="center">
  <a href="https://youtube-quest.onrender.com/" target="_blank">
    <img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3680988/de85e431-b78d-f75e-a9f9-3edefd456a99.png" >
  </a>
</div>

[クリックしてページを開く](https://youtube-quest.onrender.com/)

注意: [Render.com](https://render.com/)の無料プランで公開しているため、開くまでに50秒以上かかる場合がありますので、ご了承ください。

### チュートリアル
1. [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/)のAPIキーを取得し、フォームにAPIキーを設定します。
2. [Youtube](https://www.youtube.com/)から調べたいチャンネルのチャンネルIDもしくはユーザーIDを取得し、フォームに貼り付けます。
3. 詳細設定で表示したい項目と検索を絞り込める検索詳細設定が可能です。
4. "Search" をクリックすると、該当チャンネルの情報と動画の情報を表示します。
5. 任意でCSV形式でのダウンロードが可能です。

<br>

## ローカルでの使用方法

### プロジェクトを作成
1. リポジトリをクローンします。
```bash
mkdir youtube-quest
cd youtube-quest
```

2. 仮想環境を作成します。
```bash
py -3 -m venv .venv
.venv\Scripts\activate
```

### インストール
1. 必要なライブラリをインストールします。
```bash
pip install Flask
pip install google-api-python-client
```

2. リポジトリをクローンします。
```bash
git clone https://github.com/yhotta240/youtube-quest.git
```

### 使用方法
1. `api/run.py` のファイルを開き、`from .route import app` を `from route import app` に変更します。
2. `api/route.py` のファイルを開き、`from .youtube_api ` を `from youtube_api` に、`from .download_csv` を `from download_csv` に変更します。
3. `python api/run.py` を実行してアプリケーションを起動します。

## 参考
https://developers.google.com/youtube/v3/docs?hl=ja
https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/
