# Sky Management System

This is a collaborative Django-based management platform. 
The project uses a **Hub-and-Spoke architecture** with a centralized Dashboard and independent functional modules.

---

## 🛠️ Quick Start Guide (For the Team)

Follow these steps to get the project running on your local machine:

1. **Clone the Repository**:
   Open VS Code, press `Ctrl+Shift+P`, type `Git: Clone`, and paste the link.

2. **Install Requirements**:
   Open the terminal in VS Code and run:
   ```bash
   pip install django
   ```

3. **Launch the System**:
   Important: I've already included the database, so you DON'T need to run migrate or create superuser.
   Just start the server:
   ```bash
   python manage.py runserver
   ```

4. **Access the Admin Panel**:
   Go to `http://127.0.0.1:8000/admin/`
   * **Username:** `admin`
   * **Password:** [CHECK WHATSAPP GROUP]

---

## 📁 Project Structure

* **coreApp/**: Manages global settings, the sidebar, and the Dashboard.
* **templates/**: Contains `base.html`. **All students must extend this file.**
* **Individual Folders**: Work only inside your assigned app (e.g., `messaging/`, `teams/`).

---

## 🎨 How to Build Your Pages

To ensure the sidebar and design stay consistent, start every HTML file with:
```html
{% extends 'base.html' %}

{% block content %}
    {% endblock %}
```

---

## 🔄 Git Workflow (Rule of Three)

1. **PULL**: Always "Pull" before starting to get the latest updates.
2. **COMMIT**: Save your changes with a clear message.
3. **PUSH**: Upload your work so the rest of the team can see it.
