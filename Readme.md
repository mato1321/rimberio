# 🐾 RIMBERIO - Pet Matching Recommendation System

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=ffffff)
![FastAPI](https://img.shields.io/badge/FastAPI-0.124.2-009485?style=flat-square&logo=fastapi)
![LINE Bot](https://img.shields.io/badge/LINE-Bot%20SDK-00B900?style=flat-square&logo=line)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

**RIMBERIO** is an intelligent adoption advisor based on the LINE Chatbot. It integrates vector space algorithms and the ChromaDB vector database, using a “6-Dimensional Suitability Matching Model” to accurately recommend the most suitable pets for adopters, aiming to reduce post-adoption abandonment.

---

## Core Features

| Feature | Description |
|--------|-------------|
| **Recommendation Engine** | Vector Space Model (VSM) + ChromaDB vector similarity for accurate owner–pet matching |
| **LINE Real-time Interaction** | No app installation required; suitability assessment directly via LINE chat |
| **6-Dimensional Feature Analysis** | Activity, Affection, Independence, Space, Grooming, Noise |
| **Multi-turn Dialogue Flow** | Six contextual questions gradually build the user's preference vector |

---

## 6-Dimensional Feature Space Design

RIMBERIO defines “Owner–Pet Compatibility” as a 6-dimensional vector space, with each dimension ranging from **[0.0 ~ 1.0]**:

| Dimension ID | Feature Name | Description | Low Value (0.0) | High Value (1.0) |
|--------------|--------------|-------------|------------------|------------------|
| **0** | Activity | Activity level | Homebody | Very active |
| **1** | Affection | Affection level | Lone wolf | Clingy |
| **2** | Independence | Independence | Home often | Frequently away |
| **3** | Space | Space requirements | Small studio | Large yard |
| **4** | Grooming | Shedding level | Almost no shedding | Heavy shedding |
| **5** | Noise | Noise level | Very quiet | Very noisy |

### Example Pet Feature Vectors

| Pet Name | Activity | Affection | Independence | Space | Grooming | Noise | Suitable For |
|---------|----------|-----------|--------------|--------|-----------|--------|--------------|
| Border Collie | 1.0 | 0.6 | 0.3 | 0.9 | 0.8 | 0.7 | Active outdoor lovers |
| British Shorthair | 0.2 | 0.3 | 0.9 | 0.2 | 0.5 | 0.1 | Busy office workers |
| Beagle | 0.9 | 0.9 | 0.3 | 0.6 | 0.4 | 1.0 | Young, playful owners |
| Siamese Cat | 0.6 | 1.0 | 0.1 | 0.2 | 0.3 | 0.9 | Companion seekers |
| Shiba Inu | 0.7 | 0.4 | 0.9 | 0.5 | 1.0 | 0.6 | Independent, patient owners |

---

## Questionnaire Design (6 Questions)

Q1【Activity】
Weekend arrives — what's your ideal plan?
✓ Hiking / Running / Exploring → value=0.9 (High activity)
✓ Park stroll / Shopping → value=0.5 (Moderate activity)
✓ Staying home relaxing → value=0.1 (Low activity)

Q2【Affection】
When relaxing at home, you prefer your pet to:
✓ Stick close to you → value=0.9 (High affection)
✓ Interact occasionally → value=0.5 (Moderate affection)
✓ Do its own thing → value=0.2 (Low affection)

Q3【Independence】
How long are you usually away for work?
✓ Over 10 hours → value=0.9 (High independence needed)
✓ About 8 hours → value=0.5 (Moderate independence needed)
✓ Work from home → value=0.1 (Low independence needed)

Q4【Space】
Your living environment:
✓ House / Large yard → value=0.9 (Large space)
✓ Regular apartment → value=0.5 (Medium space)
✓ Studio / Shared room → value=0.1 (Small space)

Q5【Grooming】
Regarding pet hair at home:
✓ Cannot tolerate → value=0.1
✓ OK with frequent cleaning → value=0.5
✓ Hair is part of the decor → value=0.9

Q6【Noise】
About pet noises:
✓ Poor soundproofing / Sensitive → value=0.1 (Must be quiet)
✓ Residential area → value=0.5 (Moderate)
✓ Countryside / Detached home → value=0.9 (Can tolerate)


---

## Quick Start

### 1️⃣ Environment Requirements

```bash
python --version

2️⃣ Setup
git clone https://github.com/mato1321/rimberio.git
cd rimberio

python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

3️⃣ Setup LINE Messaging API

Follow the steps to:

Create Provider

Create Messaging API Channel

Retrieve Channel Secret + Access Token

Disable auto-replies

4️⃣ Environment Variables
LINE_CHANNEL_ACCESS_TOKEN=your_token
LINE_CHANNEL_SECRET=your_secret

5️⃣ Start Server
python -m uvicorn main:app --reload

6️⃣ Setup Ngrok
ngrok http 8000


Use the HTTPS forwarding URL.

7️⃣ Configure Webhook
https://xxxx-xxxx.ngrok-free.app/callback

User Guide

Send:

開始

測驗

開始測驗

Then follow the 6 questions.

Technical Deep Dive
Vector Space Model (VSM)
distance = sqrt( Σ (user_i - pet_i)^2 )
match_score = max(0, (1 - distance) × 100%)

ChromaDB Benefits
Advantage	Description
High-speed	HNSW search
Scalable	Handles large pet dataset
Persistent	Saved to disk
Metadata	Stores pet descriptions
Dependencies
fastapi==0.124.2
uvicorn==0.38.0
line-bot-sdk==3.21.0
chromadb==1.3.6
onnxruntime==1.23.2
numpy==2.3.5
pandas==2.3.3
python-dotenv==1.2.1
pydantic==2.12.5
requests==2.32.5

Project Structure
rimberio/
├── .env.example
├── main.py
├── data_model.py
├── requirements.txt

Contact

Email: mato1321@example.com

GitHub: https://github.com/mato1321

Issues: https://github.com/mato1321/rimberio/issues

License

MIT License

Welcome to RIMBERIO — helping every furry companion find the perfect home!

      ᙏ̥ (๑•́  ω •̀๑)  
     ∧_∧
    ( ´・ω・)  
   /   ⊃⊂  \
  (´・ω・`)   


---