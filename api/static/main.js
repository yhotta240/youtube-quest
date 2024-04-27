// すべてのチェックボックスの状態を変更する関数
function toggleAllCheckboxes() {
  let displayAllCheckbox = document.getElementById('display_all');
  let otherCheckboxes = document.querySelectorAll('.form-check-input:not(#display_all)');

  for (let i = 0; i < otherCheckboxes.length; i++) {
    otherCheckboxes[i].checked = displayAllCheckbox.checked;
  }
}
// 「すべて」のチェックボックスの状態が変更されたときに呼び出される関数
document.getElementById('display_all').addEventListener('change', toggleAllCheckboxes);


// フォーム送信時の入力チェック関数
function validateForm() {
  const apiKey = document.getElementById('api_key').value;
  const channel = document.getElementById('channel').value;
  const searchType = document.getElementById('search_type').value;
  // APIキーが入力されているかどうかをチェック
  if (apiKey === '') {
    alert('APIキーを入力してください');
    return false; // フォームの送信を中止
  }

  // 検索タイプに応じてチャンネルの入力チェック
  if (searchType === 'channel_id' && channel === '') {
    alert('チャンネルIDを入力してください');
    return false; // フォームの送信を中止
  } else if (searchType === 'channel_name' && channel === '') {
    alert('チャンネル名を入力してください');
    return false; // フォームの送信を中止
  } else if (searchType === 'channel_url' && channel === '') {
    alert('チャンネルURLを入力してください');
    return false; // フォームの送信を中止
  } else if (searchType === 'user_id' && channel === '') {
    alert('ユーザーIDを入力してください');
    return false; // フォームの送信を中止
  }

  return true; // フォームの送信を続行
}

// フォーム送信ボタンがクリックされたときに入力チェックを実行
document.getElementById('dynamic-form').addEventListener('submit', function (event) {
  if (!validateForm()) {
    event.preventDefault(); // フォームの送信を中止
  }
});


// APIのクリアボタンをクリックしたときに、入力フォームをクリアする
document
  .getElementById("clear_api_key_Btn")
  .addEventListener("click", () => {
    document.getElementById("api_key").value = "";
  });
// チャンネルIDのクリアボタンをクリックしたときに、入力フォームをクリアする
document.getElementById("clearBtn").addEventListener("click", () => {
  document.getElementById("channel").value = "";
});

// リセットボタンがクリックされたときの処理
document.getElementById("resetBtn").addEventListener("click", () => {
  // 確認ダイアログを表示
  if (confirm("検索結果をリセットしますか？")) {
    // フォームの送信
    const videoList = document.getElementById("video-list");
    videoList.innerHTML = "";
  }
});

// ボタンをクリックしたときに実行される関数
document
  .getElementById("helpButton")
  .addEventListener("click", function () {
    // ポップオーバーの内容を設定
    const content =
      "APIキーは<a href='https://console.cloud.google.com/apis/credentials' target='_blank'>Google Cloud Platform</a>から取得してください。";

    // ポップオーバーを表示するための設定
    const popoverOptions = {
      content: content, // ポップオーバーの内容
      html: true, // HTMLを含むかどうか
      placement: "top", // ポップオーバーの表示位置
      trigger: "manual", // ポップオーバーを手動で表示する
    };

    // ポップオーバーを表示
    const popover = new bootstrap.Popover(this, popoverOptions);
    popover.show();

    // ドキュメント全体のクリックイベントを追加して、ポップオーバーが閉じるようにする
    document.addEventListener("click", function (e) {
      if (!document.getElementById("helpButton").contains(e.target)) {
        popover.hide(); // ポップオーバーを閉じる
      }
    });
  });