# 🌌 Sky Management System
**Collaborative Agile Management Platform**

The Sky Management System is a comprehensive Django-based application designed to manage organizational hierarchies, project dependencies, and team communications. The project utilizes a **Hub-and-Spoke architecture**, centering all functional modules around a unified, data-rich Dashboard.

---

## 🚀 Setup & Installation Guide (For Examiners)

This project is submitted in a **complete, working state**. All environment variables and the database are pre-configured for immediate evaluation.

### 1. Environment Configuration
*   **Virtual Environment:** It is recommended to use a virtual environment to isolate dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # Mac/Linux
    venv\Scripts\activate     # Windows
    ```
*   **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
*   **Environment Variables:** A pre-configured `.env` file is already included in the root directory for your convenience. No further setup is required.

### 2. Database & Data Integrity
A pre-populated database (`db.sqlite3`) is included in this submission.
*   **Ready-to-Run:** You do not need to run migrations or sync scripts unless you wish to reset the environment.
*   **Automation Feature:** The project includes a custom `master_sync` command that automates the population of Departments, Teams, and UserProfiles from the included Excel dataset.

### 3. Launch the Application
*   **Run Server:**
    ```bash
    python manage.py runserver
    ```
*   **URL:** Access the platform at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔑 Demo Credentials
The following accounts are ready for testing different access levels:

| Role | Username | Password |
|:---|:---|:---|
| **Superuser / Admin** | `admin` | `dev12345` |
| **Team Lead** | `dianaTeamLead` | `dev12345` |
| **Team Member** | `dianaMemberExample` | `dev12345` |

---

## 📁 Technical Architecture & Integration

The application is structured into modular apps, integrated through a central core to ensure a unified user experience:

*   **`coreApp`**: The central integration layer managing the Dashboard and Global Context Processors.
*   **`accounts`**: Manages user identity, secure profile editing, and automated avatar lifecycle.
*   **`organizations`**: Defines the high-level hierarchical structures and departmental foundations.
*   **`teams`**: Handles the organizational registry, project tracking, and complex dependency mapping.
*   **`messaging`**: Facilitates secure peer-to-peer and team-wide communication.
*   **`scheduler`**: Manages team timelines, project deadlines, and event coordination.
*   **`reports`**: Aggregates data across all modules to generate real-time analytics.
*   **`site_settings`**: Controls dynamic global configurations and site-wide variables.

### High-Level Features:
*   **Data Integrity:** Automated "Atomic Link Repair" logic ensures that user roles are always synchronized with the organizational structure.
*   **Global Context:** Custom processors (e.g., `sidebar_profile`) ensure the user's profile and role are consistently rendered across all views.
*   **Namespace Routing:** Standardized URL namespacing prevents routing conflicts and supports deep-linking across all modules.
---

## 🛠 Project Maintenance
To reset the environment to its baseline state if the database becomes corrupted:
1. Delete the `db.sqlite3` file.
2. Run `python manage.py migrate`.
3. Run `python manage.py seed_data` to re-ingest the Excel registry.

---
