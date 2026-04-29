# Sky Management System

This is a collaborative Django-based management platform. 
The project uses a **Hub-and-Spoke architecture** with a centralized Dashboard and independent functional modules.

---

## 🛠️ Quick Start Guide (For the Team)

Follow these steps to get the project running on your local machine:

1. **Get the latest code**:
   ```bash
   git fetch origin
   git checkout main
   git pull origin main
   ```

2. **Set up your environment file**:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and set `DJANGO_SECRET_KEY` to any non-empty string.

3. **Install all dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Build the database** (run this every time after pulling):
   ```bash
   python manage.py migrate
   ```

5. **Create the standard admin user**:
   ```bash
   python manage.py createsuperuser
   ```
   Use: **username:** `admin` | **password:** `dev12345`

6. **Run the server**:
   ```bash
   python manage.py runserver
   ```
   Open `http://127.0.0.1:8000/`

---

## 🔑 Marker / Demo Login

| URL | Username | Password |
|-----|----------|----------|
| `http://127.0.0.1:8000/admin/` | `admin` | `dev12345` |
| `http://127.0.0.1:8000/` | `admin` | `dev12345` |

---

## 📁 Project Structure

* **coreApp/**: Manages global settings, the sidebar, and the Dashboard.
* **templates/**: Contains `base.html`. **All students must extend this file.**
* **Individual Folders**: Work only inside your assigned app (e.g., `messaging/`, `teams/`).

---
### 👥 Team Folder Assignments

To keep our database synchronized and avoid code conflicts, please work strictly within your assigned app folders:

* Student 1 (Teams): Use folder teams/
* Student 2 (Organisation): Use folder organisation/
* Student 3 (Messages): Use folder messaging/
* Student 4 (Schedule): Use folder schedules/
* Student 5 (Reports & System Core): Use folders reports/ and coreApp/

⚠️ IMPORTANT: Please do NOT modify any files in the coreApp/ folder. This folder contains the master settings for the entire project.

---

## 🎨 How to Build Your Pages

To ensure the sidebar and design stay consistent, start every HTML file with:
```html
{% extends 'base.html' %}

{% block content %}
    {% endblock %}
```

---

# 🛠 FULL GITHUB WORKFLOW GUIDE

---

### 🏁 PHASE 1: INITIALIZATION (Do this ONLY ONCE)
*After you have cloned the repository, you need to create your own workspace:*

1. **Create the branch locally:**
   ```bash
   git checkout -b student-yourName-yourTaskName
   ```
2. **Make a small change** (e.g., add a comment in a file or create your app folder).
3. **Commit and Push** (to appear in the Contributors list):
   ```bash
   git add .
   git commit -m "First commit to my individual branch"
   git push -u origin student-yourName-yourTaskName
   ```
   > 💡 **Note:** This links your branch to GitHub so you don't have to type the name ever again.

---

### 🔄 PHASE 2: DAILY ROUTINE (Every time you work)
#### 📌 The Git Rule: **Pull → Commit → Push**
*Once your branch is set up, follow this loop every time you sit down to code:*

1. **STARTING YOUR WORK (Pull) 📥**
   ```bash
   git pull origin main
   ```
   *Do this first! It gets the latest updates from the Lead (new CSS, DB models) so your code stays compatible with the main project.*

2. **DURING WORK (Commit) 💾**
   ```bash
   git add .
   git commit -m "Brief description of what you added"
   ```
   *Do this often to save your progress locally. Think of it as a "save point."*

3. **FINISHING YOUR WORK (Push) 🚀**
   ```bash
   git push
   ```
   > 💡 **Note:** Since your branch is already linked, this is all you need!

---

### ⚠️ THE GOLDEN RULE
**NEVER push directly to the `main` branch.** Always work inside your named branch. When your feature is 100% finished, open a **Pull Request** for review.

---
