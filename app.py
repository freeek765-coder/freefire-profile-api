from flask import Flask, request, jsonify
from flask_cors import CORS
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests
import time
import json
import base64
import sys

app = Flask(__name__)
CORS(app)

from google.protobuf import message_factory
from google.protobuf import descriptor_pool

pool = descriptor_pool.Default()
fd = pool.AddSerializedFile(b'\n\ndata.proto"7\n\x12InnerNestedMessage\x12\x0f\n\x07\x66ield_6\x18\x06 \x01(\x03\x12\x10\n\x08\x66ield_14\x18\x0e \x01(\x03"\x87\x01\n\nNestedItem\x12\x0f\n\x07\x66ield_1\x18\x01 \x01(\x05\x12\x0f\n\x07\x66ield_2\x18\x02 \x01(\x05\x12\x0f\n\x07\x66ield_3\x18\x03 \x01(\x05\x12\x0f\n\x07\x66ield_4\x18\x04 \x01(\x05\x12\x0f\n\x07\x66ield_5\x18\x05 \x01(\x05\x12$\n\x07\x66ield_6\x18\x06 \x01(\x0b\x32\x13.InnerNestedMessage"@\n\x0fNestedContainer\x12\x0f\n\x07\x66ield_1\x18\x01 \x01(\x05\x12\x1c\n\x07\x66ield_2\x18\x02 \x03(\x0b\x32\x0b.NestedItem"A\n\x0bMainMessage\x12\x0f\n\x07\x66ield_1\x18\x01 \x01(\x05\x12!\n\x07\x66ield_2\x18\x02 \x03(\x0b\x32\x10.NestedContainerb\x06proto3')

MainMessage = message_factory.GetMessageClass(pool.FindMessageTypeByName('MainMessage'))
NestedContainer = message_factory.GetMessageClass(pool.FindMessageTypeByName('NestedContainer'))
NestedItem = message_factory.GetMessageClass(pool.FindMessageTypeByName('NestedItem'))
InnerNestedMessage = message_factory.GetMessageClass(pool.FindMessageTypeByName('InnerNestedMessage'))

key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
freefire_version = "OB54"

def decode_jwt_noverify(token: str):
    try:
        parts = token.split(".")
        if len(parts) < 2:
            return None
        payload_b64 = parts[1] + "=" * (-len(parts[1]) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64).decode())
        return payload
    except Exception:
        return None

def get_server_url(lock_region: str):
    region = lock_region.upper()
    
    if region == "IND":
        return "https://client.ind.freefiremobile.com/SetPlayerGalleryShowInfo"
    elif region in ("BD", "PK", "SG", "ID", "ME", "VN", "TH", "TW", "EUROPE", "RU"):
        return "https://clientbp.ggpolarbear.com/SetPlayerGalleryShowInfo"
    elif region in ("BR", "US", "NA", "SAC"):
        return "https://client.us.freefiremobile.com/SetPlayerGalleryShowInfo"
    else:
        return "https://clientbp.ggpolarbear.com/SetPlayerGalleryShowInfo"

@app.route('/add', methods=['GET'])
def add_profile():
    missing_params = []
    if 'jwt' not in request.args:
        missing_params.append('jwt')
    if 'item_id' not in request.args:
        missing_params.append('item_id')
        
    if missing_params:
        return jsonify({
            "success": False,
            "message": f"The following parameters are entirely missing: {', '.join(missing_params)}",
            "method": "GET",
            "correct_usage": "/add?jwt={jwt_token}&item_id=ITEM_ID_1/ITEM_ID_2/ITEM_ID_3"
        }), 400

    jwt_token = request.args.get('jwt')
    itemid_str = request.args.get('item_id')
    
    empty_params = []
    if not jwt_token or jwt_token.strip() == "":
        empty_params.append('jwt')
    if not itemid_str or itemid_str.strip() == "":
        empty_params.append('item_id')

    if empty_params:
        return jsonify({
            "success": False,
            "message": f"You provided the parameters, but these values are empty: {', '.join(empty_params)}",
            "method": "GET",
            "correct_usage": "/add?jwt={jwt_token}&item_id=ITEM_ID_1/ITEM_ID_2/ITEM_ID_3"
        }), 400

    payload = decode_jwt_noverify(jwt_token)
    if not payload:
        return jsonify({
            "success": False,
            "message": "Invalid JWT token"
        }), 400

    lock_region = payload.get("lock_region", "IND").upper()
    url = get_server_url(lock_region)

    item_ids = itemid_str.split('/')[:15]
    if not item_ids:
        return jsonify({"success": False, "message": "At least one item ID required"}), 400

    data = MainMessage()
    data.field_1 = 1
    
    container1 = data.field_2.add()
    container1.field_1 = 1
    
    items = [
        {"field_1": 2, "field_4": 1},
        {"field_1": 2, "field_4": 1, "field_5": 4},
        {"field_1": 2, "field_4": 1, "field_5": 2},
        {"field_1": 13, "field_3": 1},
        {"field_1": 13, "field_3": 1, "field_4": 2},
        {"field_1": 13, "field_3": 1, "field_5": 2},
        {"field_1": 13, "field_3": 1, "field_5": 4},
        {"field_1": 13, "field_3": 1, "field_4": 2, "field_5": 2},
        {"field_1": 13, "field_3": 1, "field_4": 2, "field_5": 4},
        {"field_1": 13, "field_3": 1, "field_4": 4},
        {"field_1": 13, "field_3": 1, "field_4": 4, "field_5": 2},
        {"field_1": 13, "field_3": 1, "field_4": 4, "field_5": 4},
        {"field_1": 13, "field_3": 1, "field_4": 6},
        {"field_1": 13, "field_3": 1, "field_4": 6, "field_5": 2},
        {"field_1": 13, "field_3": 1, "field_4": 6, "field_5": 4}
    ]
    
    for i, item_id in enumerate(item_ids):
        if i >= len(items):
            break
        item_data = items[i]
        item = container1.field_2.add()
        item.field_1 = item_data.get("field_1", 0)
        if "field_3" in item_data:
            item.field_3 = item_data["field_3"]
        if "field_4" in item_data:
            item.field_4 = item_data["field_4"]
        if "field_5" in item_data:
            item.field_5 = item_data["field_5"]
        inner = InnerNestedMessage()
        inner.field_6 = int(item_id)
        item.field_6.CopyFrom(inner)

    container2 = data.field_2.add()
    container2.field_1 = 9
    
    item7 = container2.field_2.add()
    item7.field_4 = 3
    inner7 = InnerNestedMessage()
    inner7.field_14 = 3048205855
    item7.field_6.CopyFrom(inner7)
    
    item8 = container2.field_2.add()
    item8.field_4 = 3
    item8.field_5 = 3
    inner8 = InnerNestedMessage()
    inner8.field_14 = 3048205855
    item8.field_6.CopyFrom(inner8)

    data_bytes = data.SerializeToString()
    padded_data = pad(data_bytes, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(padded_data)

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": freefire_version,
        "Content-Type": "application/octet-stream",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
        "Accept-Encoding": "gzip"
    }

    try:
        response = requests.post(url, headers=headers, data=encrypted_data, timeout=10)
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"External request failed: {str(e)}"
        }), 500

    current_time = int(time.time())
    add_profile_list = [{"add_time": current_time, f"item_id{i+1}": int(item_id)} 
                        for i, item_id in enumerate(item_ids)]

    if response.status_code == 200:
        return jsonify({
            "message": "Item added to profile",
            "success": True,
            "lock_region": lock_region,
            "Add-items": add_profile_list,
            "response_code": response.status_code
        })
    else:
        return jsonify({
            "success": False,
            "message": f"External server returned status {response.status_code}",
            "lock_region": lock_region,
            "external_response": response.text,
            "request_size": len(encrypted_data),
            "response_code": response.status_code
        }), 400

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "version": "1.0",
        "freefire_version": freefire_version
    })

@app.route('/regions', methods=['GET'])
def get_regions():
    supported_regions = {
        "IND": "India",
        "BD": "Bangladesh",
        "PK": "Pakistan",
        "SG": "Singapore",
        "ID": "Indonesia",
        "ME": "Middle East",
        "VN": "Vietnam",
        "TH": "Thailand",
        "TW": "Taiwan",
        "EUROPE": "Europe",
        "RU": "Russia",
        "BR": "Brazil",
        "US": "United States",
        "NA": "North America",
        "SAC": "South America"
    }
    return jsonify({
        "supported_regions": supported_regions,
        "default_server": "https://clientbp.ggpolarbear.com/SetPlayerGalleryShowInfo"
    })

@app.route('/')
def home():
    return jsonify({
        "name": "Free Fire Profile API",
        "description": "API to add items to Free Fire profile",
        "version": "1.0",
        "endpoints": {
            "add_items": "/add-items?token={jwt}&itemid=ID1/ID2/...",
            "health": "/health",
            "regions": "/regions"
        },
        "supported_regions": {
            "IND": "India",
            "BD": "Bangladesh",
            "PK": "Pakistan",
            "SG": "Singapore",
            "ID": "Indonesia",
            "ME": "Middle East",
            "VN": "Vietnam",
            "TH": "Thailand",
            "TW": "Taiwan",
            "EUROPE": "Europe",
            "RU": "Russia",
            "BR": "Brazil",
            "US": "United States",
            "NA": "North America",
            "SAC": "South America"
        },
        "server_routing": {
            "IND": "https://client.ind.freefiremobile.com",
            "BD_PK_SG_ID_ME_VN_TH_TW_EUROPE_RU": "https://clientbp.ggpolarbear.com",
            "BR_US_NA_SAC": "https://client.us.freefiremobile.com",
            "default": "https://clientbp.ggpolarbear.com"
        }
    })

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(f"[🚀] Starting {__name__.upper()} on port {port} ...")
    app.run(host='0.0.0.0', port=port, debug=False)