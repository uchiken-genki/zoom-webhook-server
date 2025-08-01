from flask import Flask, request, jsonify
import hashlib
import hmac
import base64
import os

@app.before_request
def log_request_info():
    print("📥 Headers:", request.headers)
    print("📥 Body:", request.get_data())

app = Flask(__name__)

ZOOM_WEBHOOK_SECRET = os.environ.get("ZOOM_WEBHOOK_SECRET", "your_webhook_secret")

latest_caller = {"number": None}

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        # Zoom の GET リクエスト確認用
        return jsonify({'message': 'Webhook endpoint is active'}), 200

    data = request.get_json()

    # Zoom の URL 検証用の plainToken 処理
    if data and "plainToken" in data:
        plain_token = data["plainToken"]
        hash_for_zoom = hmac.new(
            ZOOM_WEBHOOK_SECRET.encode(),
            msg=plain_token.encode(),
            digestmod=hashlib.sha256
        ).digest()

        encrypted_token = base64.b64encode(hash_for_zoom).decode()

        # ✅ Zoom が期待する形式で返す
        return jsonify({
            "plainToken": plain_token,
            "encryptedToken": encrypted_token
        }), 200

    # Webhook イベント処理
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
