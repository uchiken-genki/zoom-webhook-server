from flask import Flask, request, jsonify
import hashlib
import hmac
import base64
import os

app = Flask(__name__)

# 環境変数からZoomのVerification Token（Webhook Secret Token）を取得
ZOOM_WEBHOOK_SECRET = os.environ.get("ZOOM_WEBHOOK_SECRET", "your_webhook_secret")

latest_caller = {"number": None}

@app.route('/webhook', methods=['POST'])
def webhook():
    # Zoomの検証リクエストかどうかを判定
    data = request.get_json()
    
    if "plainToken" in data:
        plain_token = data["plainToken"]
        
        # HMAC-SHA256署名を生成
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

    # 通常のWebhookイベント処理
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
