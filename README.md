# **SwiftHub: A Django-Based Project Management System**

- **Frontend**: HTML, CSS, JavaScript, AdminLTE3
**SwiftHub** is a robust and flexible project management system built using Django and AdminLTE3. It is designed to enhance team collaboration, streamline task tracking, and simplify project progress monitoring. With its modern interface and rich features, **SwiftHub** caters to organizations, teams, and individuals aiming for efficient project workflows.

---

## **Table of Contents**
1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Core Functionalities](#core-functionalities)
7. [Screenshots](#screenshots)
8. [Future Enhancements](#future-enhancements)
9. [Contributing](#contributing)
10. [License](#license)
11. [Author](#author)

---

## **Features**
- **Kanban Board**: Drag-and-drop interface for task management.
- **Notifications**: Real-time alerts for task deadlines and updates.
- **Progress Tracking**: Automatic calculation of project progress.
- **Team Collaboration**: Assign roles and manage permissions.
- **Access Levels**: Role-based access control for users.
- **Attachments & Comments**: Upload files and communicate within tasks.
- **AdminLTE3 Integration**: Responsive and user-friendly UI design.
- **Task Deadline Alerts**: Notifications for tasks nearing expiry.
- **Customizable Templates**: Easily modify layout and design.

---

## **Technologies Used**
- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript, AdminLTE3
- **Database**: SQLite (default), with support for PostgreSQL and MySQL
- **Task Queue**: Celery
- **Notification System**: Redis


---

## **Installation**

### **Prerequisites**
- Python 3.9+
- pip (Python package manager)
- Virtual environment (recommended)

### **Steps**
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/projecthub.git
   cd projecthub
   ```

   A full list of dependencies is provided in `requirements.txt`.


2. Creating virtual environment and activating it linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate 
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply Migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Run the Server:
   ```bash
   python manage.py runserver
   ```

### **Project Structure**
