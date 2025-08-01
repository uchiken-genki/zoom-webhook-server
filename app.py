from flask import Flask, request, jsonify

app = Flask(__name__)

latest_caller = {"number": None}

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Zoomの検証リクエストに対応
        challenge = request.args.get('challenge')
        if challenge:
            return jsonify({'challenge': challenge})
        else:
            return "OK", 200

    if request.method == 'POST':
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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
