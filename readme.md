# 🌍 CityConnect – AI-Powered Civic Engagement & EcoCoin Rewards

### 🏆 MIT IEE 24-Hour National Level Hackathon Project

CityConnect is an **AI-powered civic-tech + gamification platform** that empowers citizens to **report civic issues, complete eco-friendly tasks, and earn rewards**. The system integrates **AI verification, live location tracking, EcoCoin gamification, and departmental admin panels** to create a **smart city management ecosystem**.

---

## 🎯 Problem Statement

Citizens often face difficulties in reporting civic issues, and governments struggle with verification, accountability, and public engagement. Additionally, there is a lack of motivation for citizens to actively participate in eco-friendly initiatives.

**CityConnect solves this by:**

* Using **AI to verify issues & eco tasks**.
* Providing **gamified incentives (EcoCoins, badges, leaderboard)**.
* Building a **transparent reward system** where users can redeem offers.
* Giving **departments real-time dashboards** to track and resolve issues.

---

## 🚀 Features

### 👤 User Features

* **Profile Dashboard**: Track reports, tasks, EcoCoins, badges, and redemptions.
* **Issue Reporting Feed**:

  * Submit issues with **image, description, live location**.
  * **AI verification** ensures authenticity.
  * Like ❤️, Comment 💬, Save 📌, Share 🔗.
* **Eco Tasks**:

  * Complete eco-friendly tasks (waste management, plantation, etc.).
  * **AI validates** task submissions.
  * EcoCoins awarded automatically.
* **Gamification**:

  * Earn **EcoCoins** via issues, tasks, likes, and comments.
  * Unlock **badges** for milestones (First Post, 100 EcoCoins, etc.).
  * Compete on the **Leaderboard**.
* **EcoCoin Store**:

  * 4 categories: 🛍 Shop Offers, 🎁 Donor Gifts, 🎟 Event Tickets, 🌱 Eco Rewards.
  * Redeem offers → Generate **voucher PDF** → Claim at physical location.
* **Saved Posts**: Save/unsave posts with HTMX-powered UI.

---

### 🏛 Department Admin Panels

Departments manage issues in their category:

* **Electricity Department**
* **Waste Management Department**
* **Water Supply Department**
* **Public Works Department**

Each panel allows:

* Viewing issues assigned to department.
* Seeing **live location maps**.
* Updating issue status (Pending → In Progress → Resolved).
* Monitoring issue resolution history.

---

### 🎮 Gamification System

* **EcoCoins**:

  * Earned via tasks, issue reporting, likes, comments.
  * Spent in the EcoCoin Store.
* **Badges**:

  * 🐣 First Post
  * 🌱 Green Starter (50 EcoCoins)
  * 🌿 Eco Warrior (100 EcoCoins)
  * 🌳 Eco Champion (200 EcoCoins)
  * 🪐 Planet Protector (500 EcoCoins)
* **Leaderboard**:

  * Shows top contributors by EcoCoins.

---

### 🎁 EcoCoin Store

* **Categories**:

  * 🛍 Shop Offers – Discounts from local businesses.
  * 🎁 Donor Gifts – Items donated by citizens.
  * 🎟 Event Tickets – Concerts, workshops, city events.
  * 🌱 Eco Rewards – Plants, bottles, eco-bags.
* **Redemption Flow**:

  1. User redeems an offer.
  2. Coins deducted & stock reduced.
  3. Unique **voucher code** generated.
  4. User downloads/prints PDF receipt.
  5. Claim at physical store/location.

---

## ⚙️ Tech Stack

### Backend

* **Django 5.x** (Python)
* **PostgreSQL / SQLite**
* **OpenAI API** – Image & text verification
* **HTMX** – Interactive frontend updates

### Frontend

* **Django Templates**
* **Bootstrap 5**
* **Bootstrap Icons / FontAwesome**
* **JS + AJAX + HTMX**

### Other Integrations

* PDF Voucher Generation
* Live Location Fetch
* AI-based Coin Allocation

---

## 📂 Project Structure

```
cityconnect/
│── cityconnect/         # Main project settings
│── core/                # User profiles, dashboard, feed, auth
│── issues/              # Issue reporting & AI verification & Civic task submission 
│── store/               # EcoCoin store, redemptions
│── admin_panel/         # Department dashboards
│── templates/           # HTML templates
│── static/              # CSS, JS, assets
```

---

## 📊 System Workflow

1. **User Action** → Reports issue / Completes task.
2. **AI Verification** → Matches image + description + department.
3. **EcoCoins Awarded** → Based on authenticity & engagement.
4. **Department Panel** → Sees issue, updates status.
5. **Store Redemption** → User redeems offer, receives voucher.
6. **Physical Claim** → User shows voucher at store to get reward.

---

## 🎉 Impact

* ✅ Citizens empowered to report and act.
* ✅ AI ensures fairness & reduces fake reports.
* ✅ Gamification motivates civic participation.
* ✅ Departments get real-time actionable insights.
* ✅ Local businesses & donors engage with community.

---

## 🔮 Future Enhancements

* Mobile App (Flutter/React Native)
* Push Notifications (task verified, badge unlocked)
* AI Fake Report Detection (more advanced)
* Shopkeeper/Donor Self-Service Panel
* City Analytics Dashboard

---

## 👨‍💻 Team & Credits

Developed as part of **MIT IEE 24-Hour National Level Hackathon**.

**Team Goal**: To create a **Smart City + AI-powered Gamification Platform** that makes civic engagement **transparent, rewarding, and impactful**.

---

## 🏆 Conclusion

CityConnect is more than just a hackathon project – it’s a **scalable smart city solution** that bridges the gap between **citizens, government, and local businesses**, using the power of **AI + gamification** to make cities cleaner, greener, and more efficient.
