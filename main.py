from fastapi import FastAPI
from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.params import body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2 import RealDictCursor
import time


app = FastAPI()

class Post(BaseModel):
    title: int
    content: str
    published: bool =  True

while True:
    try:
        conn = psycopg2.connect(
            host= 'localhost', 
            database='fastapi', 
            user='postgres',
            password='password',
            cursor_factory=RealDictCursor
            )
        # execute SQL statements
        cursor = conn.cursor()
        print('PostgreSQL database connection was successfully established.')
        break
    except Exception as e:
        print(f"The error '{e}' occurred")
        time.sleep(2)
        

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute('SELECT * FROM posts')
    # to run it, have to to use fetchall()  to get the data
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def created_post(post: Post):
    #parametized query 1 values passed as title, content, published
    cursor.execute('INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)', 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute('SELECT * FROM posts WHERE id = %s', (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} not found")
    return {"post_detail": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute('DELETE FROM posts WHERE id = %s', (str(id),))
    conn.commit()
    return {"message": f"Post with id: {id} deleted successfully"}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute('SELECT * FROM posts WHERE id = %s', (str(id),))
    existing_post = cursor.fetchone()
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} not found")
    cursor.execute('UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s', 
                   (post.title, post.content, post.published, str(id)))
    conn.commit()
    return {"message": f"Post with id: {id} updated successfully"}