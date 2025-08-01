from flask import Flask, request, jsonify

@app.route('/')
def index():
    return "✅ Zoom Webhook サーバーは正常に動作しています。"

app = Flask(__name__)
latest_caller = {"number": None}

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
