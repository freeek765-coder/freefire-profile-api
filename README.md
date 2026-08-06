# 🔥 Free Fire Advanced Profile & Utility API

एक पावरफुल और मॉडर्न Flask API जिसे Vercel पर डिप्लॉय किया गया है। यह API Free Fire प्रोफाइल्स को मैनेज करने, गैलरी आइटम्स अपडेट करने, और लाइक्स भेजने जैसे फीचर्स प्रदान करती है।

---

## 🚀 Endpoints & Usage Guide

### 1. Health Check
* **URL:** `/health`
* **Method:** `GET`
* **Description:** चेक करता है कि सर्वर लाइव है या नहीं।

### 2. Supported Regions
* **URL:** `/regions`
* **Method:** `GET`
* **Description:** गेम के सभी एक्टिव रीजन्स की लिस्ट दिखाता है।

### 3. Get Real Profile Details
* **URL:** `/profile?uid=YOUR_UID&region=IND`
* **Method:** `GET`
* **Description:** यूज़र का असली नाम, लेवल, और अकाउंट डिटेल्स JSON फॉर्मेट में देता है।

### 4. Add Gallery Items (Batch Supported)
* **URL:** `/add?jwt=YOUR_JWT_TOKEN&item_id=101,102`
* **Method:** `GET`
* **Description:** एक साथ कई आइटम्स को प्रोफाइल गैलरी में जोड़ता है।

### 5. Send Profile Likes
* **URL:** `/like?uid=YOUR_UID&region=IND`
* **Method:** `GET`
* **Description:** टारगेट UID पर डायरेक्ट लाइक्स भेजता है।

---
*Developed for high-speed automation and profile management.*
