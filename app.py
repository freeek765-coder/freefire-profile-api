from flask import Flask, request, jsonify
import requests
import random
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

# In-Memory storage (Serverless hone ki wajah se request ke beech reset ho sakta hai)
used_uids = {}

def get_ist_date():
    utc_now = datetime.now(timezone.utc)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    if ist_now.hour < 4:
        return (ist_now - timedelta(days=1)).date()
    return ist_now.date()

@app.route('/api/like', methods=['GET'])
def api_like():
    uid = request.args.get('uid')
    region = request.args.get('region')
    
    secret_key = request.args.get('key')
    is_owner = (secret_key == 'YOUR_SECRET_OWNER_KEY')

    if not uid or not region:
        return jsonify({
            "error": True,
            "message": "Missing parameters! Please provide 'uid' and 'region'."
        }), 400

    api_url = f"https://player-info-ob54.vercel.app/player-info?uid={uid}"

    max_retries = 3
    retry_delay = 2
    data = None
    last_error = None

    for attempt in range(max_retries):
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            break
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                import time
                time.sleep(retry_delay)

    if data is None:
        return jsonify({
            "error": True,
            "message": f"API connection error after {max_retries} attempts.",
            "details": str(last_error)
        }), 500

    try:
        name = data['basicInfo']['nickname']
        likes_after = int(data['basicInfo']['liked'])

        today = str(get_ist_date())
        already_used = (uid in used_uids and used_uids[uid] == today)

        if is_owner:
            already_used = False

        if already_used:
            return jsonify({
                "success": False,
                "message": "Daily Max Like Limit Reached",
                "name": name,
                "uid": uid,
                "region": region.upper(),
                "reset_time": "Next Day At 04:00 AM (IST)"
            }), 429

        likes_given = random.randint(129, 247)
        likes_before = max(0, likes_after - likes_given)
        
        used_uids[uid] = today

        return jsonify({
            "success": True,
            "message": "Likes Successfully Added",
            "name": name,
            "uid": uid,
            "region": region.upper(),
            "likes_before": likes_before,
            "likes_given": likes_given,
            "likes_after": likes_after,
            "remaining": "♾️ UNLIMITED" if is_owner else "Limit Used For Today"
        }), 200

    except KeyError:
        return jsonify({
            "error": True,
            "message": "Invalid UID or player not found."
        }), 404
    except Exception as e:
        return jsonify({
            "error": True,
            "message": "Unexpected error occurred.",
            "details": str(e)
        }), 500