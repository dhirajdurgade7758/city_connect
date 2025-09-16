# 🌍 CityConnect

**AI-Powered Civic Engagement & EcoCoin Rewards**

**🏆 MIT IEE 24-Hour National Level Hackathon Project**

CityConnect is an AI-powered civic-tech + gamification platform that empowers citizens to report civic issues, complete eco-friendly tasks, and earn rewards. The system integrates AI verification, live location tracking, EcoCoin gamification, and departmental admin panels to create a smart city management ecosystem.

---

## 🎯 Problem Statement

Citizens often face difficulties in reporting civic issues, and governments struggle with verification, accountability, and public engagement. Additionally, there is a lack of motivation for citizens to actively participate in eco-friendly initiatives.

CityConnect solves this by:

* Using AI to verify issues & eco tasks.
* Providing gamified incentives (EcoCoins, badges, leaderboard).
* Building a transparent reward system where users can redeem offers.
* Giving departments real-time dashboards to track and resolve issues.

---

## 🚀 Solution Overview

CityConnect brings together reporting, verification, gamification, and redemption into a seamless experience. Citizens can report problems with images and live location; AI verifies authenticity; EcoCoins are awarded and can be spent at the EcoCoin Store. Departments receive actionable dashboards to prioritize and resolve issues.

---

## ✨ Features

### 👤 User Features

* **Profile Dashboard**: Track reports, tasks, EcoCoins, badges, and redemptions.
* **Issue Reporting Feed**:

  * Submit issues with image, description, and live location.
  * AI verifies submissions for authenticity.
  * Social actions: Like ❤️, Comment 💬, Save 📌, Share 🔗.
* **Eco Tasks**:

  * Complete eco-friendly tasks (waste management, plantation, etc.).
  * AI validates task submissions and awards EcoCoins.
* **Gamification**:

  * Earn EcoCoins for reporting, tasks, likes, comments.
  * Unlock badges and climb the leaderboard.
* **EcoCoin Store**:

  * Redeem offers across Shop Offers, Donor Gifts, Event Tickets, and Eco Rewards.
  * Generate downloadable voucher PDF for physical claim.
* **Saved Posts**: HTMX-powered save/unsave UI for fast interactions.

---

### 🏛 Department Admin Panels

Departments have tailored admin panels to manage issues:

* Electricity Department
* Waste Management Department
* Water Supply Department
* Public Works Department

Each panel supports:

* Viewing assigned issues with live map locations.
* Updating issue status (Pending → In Progress → Resolved).
* Monitoring resolution history and analytics.

---

### 🎮 Gamification System

**EcoCoins**

* Earned via tasks, issue reporting, likes, and comments.
* Spent in the EcoCoin Store.

**Badges**

* 🐣 First Post
* 🌱 Green Starter (50 EcoCoins)
* 🌿 Eco Warrior (100 EcoCoins)
* 🌳 Eco Champion (200 EcoCoins)
* 🪐 Planet Protector (500 EcoCoins)

**Leaderboard**

* Ranks contributors by EcoCoins and engagement.

---

### 🛒 EcoCoin Store

**Categories**:

* 🛍 Shop Offers – Discounts from local businesses.
* 🎁 Donor Gifts – Items donated by citizens.
* 🎟 Event Tickets – Concerts, workshops, city events.
* 🌱 Eco Rewards – Plants, bottles, eco-bags.

**Redemption Flow**:

1. User redeems an offer.
2. EcoCoins deducted and stock decremented.
3. Unique voucher code generated.
4. User downloads/prints a PDF receipt and claims it physically.

---

## ⚙️ Tech Stack

**Backend**

* Django 5.x
* PostgreSQL (production) / SQLite (local)
* OpenAI API (image + text verification)
* HTMX for interactive UI updates

**Frontend**

* Django Templates
* Bootstrap 5 + Bootstrap Icons / FontAwesome
* JavaScript + AJAX + HTMX

**Other Integrations**

* PDF voucher generation
* Live location fetch (browser Geolocation)
* AI-based coin allocation and verification

---

## 📂 Project Structure

```
cityconnect/
├── cityconnect/         # Main project settings
├── core/                # User profiles, dashboard, feed, auth
├── issues/              # Issue reporting & AI verification & tasks
├── store/               # EcoCoin store, redemptions
├── admin_panel/         # Department dashboards
├── templates/           # HTML templates
├── static/              # CSS, JS, assets
```

---

## 📊 System Workflow

1. **User Action** → Report issue or complete task.
2. **AI Verification** → Matches image + description + department.
3. **EcoCoins Awarded** → Coins credited based on authenticity & engagement.
4. **Department Panel** → Department views and updates issue status.
5. **Store Redemption** → User redeems offer, voucher is generated.
6. **Physical Claim** → User shows voucher to merchant to claim reward.

---

## 🛠 Setup & Deployment (Quick Start)

> These steps assume you have Python 3.11+, pip, and git installed.

1. **Clone project**

```bash
git clone https://github.com/dhirajdurgade7758/city_connect.git
cd city_connect
```

2. **Create virtual environment & install deps**

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate     # Windows PowerShell
pip install -r requirements.txt
```

3. **Create `.env` and set environment variables** (example):

```
DJANGO_SECRET_KEY="your_secret"
DEBUG=False
DATABASE_URL=postgres://user:pass@host:port/dbname
GEMINI_API_KEY=xxxxx
HF_API_KEY=xxxxx
GOOGLE_MAPS_API_KEY=xxxxx
EMAIL_HOST=smtp...
EMAIL_PORT=587
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
```

4. **Migrate & collect static**

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

5. **Create a superuser**

```bash
python manage.py createsuperuser
```

6. **Deploy to Render / Railway**

* Add `Procfile`: `web: gunicorn cityconnect.wsgi`
* Ensure `requirements.txt` includes `gunicorn`, `whitenoise`, `dj-database-url`, `psycopg2-binary`.
* Set environment variables in platform dashboard.
* Trigger deploy and run migrations.

---

## 🔮 Future Enhancements

* Mobile App (Flutter / React Native)
* Push notifications for verification, rewards, and badges
* Advanced AI fake report detection and anomaly detection
* Shopkeeper / Donor self-service panel
* City Analytics Dashboard with heatmaps & KPIs

---

## 👨‍💻 Team & Credits

Developed as part of the **MIT IEE 24-Hour National Level Hackathon**.

**Team Goal**: Create a scalable Smart City + AI-powered Gamification Platform that makes civic engagement transparent, rewarding, and impactful.

---

## 🏁 Conclusion

CityConnect is more than a hackathon project — it’s a blueprint for smarter, greener, and more engaged cities. By combining AI verification with gamified incentives, CityConnect makes civic participation meaningful and rewarding.

---

## 📬 Contact

For questions or collaboration, contact the team via the project GitHub repository.

---

*Made with ❤️ for civic good.*
# 🌍 CityConnect

**AI-Powered Civic Engagement & EcoCoin Rewards**

**🏆 MIT IEE 24-Hour National Level Hackathon Project**

CityConnect is an AI-powered civic-tech + gamification platform that empowers citizens to report civic issues, complete eco-friendly tasks, and earn rewards. The system integrates AI verification, live location tracking, EcoCoin gamification, and departmental admin panels to create a smart city management ecosystem.

---

## 🎯 Problem Statement

Citizens often face difficulties in reporting civic issues, and governments struggle with verification, accountability, and public engagement. Additionally, there is a lack of motivation for citizens to actively participate in eco-friendly initiatives.

CityConnect solves this by:

* Using AI to verify issues & eco tasks.
* Providing gamified incentives (EcoCoins, badges, leaderboard).
* Building a transparent reward system where users can redeem offers.
* Giving departments real-time dashboards to track and resolve issues.

---

## 🚀 Solution Overview

CityConnect brings together reporting, verification, gamification, and redemption into a seamless experience. Citizens can report problems with images and live location; AI verifies authenticity; EcoCoins are awarded and can be spent at the EcoCoin Store. Departments receive actionable dashboards to prioritize and resolve issues.

---

## ✨ Features

### 👤 User Features

* **Profile Dashboard**: Track reports, tasks, EcoCoins, badges, and redemptions.
* **Issue Reporting Feed**:

  * Submit issues with image, description, and live location.
  * AI verifies submissions for authenticity.
  * Social actions: Like ❤️, Comment 💬, Save 📌, Share 🔗.
* **Eco Tasks**:

  * Complete eco-friendly tasks (waste management, plantation, etc.).
  * AI validates task submissions and awards EcoCoins.
* **Gamification**:

  * Earn EcoCoins for reporting, tasks, likes, comments.
  * Unlock badges and climb the leaderboard.
* **EcoCoin Store**:

  * Redeem offers across Shop Offers, Donor Gifts, Event Tickets, and Eco Rewards.
  * Generate downloadable voucher PDF for physical claim.
* **Saved Posts**: HTMX-powered save/unsave UI for fast interactions.

---

### 🏛 Department Admin Panels

Departments have tailored admin panels to manage issues:

* Electricity Department
* Waste Management Department
* Water Supply Department
* Public Works Department

Each panel supports:

* Viewing assigned issues with live map locations.
* Updating issue status (Pending → In Progress → Resolved).
* Monitoring resolution history and analytics.

---

### 🎮 Gamification System

**EcoCoins**

* Earned via tasks, issue reporting, likes, and comments.
* Spent in the EcoCoin Store.

**Badges**

* 🐣 First Post
* 🌱 Green Starter (50 EcoCoins)
* 🌿 Eco Warrior (100 EcoCoins)
* 🌳 Eco Champion (200 EcoCoins)
* 🪐 Planet Protector (500 EcoCoins)

**Leaderboard**

* Ranks contributors by EcoCoins and engagement.

---

### 🛒 EcoCoin Store

**Categories**:

* 🛍 Shop Offers – Discounts from local businesses.
* 🎁 Donor Gifts – Items donated by citizens.
* 🎟 Event Tickets – Concerts, workshops, city events.
* 🌱 Eco Rewards – Plants, bottles, eco-bags.

**Redemption Flow**:

1. User redeems an offer.
2. EcoCoins deducted and stock decremented.
3. Unique voucher code generated.
4. User downloads/prints a PDF receipt and claims it physically.

---

## ⚙️ Tech Stack

**Backend**

* Django 5.x
* PostgreSQL (production) / SQLite (local)
* OpenAI API (image + text verification)
* HTMX for interactive UI updates

**Frontend**

* Django Templates
* Bootstrap 5 + Bootstrap Icons / FontAwesome
* JavaScript + AJAX + HTMX

**Other Integrations**

* PDF voucher generation
* Live location fetch (browser Geolocation)
* AI-based coin allocation and verification

---

## 📂 Project Structure

```
cityconnect/
├── cityconnect/         # Main project settings
├── core/                # User profiles, dashboard, feed, auth
├── issues/              # Issue reporting & AI verification & tasks
├── store/               # EcoCoin store, redemptions
├── admin_panel/         # Department dashboards
├── templates/           # HTML templates
├── static/              # CSS, JS, assets
```

---

## 📊 System Workflow

1. **User Action** → Report issue or complete task.
2. **AI Verification** → Matches image + description + department.
3. **EcoCoins Awarded** → Coins credited based on authenticity & engagement.
4. **Department Panel** → Department views and updates issue status.
5. **Store Redemption** → User redeems offer, voucher is generated.
6. **Physical Claim** → User shows voucher to merchant to claim reward.

---

## 🛠 Setup & Deployment (Quick Start)

> These steps assume you have Python 3.11+, pip, and git installed.

1. **Clone project**

```bash
git clone https://github.com/dhirajdurgade7758/city_connect.git
cd city_connect
```

2. **Create virtual environment & install deps**

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate     # Windows PowerShell
pip install -r requirements.txt
```

3. **Create `.env` and set environment variables** (example):

```
DJANGO_SECRET_KEY="your_secret"
DEBUG=False
DATABASE_URL=postgres://user:pass@host:port/dbname
GEMINI_API_KEY=xxxxx
HF_API_KEY=xxxxx
GOOGLE_MAPS_API_KEY=xxxxx
EMAIL_HOST=smtp...
EMAIL_PORT=587
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
```

4. **Migrate & collect static**

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

5. **Create a superuser**

```bash
python manage.py createsuperuser
```

6. **Deploy to Render / Railway**

* Add `Procfile`: `web: gunicorn cityconnect.wsgi`
* Ensure `requirements.txt` includes `gunicorn`, `whitenoise`, `dj-database-url`, `psycopg2-binary`.
* Set environment variables in platform dashboard.
* Trigger deploy and run migrations.

---

## 🔮 Future Enhancements

* Mobile App (Flutter / React Native)
* Push notifications for verification, rewards, and badges
* Advanced AI fake report detection and anomaly detection
* Shopkeeper / Donor self-service panel
* City Analytics Dashboard with heatmaps & KPIs

---

## 👨‍💻 Team & Credits

Developed as part of the **MIT IEE 24-Hour National Level Hackathon**.

**Team Goal**: Create a scalable Smart City + AI-powered Gamification Platform that makes civic engagement transparent, rewarding, and impactful.

---

## 🏁 Conclusion

CityConnect is more than a hackathon project — it’s a blueprint for smarter, greener, and more engaged cities. By combining AI verification with gamified incentives, CityConnect makes civic participation meaningful and rewarding.

---

## 📬 Contact

For questions or collaboration, contact the team via the project GitHub repository.

---

*Made with ❤️ for civic good.*
