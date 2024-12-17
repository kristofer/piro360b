from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import uvicorn
from models import Base, Piro, Tag, User, create_engine, sessionmaker

class Piro360rest:
    def __init__(self, session):
        self.app = FastAPI()
        self.session = session

    def start(self):
        @self.app.get("/")
        def read_root():
            return {"message": "Welcome to the Piro360 REST server"}

##
##
## PIRO
##
        @self.app.post("/piros/", response_model=Piro)
        def create_piro(piro: Piro, db: Session = Depends(self.get_db)):
            db.add(piro)
            db.commit()
            db.refresh(piro)
            return piro

        @self.app.get("/piros/", response_model=list[Piro])
        def read_piros(skip: int = 0, limit: int = 10, db: Session = Depends(self.get_db)):
            piros = db.query(Piro).offset(skip).limit(limit).all()
            return piros

        @self.app.get("/piros/{piro_id}", response_model=Piro)
        def read_piro(piro_id: int, db: Session = Depends(self.get_db)):
            piro = db.query(Piro).filter(Piro.id == piro_id).first()
            if piro is None:
                raise HTTPException(status_code=404, detail="Piro not found")
            return piro

        @self.app.put("/piros/{piro_id}", response_model=Piro)
        def update_piro(piro_id: int, piro: Piro, db: Session = Depends(self.get_db)):
            db_piro = db.query(Piro).filter(Piro.id == piro_id).first()
            if db_piro is None:
                raise HTTPException(status_code=404, detail="Piro not found")
            for key, value in piro.dict().items():
                setattr(db_piro, key, value)
            db.commit()
            db.refresh(db_piro)
            return db_piro

        @self.app.delete("/piros/{piro_id}")
        def delete_piro(piro_id: int, db: Session = Depends(self.get_db)):
            db_piro = db.query(Piro).filter(Piro.id == piro_id).first()
            if db_piro is None:
                raise HTTPException(status_code=404, detail="Piro not found")
            db.delete(db_piro)
            db.commit()
            return {"detail": "Piro deleted"}

##
##
## TAG
##
        @self.app.post("/tags/", response_model=Tag)
        def create_tag(tag: Tag, db: Session = Depends(self.get_db)):
            db.add(tag)
            db.commit()
            db.refresh(tag)
            return tag

        @self.app.get("/tags/", response_model=list[Tag])
        def read_tags(skip: int = 0, limit: int = 10, db: Session = Depends(self.get_db)):
            tags = db.query(Tag).offset(skip).limit(limit).all()
            return tags

        @self.app.get("/tags/{tag_id}", response_model=Tag)
        def read_tag(tag_id: int, db: Session = Depends(self.get_db)):
            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag is None:
                raise HTTPException(status_code=404, detail="Tag not found")
            return tag

        @self.app.put("/tags/{tag_id}", response_model=Tag)
        def update_tag(tag_id: int, tag: Tag, db: Session = Depends(self.get_db)):
            db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if db_tag is None:
                raise HTTPException(status_code=404, detail="Tag not found")
            for key, value in tag.dict().items():
                setattr(db_tag, key, value)
            db.commit()
            db.refresh(db_tag)
            return db_tag

        @self.app.delete("/tags/{tag_id}")
        def delete_tag(tag_id: int, db: Session = Depends(self.get_db)):
            db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if db_tag is None:
                raise HTTPException(status_code=404, detail="Tag not found")
            db.delete(db_tag)
            db.commit()
            return {"detail": "Tag deleted"}

##
##
## USER
##
        @self.app.post("/users/", response_model=User)
        def create_user(user: User, db: Session = Depends(self.get_db)):
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

        @self.app.get("/users/", response_model=list[User])
        def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(self.get_db)):
            users = db.query(User).offset(skip).limit(limit).all()
            return users

        @self.app.get("/users/{user_id}", response_model=User)
        def read_user(user_id: int, db: Session = Depends(self.get_db)):
            user = db.query(User).filter(User.id == user_id).first()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return user

        @self.app.put("/users/{user_id}", response_model=User)
        def update_user(user_id: int, user: User, db: Session = Depends(self.get_db)):
            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            for key, value in user.dict().items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
            return db_user

        @self.app.delete("/users/{user_id}")
        def delete_user(user_id: int, db: Session = Depends(self.get_db)):
            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            db.delete(db_user)
            db.commit()
            return {"detail": "User deleted"}

        # end creation of app
        return self.app


    def get_db(self):
        db = self.session()
        try:
            yield db
        finally:
            db.close()

    def run_app(self):
        uvicorn.run(self.start(), host="0.0.0.0", port=8000)
        
# if __name__ == "__main__":
#     app_instance = Piro360rest()
#     uvicorn.run(app_instance.start(), host="0.0.0.0", port=8000)


if __name__ == "__main__":
    engine = create_engine('sqlite:///piro360.db')
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    app_instance = Piro360rest(SessionLocal)
    uvicorn.run(app_instance.start(), host="0.0.0.0", port=8000)