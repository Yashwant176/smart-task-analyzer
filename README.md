# Smart Task Analyzer 🧠✅

A full-stack web application that intelligently analyzes and prioritizes tasks using a dynamic scoring system based on urgency, importance, effort, and dependencies.

This project was built for the Singularium Internship Assignment 2025 and strictly follows all core requirements while incorporating additional intelligent logic enhancements.

---

## 🚀 Features

### ✅ Core Functionalities
- Add individual tasks via interactive UI  
- Bulk task input using JSON array  
- Dynamic task prioritization using intelligent scoring  
- Strategy-based task analysis:
  - Smart Balance  
  - Fastest Wins  
  - High Impact  
  - Deadline Driven  
- Dependency handling with cycle detection  
- Task suggestions and explanations  
- REST API for task analysis  
- Responsive modern UI  

---

## 🧠 Smart Scoring System

Each task is scored using a weighted formula based on:

- Urgency (due date proximity)  
- Importance (1–10 scale)  
- Effort (estimated hours)  
- Dependency impact (blocked tasks)  

### Strategies modify weights dynamically:

| Strategy | Focus |
|----------|--------|
Smart Balance | Balanced decision-making  
Fastest Wins | Prioritises low-effort tasks  
High Impact | Prioritises importance  
Deadline Driven | Prioritises urgent deadlines  

---

## 🎁 Bonus & Enhancements Implemented

✅ Circular Dependency Detection  
✅ Comprehensive Unit Tests  
✅ Intelligent Task Suggestions  
✅ Error handling + validation logic  

(Not implemented: Dependency graph visualization, Eisenhower matrix, learning system as they were optional)

---

## 🛠 Tech Stack

- Backend: Django (Python)  
- Frontend: HTML, CSS, JavaScript  
- Styling: Custom Dark UI Theme  
- Testing: Django Test Framework  

---

## 📁 Project Structure

task-analyzer/
├── backend/
│ ├── manage.py
│ ├── backend/
│ └── tasks/
│ ├── static/
│ ├── templates/
│ ├── tests.py
│ ├── scoring.py
│ ├── views.py
│
├── README.md
├── requirements.txt


---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/Yashwant176/smart-task-analyzer.git
cd smart-task-analyzer/backend

2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Run Server
python manage.py runserver


Open browser:

http://127.0.0.1:8000/

🧪 Run Unit Tests
python manage.py test


Expected output:

OK

🔗 API Endpoints
Analyze Tasks
POST /api/analyze/


Accepts JSON task array and returns ranked task list with scores.

Suggestions
POST /api/suggest/


Returns intelligent productivity advice based on task patterns.


🖥 UI Workflow

1. Add tasks manually OR paste JSON array

2. Select strategy

3. Click Analyze Tasks

4. View ranked results + suggestions

If both manual & JSON are present → JSON takes precedence.

👨‍💻 Author

Yashwant Kumar
GitHub: https://github.com/Yashwant176

Portfolio: https://yashwant.is-a.dev

LinkedIn: https://www.linkedin.com/in/kyashwantkumar/