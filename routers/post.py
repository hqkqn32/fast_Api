from fastapi import FastAPI, HTTPException, status, Depends,APIRouter
from typing import List,Optional
from sqlalchemy.orm import Session
import models   # . yerine direkt import
from database import engine, SessionLocal,get_db
from schemas import PostBase,PostResponse,PostCreate,UserOut
import oautho2
from sqlalchemy import func


router=APIRouter(prefix="/posts",tags=["posts"])

@router.get("/", response_model=List[PostResponse])


def get_posts(db: Session = Depends(get_db),user_id:int=Depends(oautho2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).order_by(models.Post.id).limit(limit).offset(skip).all()
    print(limit)
    result=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id)
    print(result)
    
    return posts



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oautho2.get_current_user),limit:int=10):
    print(f"Current User ID: {current_user.id}")
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db),user_id:int=Depends(oautho2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oautho2.get_current_user)
):
    # Post sorgusu
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # Post nesnesi bulunamadıysa hata döndür
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )

    # Debug bilgisi
    print(f"get_current_user'ın bulduğu id: {current_user.id}")
    print(f"Sorgunun bulduğu owner_id: {post.owner_id}")

    # Yetkilendirme kontrolü
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="İzniniz yok, bu post'u silemezsiniz."
        )

    # Silme işlemi
    post_query.delete(synchronize_session=False)
    db.commit()
    return



@router.put("/{id}", response_model=PostBase)
def update_post(
    id: int,
    updated_post: PostBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oautho2.get_current_user)
):
    # Post sorgusu
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # Post bulunamadıysa hata döndür
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )

    # Yetki kontrolü
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="İzniniz yok, bu post'u güncelleyemezsiniz."
        )

    # Güncelleme işlemi
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    updated_post = post_query.first()  # Güncellenmiş post'u al

    return updated_post
