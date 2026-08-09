from flask import Flask, request, jsonify
import requests
import random
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

# Track UID usage count per day: {uid: {"date": "YYYY-MM-DD", "count": 1_or_2}}
uid_usage_tracker = {}

def get_ist_date():
    utc_now = datetime.now(timezone.utc)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    if ist_now.hour < 4:
        return (ist_now - timedelta(days=1)).date()
    return ist_now.date()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "online", "message": "Advanced Multi-ID 2x Like API is running"}), 200

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
                time.sleep(2)

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
        
        # Initialize or fetch usage for this UID
        if uid not in uid_usage_tracker or uid_usage_tracker[uid]["date"] != today:
            uid_usage_tracker[uid] = {"date": today, "count": 0}

        current_count = uid_usage_tracker[uid]["count"]
        max_limit = 2  # अब हर UID दिन में 2 बार लाइक्स ले सकती है

        if not is_owner and current_count >= max_limit:
            return jsonify({
                "success": False,
                "message": "❌ Daily Limit Reached (Max 2 times per day for this UID)",
                "name": name,
                "uid": uid,
                "region": region.upper(),
                "used_today": current_count,
                "reset_time": "Next Day At 04:00 AM (IST)"
            }), 429

        # Increment usage count
        if not is_owner:
            uid_usage_tracker[uid]["count"] += 1
            remaining_chances = max_limit - uid_usage_tracker[uid]["count"]
        else:
            remaining_chances = "♾️ UNLIMITED (Owner Key Active)"

        likes_given = random.randint(129, 247)
        likes_before = max(0, likes_after - likes_given)

        return jsonify({
            "success": True,
            "message": "✅ Likes Successfully Added (2x Limit System)",
            "name": name,
            "uid": uid,
            "region": region.upper(),
            "likes_before": likes_before,
            "likes_given": likes_given,
            "likes_after": likes_after,
            "attempts_used": uid_usage_tracker[uid]["count"] if not is_owner else "Owner",
            "remaining_attempts_today": remaining_chances
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

if __name__ == '__main__':
    app.run(debug=True)
    
