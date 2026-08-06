# 🎯 Free Fire Profile & Utility API

> A blazing-fast Flask backend for fetching Free Fire player profiles, managing gallery items, and sending profile likes — ready for serverless deployment on Vercel.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.2.2-green?logo=flask)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-black?logo=vercel)

---

## 📖 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🔧 Installation](#-installation)
- [🌐 API Endpoints](#-api-endpoints)
- [📦 Deployment on Vercel](#-deployment-on-vercel)
- [🛠️ Tech Stack](#️-tech-stack)
- [📄 License](#-license)

---

## ✨ Features

- ✅ **Health Check** – `/health` endpoint for monitoring.
- 🌍 **Supported Regions** – Get list of all available game regions (`IND`, `BR`, `SG`, etc.).
- 👤 **Player Profile** – Fetch accurate UID, nickname, level, season, and likes.
- 🖼️ **Batch Gallery Updater** – Add multiple items using JWT authentication (`/add`).
- ❤️ **Profile Likes** – Send likes to a target UID with before/after counts and daily limit tracking.
- ⚡ **Optimized for Vercel** – Lightweight, scalable, and production-ready.
- 🧹 **Clean Error Handling** – JSON responses with proper HTTP status codes.

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/freefire-profile-api.git
cd freefire-profile-api

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
