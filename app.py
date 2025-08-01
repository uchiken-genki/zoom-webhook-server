from flask import Flask, request, jsonify
import os

app = Flask(__name__)

latest_caller = {"number": None}  # 最新の電話番号を保存する辞書

@app.route('/')
def index():
    return "✅ Zoom Webhook サーバーは正常に動作しています。"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
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

@app.route('/latest_number', methods=['GET'])
def get_latest_number():
    return jsonify({"number": latest_caller["number"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
