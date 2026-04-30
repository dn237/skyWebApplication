# 🌌 Sky Management System
**Collaborative Agile Management Platform**

The Sky Management System is a comprehensive Django-based application designed to manage organizational hierarchies, project dependencies, and team communications. The project utilizes a **Hub-and-Spoke architecture**, centering all functional modules around a unified, data-rich Dashboard.

---

## 🚀 Setup & Installation Guide (For Examiners)

Please follow these steps to initialize the project environment and view the integrated work.

### 1. Environment Configuration
*   **Virtual Environment:** It is recommended to use a virtual environment to isolate dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # Mac/Linux
    venv\Scripts\activate     # Windows
    
```
*   **Install Dependencies:** All necessary libraries, including **Pandas** and **OpenPyXL** for data ingestion, are included in this file.
    ```bash
    pip install -r requirements.txt
    ```
*   **Environment Variables:** Create a `.env` file in the root directory based on the provided `.env.example` template.
    ```bash
    # Example for Windows
    copy .env.example .env
    ```

### 2. Database Initialization & Automation
While a pre-populated database (`db.sqlite3`) is included in this submission, the project features a custom automation layer to ensure data consistency across all team modules.
*   **Apply Migrations:**
    ```bash
    python manage.py migrate
    ```
*   **Master Data Sync (Core Feature):** Run the custom management command to ingest the Excel Team Registry and repair user profiles.
    ```bash
    python manage.py master_sync
    ```
    > 💡 **Technical Note:** This script automates the population of Departments, Teams, Projects, and UserProfiles from a structured Excel dataset, serving as the "Single Source of Truth" for the entire application.

### 3. Launch the Application
*   **Run Server:**
    ```bash
    python manage.py runserver
    
```
*   **URL:** Access the platform at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔑 Demo Credentials
| Access Level | Username | Password |
|:---|:---|:---|
| **Superuser / Admin** | `admin` | `dev12345` |
| **Standard User** | (Generated via `master_sync`) | N/A |

---

## 📁 Technical Architecture & Integration

The application is structured into modular apps, integrated through a central core to ensure a unified user experience:

*   **`coreApp`**: The central integration layer managing the Dashboard and Global Context Processors.
*   **`accounts`**: Manages user identity, secure profile editing, and automated avatar lifecycle.
*   **`teams`**: Handles the organizational registry, project tracking, and complex dependency mapping.
*   **Integrated Modules**: Seamlessly integrated `messaging`, `schedules`, and `reports` modules from group contributors.

### High-Level Features:
*   **Data Integrity:** Automated "Atomic Link Repair" logic ensures that user roles (e.g., Team Lead vs. Engineer) are always synchronized with the organizational structure.
*   **Global Context:** Custom processors (e.g., `sidebar_profile`) ensure the user's profile and role are consistently rendered across all 15+ views.
*   **Namespace Routing:** Standardized URL namespacing across all apps to prevent routing conflicts and support deep-linking (e.g., messaging a Team Lead directly from the Teams Registry).

---

## 🛠 Project Maintenance
To reset the environment to its baseline state:
1. Delete the `db.sqlite3` file.
2. Run `python manage.py migrate`.
3. Run `python manage.py master_sync` to re-ingest the Excel registry.
