from flask import Flask, request, jsonify
import hashlib
import hmac
import base64
import os

app = Flask(__name__)

# 環境変数から Zoom の Webhook Secret Token を取得
ZOOM_WEBHOOK_SECRET = os.environ.get("ZOOM_WEBHOOK_SECRET", "your_webhook_secret")

# 最新の発信者番号を保持
latest_caller = {"number": None}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    # Zoom の URL 検証ステップ
    if "plainToken" in data:
        plain_token = data["plainToken"]
        # HMAC-SHA256 を使って encryptedToken を生成
        hash_for_zoom = hmac.new(
            ZOOM_WEBHOOK_SECRET.encode(),
            msg=plain_token.encode(),
            digestmod=hashlib.sha256
        ).digest()
        encrypted_token = base64.b64encode(hash_for_zoom).decode()

        return jsonify({
            "plainToken": plain_token,
            "encryptedToken": encrypted_token
        })

    # Zoom Phone のイベント処理
    try:
        event_type = data.get('event')
        if event_type == "phone.callee_ringing":
            caller_id = data['payload']['object']['caller']['id']
            print(f"📞 Ringing from: {caller_id}")
            latest_caller["number"] = caller_id
        return jsonify({"status": "received"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error"}), 500

# テスト用の GET エンドポイント（任意）
@app.route("/webhook", methods=["GET"])
def webhook_get():
    return jsonify({"message": "Webhook endpoint is active"}), 200

# サーバー起動
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
