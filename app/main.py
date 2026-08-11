from fastapi import FastAPI, Request, Form, UploadFile, File 
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.database import connection, cursor
from app.security import hash_password, verify_password
from starlette.middleware.sessions import SessionMiddleware
import shutil
from fastapi.staticfiles import StaticFiles

app= FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.add_middleware(
    SessionMiddleware,
    secret_key="my-secret-key"
)

templates = Jinja2Templates(directory='templates')
@app.get("/")
def home(request:Request):
    return templates.TemplateResponse(
                                        request=request,
                                        name = 'home.html',
                                        context = {}
                                        )
# register user
@app.get("/register")
def register(request: Request):

    return templates.TemplateResponse(
                                        request = request,
                                        name= 'register_page.html',
                                        context = {}
                                    )

@app.post("/register")
def register_user(  request: Request,
                    username:str = Form(...),
                    email: str = Form(...),
                    password:str = Form(...),
                    confirm_password: str = Form(...)
                    ):
                    

    
    # check for same password
    if password != confirm_password:
        return templates.TemplateResponse(
                                            request= request,
                                            name='register_page.html',
                                            context = {'error': 'Password do not match'}
        )
    # check if email already exists
    cursor.execute("""
                    SELECT * FROM users 
                    WHERE email = ?
                    """, (email,)
                    )

    existing_user = cursor.fetchone()
    if existing_user:
        return templates.TemplateResponse(
                                            request= request,
                                            name = 'register_page.html',
                                            context = {'error': 'email already exists'}
                                        )

    hash_pass = hash_password(password)

    cursor.execute("""
                    INSERT INTO users(username, email, password)
                    VALUES (?, ?, ?)
                    """,
                    (username, email, hash_pass)
                    )  

    connection.commit()

    return RedirectResponse(
                            url='/login',
                            status_code= 303
                            )
    
# user login 
@app.get("/login")
def login(request: Request):

    return templates.TemplateResponse(
                                        request = request,
                                        name= 'login_page.html',
                                        context = {}
                                    )


@app.post("/login")
def login_page(
                request: Request,
                email:str = Form(...),
                password: str = Form(...)
                ):

    cursor.execute("""
                    SELECT * FROM users
                    WHERE email = ?
                    """,
                    (email,)
                    )
    existing_user = cursor.fetchone()

    if not existing_user:
        return templates.TemplateResponse(
                                            request = request,
                                            name = 'login_page.html',
                                            context ={'error': 'Invalid email or password'}
        )

    # check password
    if not verify_password(password, existing_user['password']):
        return templates.TemplateResponse(
                                            request = request,
                                            name = 'login_page.html',
                                            context = {'error': 'Invalid email or password'}
        )

    request.session["user_id"] = existing_user["id"]

    return RedirectResponse(
                            url = '/dashboard',
                            status_code = 303
                            )


# dashboard
@app.get("/dashboard")
def dashboard(request: Request):

    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    cursor.execute(
        """
        SELECT * FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={'user': user}
    )



@app.get("/posts")
def post(request: Request):

    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    cursor.execute("""
        SELECT
            posts.id,
            posts.title,
            posts.content,
            posts.image,
            posts.user_id,
            users.username AS author
        FROM posts
        JOIN users
        ON posts.user_id = users.id
        ORDER BY posts.id DESC
    """)

    posts = cursor.fetchall()

    return templates.TemplateResponse(
                                        request=request,
                                        name="post.html",
                                        context={
                                            "posts": posts,
                                            'user_id': user_id
                                            }
                                    )                

@app.get("/posts/create")
def create_post_page(request: Request):

    user = request.session.get('user_id')
    
    if not user:
        return RedirectResponse(
                                url = '/login',
                                status_code = 303
        )

    return templates.TemplateResponse(
                                        request = request,
                                        name='create_post.html',
                                        context = {}
                                    )    

@app.post("/posts/create")
def create_post(
                request: Request,
                title: str = Form(...),
                content: str = Form(...),
                image: UploadFile = File(None)
            ):
    user_id = request.session.get('user_id')

    if not user_id:
        return RedirectResponse(
                                    url="/login",
                                    status_code=303
                                )
    image_name = None

    if image and image.filename:
        image_name = image.filename

        file_path = f"static/uploads/{image_name}"

        with open(file_path,'wb') as buffer:
            shutil.copyfileobj(image.file,  buffer)

    cursor.execute("""
                    INSERT INTO posts
                    (title, content,image, user_id)
                    VALUES
                    (?,?,?,?)
                    """,
                    (
                        title, content, image_name, user_id
                    )
                    )
    connection.commit()

    return RedirectResponse(
                            url='/posts',
                            status_code = 303
                            )

@app.get("/logout")
def logout(request: Request):
    request.session.clear()

    return templates.TemplateResponse(
                                        request= request,
                                        name= 'login_page.html',
                                        context = {}
                                    )

@app.get("/posts/edit/{post_id}")
def edit_post(request: Request, post_id: int):

    user_id = request.session.get('user_id')

    if not user_id:
        return RedirectResponse(
                                url = '/login',
                                status_code= 303
                                )
    cursor.execute("""
                    SELECT * FROM posts
                    where id = ? 
                    """,
                    (post_id,))

    post = cursor.fetchone()

    return templates.TemplateResponse(
                                        request= request,
                                        name = "edit_post.html",
                                        context = {'post': post}
                                    )

@app.post("/posts/edit/{post_id}")
def update_post(
                    request: Request,
                    post_id: int,
                    title: str = Form(...),
                    content: str = Form(...),
                    image: UploadFile = File(None)
                ):

    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    cursor.execute(
                    """
                    SELECT * FROM posts
                    WHERE id = ? AND user_id=?
                    """,
                    (post_id, user_id)
                )

    post = cursor.fetchone()

    if not post:
        return RedirectResponse(
                                url="/posts",
                                status_code=303
                            )

    image_name = post["image"]

    if image and image.filename:

        image_name = image.filename

        file_path = f"static/uploads/{image_name}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    cursor.execute(
                """
                UPDATE posts
                SET title = ?, content = ?, image = ?
                WHERE id = ?
                """,
                    (
                        title,
                        content,
                        image_name,
                        post_id
                    )
                )

    connection.commit()

    return RedirectResponse(
                            url="/posts",
                            status_code=303
                            )


# delete
@app.post("/posts/delete/{post_id}")
def delete(request:Request, post_id:int):
    user_id = request.session.get('user_id')

    if not user_id:
        return RedirectResponse(
                                url='/login',
                                status_code=303
                                )
    
    cursor.execute("""
                    DELETE FROM posts
                    WHERE id = ? AND user_id = ?
                    """,
                    (post_id, user_id)
                    )

    connection.commit()

    return RedirectResponse(
                            url='/posts',
                            status_code = 303
                            )