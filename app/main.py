from fastapi import Depends, FastAPI, HTTPException,status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
import database

from database import SessionLocal, engine

class Post(BaseModel):
    title:str
    content:str
    published:bool=True

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/posts")
def test_posts(db:Session=Depends(get_db)):
    posts =    db.query(models.Post).all()
    return{"data":posts}

@app.post("/posts")
def create_posts(post:Post,db:Session=Depends(get_db)):
   new_post=models.Post(**post.dict())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return{"data":new_post}
    
@app.get("/posts/{id}")
def get_post(id:int,db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id).first()

    if not post:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} not found")
    return{"post_detail":post}


@app.delete("/posts/{id}")
def delete_posts(id:int,db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id)

    if post.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return{"status":"successful"}

@app.delete("/posts")
def delete_post(id:int,db:Session=Depends(get_db)):
    post =db.query(models.Post).filter(models.Post.id==id)
