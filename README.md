# Project_09_OC
Créez une API sécurisée RESTful en utilisant Django REST

# 🛠️ 

A Django REST API for managing users, projects, issues, comments, and contributors.

---

## 🚀 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Razvan-drb/Project_09_OC
```

```bash
pip install -r requirements.txt
```

### Apply database migrations
```bash
python manage.py migrate

```

### Create a superuser

```bash
python manage.py createsuperuser

```

### Run the app

```bash
python manage.py runserver

```


# 🧪 API Features

### 👤 User Endpoints

| Method | Endpoint           | Description                          |
|--------|--------------------|--------------------------------------|
| POST   | `/api/users/`      | Create a new user                    |
| GET    | `/api/users/`      | View current user profile (auth required) |
| DELETE | `/api/users/{id}/` | Delete your user account             |



### 📁 Project Endpoints

| Method | Endpoint              | Description                                  |
|--------|-----------------------|----------------------------------------------|
| POST   | `/api/projects/`      | Create a new project                         |
| GET    | `/api/projects/`      | List all projects (requires auth)            |
| PUT    | `/api/projects/{id}/` | Update a project (only if you're the author) |
| DELETE | `/api/projects/{id}/` | Delete a project (only if you're the author) |


### 🧩 Issue Endpoints

| Method | Endpoint                        | Description                          |
|--------|----------------------------------|--------------------------------------|
| POST   | `/api/projects/{id}/issues/`     | Create an issue (must be a contributor) |
| GET    | `/api/issues/`                  | List issues (paginated)              |
| PUT    | `/api/issues/{id}/`             | Update issue (only the author)       |

---

### 💬 Comment Endpoints

| Method | Endpoint                   | Description                         |
|--------|----------------------------|-------------------------------------|
| POST   | `/api/comments/`           | Create a comment (linked to an issue) |
| GET    | `/api/comments/`           | List comments (paginated)           |
| PUT    | `/api/comments/{id}/`      | Update comment (only the author)    |
| DELETE | `/api/comments/{id}/`      | Delete comment (only the author)    |

---

### 👥 Contributor Endpoints

| Method | Endpoint                   | Description                             |
|--------|----------------------------|-----------------------------------------|
| POST   | `/api/contributors/`       | Add contributor (only project author)   |
| DELETE | `/api/contributors/{id}/`  | Remove contributor (only project author) |

