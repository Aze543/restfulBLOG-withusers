# 📝 RESTful Blog Platform with User Authentication

> A full-stack RESTful blogging web application featuring multi-user authentication, rich text editing, role-based controls, and persistent database management.

---

## 📋 Table of Contents
- [About The Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture & Structure](#-project-architecture--structure)
- [Getting Started](#-getting-started)
- [Usage & Workflows](#-usage--workflows)
- [Author](#-author)

---

## 🎯 About The Project

**RESTful Blog Platform** is a personal web application designed to demonstrate clean RESTful routing architecture, secure authentication patterns, and database relationship management using Python and Flask. 

The application allows users to register, log in, comment on posts, and view blog content, while giving admin users full CRUD (Create, Read, Update, Delete) administrative capabilities over articles and platform management.

---

## ✨ Key Features

- **RESTful Routing:** Standardized HTTP endpoints for navigating, creating, updating, and deleting blog posts.
- **User Authentication & Authorization:** Secure user registration and login flows powered by password hashing and session management.
- **Role-Based Access Control:** Differentiated access levels restricting administrative actions (creating/editing/deleting posts) to author/admin accounts.
- **Interactive Comment System:** Authenticated users can post comments linked directly to specific blog articles.
- **Rich Text Integration:** Integrated WYSIWYG editor (CKEditor) for drafting styled blog posts with embedded images and formatting.
- **Avatar Customization:** Automatic user profile avatar generation via Gravatar integration based on user email.

---

## 🛠️ Tech Stack

* **Backend Framework:** Python, Flask
* **Database & ORM:** SQLite, Flask-SQLAlchemy
* **Authentication & Security:** Flask-Login, Werkzeug (Password Hashing)
* **Templating & Forms:** Jinja2, Flask-WTF, WTForms
* **Frontend:** HTML5, CSS3, Bootstrap, CKEditor
* **Tools:** Git, GitHub

---

## 📂 Project Architecture & Structure

```text
restfulBLOG-withusers/
│
├── static/          # CSS stylesheets, JavaScript, and image assets
├── templates/       # Jinja2 HTML templates (index, post, login, register, etc.)
├── main.py          # Application entry point, routes, and Flask models
├── forms.py         # WTForms definitions for validation
├── instance/        # Local SQLite database instance
├── requirements.txt # Project dependencies
└── README.md        # Project documentation
