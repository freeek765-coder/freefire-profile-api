import os
import hashlib
import random
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for all routes

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
SUPPORTED_REGIONS = [
    "IND", "BR", "SG", "ID", "TH", "VN",
    "MY", "PK", "BD", "NG", "EG", "SA",
    "US", "UK", "RU"
]

# ---------------------------------------------------------------------
# Validation Helpers
# ---------------------------------------------------------------------
def validate_uid(uid: str) -> bool:
    """Ensure UID is numeric and between 10 and 12 digits."""
    return uid.isdigit() and 10 <= len(uid) <= 12

def validate_region(region: str) -> bool:
    """Check if region is supported."""
    return region.upper() in SUPPORTED_REGIONS

# ---------------------------------------------------------------------
# Mock Service Functions (replace with real API calls)
# ---------------------------------------------------------------------
def fetch_player_profile(uid: str, region: str) -> dict:
    """
    Simulate fetching player info from an external Free Fire API.
    In production, replace with requests to a real service.
    """
    # Deterministic mock data based on UID
    mock_names = ["PlayerOne", "ShadowBlade", "FireMaster", "SniperKing", "GhostRunner"]
    hash_val = int(hashlib.md5(uid.encode()).hexdigest(), 16)
    name_index = hash_val % len(mock_names)
    level = (hash_val % 50) + 10          # Level 10–59
    season = (hash_val % 15) + 1          # Season 1–15
    likes = (hash_val % 1000) + 100       # Likes count

    return {
        "uid": uid,
        "region": region.upper(),
        "nickname": mock_names[name_index],
        "level": level,
        "season": season,
        "likes": likes
    }

def process_gallery_items(jwt: str, item_ids: str) -> dict:
    """
    Simulate adding items to the gallery using a JWT token.
    Replace with actual authentication and gallery update logic.
    """
    if not jwt or len(jwt) < 10:
        raise ValueError("Invalid JWT – token too short")
    items = [item.strip() for item in item_ids.split(',') if item.strip()]
    if not items:
        raise ValueError("No valid item IDs provided")
    # Simulate successful processing
    return {"added_items": items, "count": len(items)}

def send_like(target_uid: str, region: str = None) -> dict:
    """
    Simulate sending a profile like.
    Replace with real Free Fire API call that returns before/after counts.
    """
    # Deterministic random for consistent mock behaviour per UID
    random.seed(target_uid)
    before_likes = random.randint(100, 5000)
    daily_limit = 50
    daily_used = random.randint(0, daily_limit)
    remaining = daily_limit - daily_used

    if daily_used >= daily_limit:
        status = "Daily Limit Reached"
        after_likes = before_likes
        success = False
    else:
        status = "Successfully Sent"
        after_likes = before_likes + 1
        success = True
        daily_used += 1   # update used count for this operation
        remaining -= 1

    return {
        "success": success,
        "status": status,
        "before_likes": before_likes,
        "after_likes": after_likes,
        "daily_limit": daily_limit,
        "daily_used": daily_used,
        "remaining": max(remaining, 0)
    }

# ---------------------------------------------------------------------
# Flask Endpoints
# ---------------------------------------------------------------------
@app.route('/health', methods=['GET'])
def health():
    """Server health check."""
    return jsonify({"status": "ok", "message": "Free Fire Profile API is running"}), 200

@app.route('/regions', methods=['GET'])
def regions():
    """List all supported regions."""
    return jsonify({"regions": SUPPORTED_REGIONS}), 200

@app.route('/profile', methods=['GET'])
def profile():
    """
    Fetch player profile.
    Query parameters: uid (required), region (required)
    """
    uid = request.args.get('uid')
    region = request.args.get('region')

    if not uid or not region:
        return jsonify({"error": "Missing uid or region parameters"}), 400
    if not validate_uid(uid):
        return jsonify({"error": "Invalid UID. Must be numeric and 10–12 digits."}), 400
    if not validate_region(region):
        return jsonify({"error": f"Unsupported region. Supported: {', '.join(SUPPORTED_REGIONS)}"}), 400

    try:
        player_info = fetch_player_profile(uid, region)
        return jsonify(player_info), 200
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/add', methods=['POST'])
def add_gallery_items():
    """
    Batch update gallery items.
    Expects JSON: { "jwt": "...", "item_ids": "id1,id2,id3" }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    jwt = data.get('jwt')
    item_ids = data.get('item_ids')
    if not jwt or not item_ids:
        return jsonify({"error": "Missing jwt or item_ids"}), 400

    try:
        result = process_gallery_items(jwt, item_ids)
        return jsonify({"status": "success", "data": result}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/like', methods=['POST'])
def like_profile():
    """
    Send a like to a target UID.
    Expects JSON: { "uid": "1234567890", "region": "IND" }  # region optional
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    target_uid = data.get('uid')
    region = data.get('region')   # optional
    if not target_uid:
        return jsonify({"error": "Missing target uid"}), 400
    if not validate_uid(target_uid):
        return jsonify({"error": "Invalid UID. Must be numeric and 10–12 digits."}), 400
    if region and not validate_region(region):
        return jsonify({"error": f"Unsupported region. Supported: {', '.join(SUPPORTED_REGIONS)}"}), 400

    try:
        result = send_like(target_uid, region)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# ---------------------------------------------------------------------
# Error Handlers
# ---------------------------------------------------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

# ---------------------------------------------------------------------
# Run the Application
# ---------------------------------------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
