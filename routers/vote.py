from fastapi import FastAPI,Response,status, HTTPException, Depends, APIRouter
import database,schemas,models,oautho2
from sqlalchemy.orm import Session

router=APIRouter(prefix="/vote",tags=['votes'])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(database.get_db),current_user:int=Depends(oautho2.get_current_user)):
   post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
   if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {vote.post_id} does not exsiist")
   vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)

   found_vote=vote_query.first()
   print(f"Current user ID: {current_user.id}")
   print(f"votes post ID: {vote.post_id}")
   print(found_vote)
   



   if (vote.dir==1):

      if found_vote:
         raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user{current_user.id} has already voted on post {vote.post_id}")
    
      new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
      db.add(new_vote)
      db.commit()
      return {"message":"succesfully added vote"}
   else:
      if not found_vote:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="votes does not exist")
      
      vote_query.delete(synchronize_session=False)
      db.commit()
      return{"message":"helal sildin"}





