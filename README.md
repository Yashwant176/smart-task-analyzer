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


## ⚙️ Smart Task Analyzer - Full Setup & Usage

## 🧬 Clone Repository & Navigate
git clone https://github.com/Yashwant176/smart-task-analyzer.git
cd smart-task-analyzer/backend

### 🐍 Create & Activate Virtual Environment
python -m venv venv
venv\Scripts\activate

### 📦 Install Dependencies
pip install -r requirements.txt

### 🚀 Run Development Server
python manage.py runserver

### 🌐 Open in Browser
 http://127.0.0.1:8000/

### 🧪 Run Unit Tests
python manage.py test

# ✅ Expected Output:
 OK


## 🔗 API ENDPOINTS INFO

### 📊 Analyze Tasks
 POST /api/analyze/
 Accepts JSON task array and returns ranked task list with scores.

### 💡 Suggestions
 POST /api/suggest/
 Returns intelligent productivity advice based on task patterns.


## 🖥 UI WORKFLOW

 1. Add tasks manually OR paste JSON array
 2. Select strategy
 3. Click "Analyze Tasks"
 4. View ranked results + suggestions

## ⚠️ Note:
 If both manual & JSON are present → JSON takes precedence

##👨‍💻 Author

## K Yashwant Kumar
GitHub: https://github.com/Yashwant176

Portfolio: https://yashwant.is-a.dev

LinkedIn: https://www.linkedin.com/in/kyashwantkumar/
