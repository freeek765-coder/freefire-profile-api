from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- 1. Health Check Endpoint ---
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "online",
        "game": "Free Fire",
        "version": "OB54",
        "message": "API System is running perfectly on Vercel"
    }), 200

# --- 2. Regions List Endpoint ---
@app.route('/regions', methods=['GET'])
def regions():
    supported_regions = [
        {"code": "IND", "name": "India", "status": "Active"},
        {"code": "US", "name": "United States", "status": "Active"},
        {"code": "BR", "name": "Brazil", "status": "Active"},
        {"code": "SG", "name": "Singapore", "status": "Active"}
    ]
    return jsonify({"success": True, "regions": supported_regions}), 200

# --- 3. Get Real Profile & Details Endpoint ---
@app.route('/profile', methods=['GET'])
def get_profile():
    uid = request.args.get('uid')
    region = request.args.get('region', 'IND')
    
    if not uid:
        return jsonify({"success": False, "error": "UID is required"}), 400
        
    # यहाँ आप असली गेम सर्वर या API का रिस्पॉन्स मैप कर सकते हैं
    real_profile_data = {
        "success": True,
        "account_info": {
            "uid": uid,
            "region": region,
            "nickname": "BHAIRAV",  # असली इन-गेम नाम
            "level": 2,              # सीजन लेवल
            "season": 0,
            "likes": 1540,
            "exp": 45000,
            "created_at": "2025-11-01"
        },
        "equipped_items": {
            "avatar": 1001,
            "banner": 2001,
            "pin": 3001
        }
    }
    return jsonify(real_profile_data), 200

# --- 4. Add / Update Gallery Items API (Advanced Batch Support) ---
@app.route('/add', methods=['GET'])
def add_items():
    jwt_token = request.args.get('jwt')
    item_ids = request.args.get('item_id', '') # कॉमा सेपरेटेड वैल्यू (जैसे: 101,102)
    
    if not jwt_token or not item_ids:
        return jsonify({
            "success": False, 
            "error": "Missing parameters! 'jwt' and 'item_id' are required."
        }), 400
    
    id_list = item_ids.split(',')
    results = []
    
    for item in id_list:
        # सिमुलेशन लॉजिक: आप यहाँ गेम सर्वर की रिक्वेस्ट डाल सकते हैं
        if item.isdigit():
            results.append({"item_id": item.strip(), "status": "SUCCESS", "message": "Item added to gallery"})
        else:
            results.append({"item_id": item.strip(), "status": "FAILED", "error": "BR_ACCOUNT_INVALID_GALLERY_ITEM"})
            
    return jsonify({
        "success": True,
        "message": "Batch process complete",
        "details": results
    }), 200

# --- 5. Free Fire Likes Sender API ---
@app.route('/like', methods=['GET'])
def send_likes():
    uid = request.args.get('uid')
    region = request.args.get('region', 'IND')
    
    if not uid:
        return jsonify({"success": False, "error": "UID is required to send likes"}), 400
        
    # यहाँ लाइक्स भेजने का ऑफिशियल लॉजिक या इंटीग्रेशन आएगा
    return jsonify({
        "success": True,
        "message": f"Successfully sent likes to UID: {uid}",
        "region": region,
        "status_code": 200
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
