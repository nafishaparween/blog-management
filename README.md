# Blog Management System

A Blog Management System built using **FastAPI, SQLite, Jinja2, and HTML**.

The application allows users to register, log in, create blog posts with images, view posts, edit their own posts, and delete their own posts.

## Features

- User registration
- User login and logout
- Password hashing
- Session-based authentication
- Create blog posts
- Upload images with posts
- View all blog posts
- Edit existing posts
- Change post images
- Delete posts
- User-based post ownership
- Users can edit and delete only their own posts
- SQLite database integration
- Jinja2 HTML templates

## Technologies Used

- Python
- FastAPI
- SQLite
- Jinja2
- HTML
- Passlib / bcrypt
- Starlette SessionMiddleware
- Uvicorn

## Project Structure

```text
blog-management/
├── app/
│   ├── main.py
│   ├── database.py
│   └── security.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── register_page.html
│   ├── login_page.html
│   ├── dashboard.html
│   ├── create_post.html
│   ├── edit_post.html
│   └── post.html
├── static/
│   └── uploads/
├── requirements.txt
└── README.md
```

## Database

The application uses **SQLite** for storing users and blog posts.

### Users Table

The users table stores:

- id
- username
- email
- password

Passwords are stored as hashed passwords rather than plain text.

### Posts Table

The posts table stores:

- id
- title
- content
- image
- user_id

The `user_id` connects each blog post to the user who created it.

## Authentication and Authorization

The application uses session-based authentication.

After successful login, the user's ID is stored in the session.

Post ownership is also checked before allowing edit or delete operations. This prevents one logged-in user from editing or deleting another user's posts.

## Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/nafishaparween/blog-management
```

Move into the project directory:

```bash
cd blog-management
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

### 5. Open the application

Open the following address in your browser:

```text
http://127.0.0.1:8000
```

## Application Flow

```text
Register
   ↓
Login
   ↓
Dashboard
   ↓
Create Post
   ↓
Add Title + Content + Optional Image
   ↓
Publish
   ↓
View Posts
   ↓
Edit / Delete Own Posts
```

## What I Learned

While building this project, I practiced:

- Creating FastAPI routes
- Working with GET and POST requests
- Handling HTML forms
- Using Jinja2 templates
- Working with SQLite databases
- Writing SQL queries
- Creating relationships using `user_id`
- Password hashing and password verification
- Session-based authentication
- Protecting routes for logged-in users
- User authorization and post ownership
- Uploading and displaying images
- Creating CRUD operations
- Redirecting users between pages

## CRUD Operations

The project implements complete CRUD functionality for blog posts:

- **Create** — Create a new blog post
- **Read** — View blog posts
- **Update** — Edit an existing blog post
- **Delete** — Delete an existing blog post

## Future Improvements

Possible improvements for future versions:

- Improve frontend styling
- Add post search and filtering
- Add pagination
- Add individual post detail pages
- Add post creation and update timestamps
- Improve image handling
- Add stronger form validation
- Refactor the application using FastAPI routers
- Move to SQLAlchemy for database operations

