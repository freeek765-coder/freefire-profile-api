# 🚀 Free Fire Profile API

## 📋 Project Overview
A robust Python-based API designed for Free Fire profile management. This project enables seamless interaction with game services, allowing for profile customization and item updates via a clean API interface.

---

## 🛠️ Tech Stack
* **Language:** Python
* **Framework:** Flask
* **Deployment:** Vercel
* **Dependencies:** `flask`, `flask-cors`, `pycryptodome`, `requests`, `protobuf`

---

## ⚙️ Features
- **Region Management:** Supports multiple global regions.
- **Profile Updates:** Securely add items to the profile.
- **Status Monitoring:** Real-time health check endpoint.
- **Security:** AES-CBC encryption for secure data transmission.

---

## 🚀 Deployment Guide
1. **Repository Setup:**
   - Initialize a new GitHub repository.
   - Upload `app.py`, `requirements.txt`, and `vercel.json`.
2. **Vercel Connection:**
   - Link your GitHub repository to [Vercel](https://vercel.com).
   - Configure the root directory settings.
   - Deploy!

---

## 🔗 API Endpoints
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/add` | `GET` | Add items to profile |
| `/health` | `GET` | Service status check |
| `/regions` | `GET` | List supported regions |

---
*Developed for optimal performance on mobile devices.*
