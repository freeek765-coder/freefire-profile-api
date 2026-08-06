import os
import hashlib
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

SUPPORTED_REGIONS = ["IND", "BR", "SG"]

def validate_uid(uid):
    return uid.isdigit() and 10 <= len(uid) <= 12

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/regions', methods=['GET'])
def regions():
    return jsonify({"regions": SUPPORTED_REGIONS}), 200

@app.route('/profile', methods=['GET'])
def profile():
    uid = request.args.get('uid')
    region = request.args.get('region')
    if not uid or not region:
        return jsonify({"error": "Missing uid or region"}), 400
    if not validate_uid(uid):
        return jsonify({"error": "Invalid UID"}), 400
    # Mock data
    return jsonify({
        "uid": uid,
        "region": region.upper(),
        "nickname": "TestPlayer",
        "level": 30,
        "season": 5,
        "likes": 123
    }), 200

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON"}), 400
    # ... rest
    return jsonify({"status": "success"}), 200

@app.route('/like', methods=['POST'])
def like():
    data = request.get_json()
    if not data or 'uid' not in data:
        return jsonify({"error": "Missing uid"}), 400
    uid = data['uid']
    if not validate_uid(uid):
        return jsonify({"error": "Invalid UID"}), 400
    # Mock response
    return jsonify({
        "success": True,
        "status": "Successfully Sent",
        "before_likes": 100,
        "after_likes": 101,
        "daily_limit": 50,
        "daily_used": 5,
        "remaining": 45
    }), 200

# Not needed for Vercel, but harmless
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
