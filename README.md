# Youtube Quest

このアプリは、YouTube Data API v3を使用して指定されたチャンネルの情報を取得するWebアプリケーションです。Flaskフレームワークを使用しています。

## プレビュー

<div align="center">
  <a href="https://youtube-quest.onrender.com/" target="_blank">
    <img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3680988/44c3ac08-c486-594e-5416-67c32f4261bd.png" >
  </a>
</div>

[クリックしてページを開く](https://youtube-quest.onrender.com/)

注意: [Render.com](https://render.com/)の無料プランで公開しているため、開くまでに50秒以上かかります。

### チュートリアル
1. [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/)のAPIキーを取得し、フォームにAPIキーを設定します。
2. [Youtube](https://www.youtube.com/)から調べたいチャンネルのチャンネルIDもしくはユーザーIDを取得し、フォームに貼り付けます。
3. 詳細設定で表示したい項目と検索を絞り込める検索詳細設定が可能です。
4. "Search" をクリックすると、該当チャンネルの情報と動画の情報を表示します。
5. 任意でCSV形式でのダウンロードが可能です。

<br>

## ローカルでの使用方法
https://github.com/yhotta240/youtube-quest

### プロジェクトを作成
1.リポジトリをクローンします。
```powershell:Windows
git clone https://github.com/yhotta240/youtube-quest.git
cd youtube-quest
code . 
```

2.仮想環境を作成します。
```powershell:Windows
py -3 -m venv .venv
.venv\Scripts\activate
```

### インストール
必要なライブラリをインストールします。

```powershell:Windows
pip install Flask
pip install google-api-python-client
```
もしくはrequirementsを使って一括インストール
```powershell:Windows
pip install -r requirements.txt
```
### 起動方法
1.`python fix_imports.py` を実行し、ローカル用のimportに修正します。
```powershell:Windows
python fix_imports.py
```
2.`python api/run.py` を実行してアプリケーションを起動します。
```powershell:Windows
python api/run.py
```
<br>


## 参考
https://developers.google.com/youtube/v3/docs?hl=ja<br>
https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/
