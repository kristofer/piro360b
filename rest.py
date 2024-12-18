from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
import uvicorn
from models import Piro, Tag, User, create_engine, SQLModel


# TODO: Make this class the primary, it needs to opena connection to the database
# and then pass that connection to the FastAPI app
# using the session instead as a DI, isn't the right thing.

origins = [
    "http://localhost",
    "http://localhost:9000",
]


class Piro360rest:
    def __init__(self, session):
        self.app = FastAPI()
        self.session = session
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


    def start(self):
        @self.app.get("/")
        def read_root():
            return {"message": "Welcome to the Piro360 REST server"}

        @self.app.post("/api/piros/", response_model=Piro)
        def create_piro(piro: Piro, db: Session = Depends(self.get_db)):
            db.add(piro)
            db.commit()
            db.refresh(piro)
            return piro

        @self.app.get("/api/piros/", response_model=list[Piro])
        def read_piros(skip: int = 0, limit: int = 10, db: Session = Depends(self.get_db)):
            statement = select(Piro).offset(skip).limit(limit)
            results = db.exec(statement)
            piros = results.all()
            return piros

        @self.app.get("/api/piros/{piro_id}", response_model=Piro)
        def read_piro(piro_id: int, db: Session = Depends(self.get_db)):
            piro = db.get(Piro, piro_id)
            if not piro:
                raise HTTPException(status_code=404, detail="Piro not found")
            return piro

        @self.app.put("/api/piros/{piro_id}", response_model=Piro)
        def update_piro(piro_id: int, piro: Piro, db: Session = Depends(self.get_db)):
            db_piro = db.get(Piro, piro_id)
            if not db_piro:
                raise HTTPException(status_code=404, detail="Piro not found")
            piro_data = piro.dict(exclude_unset=True)
            for key, value in piro_data.items():
                setattr(db_piro, key, value)
            db.add(db_piro)
            db.commit()
            db.refresh(db_piro)
            return db_piro

        @self.app.delete("/api/piros/{piro_id}")
        def delete_piro(piro_id: int, db: Session = Depends(self.get_db)):
            piro = db.get(Piro, piro_id)
            if not piro:
                raise HTTPException(status_code=404, detail="Piro not found")
            db.delete(piro)
            db.commit()
            return {"detail": "Piro deleted"}

        @self.app.post("/api/tags/", response_model=Tag)
        def create_tag(tag: Tag, db: Session = Depends(self.get_db)):
            db.add(tag)
            db.commit()
            db.refresh(tag)
            return tag

        @self.app.get("/api/tags/", response_model=list[Tag])
        def read_tags(skip: int = 0, limit: int = 10, db: Session = Depends(self.get_db)):
            statement = select(Tag).offset(skip).limit(limit)
            results = db.exec(statement)
            tags = results.all()
            return tags

        @self.app.get("/api/tags/{tag_id}", response_model=Tag)
        def read_tag(tag_id: int, db: Session = Depends(self.get_db)):
            tag = db.get(Tag, tag_id)
            if not tag:
                raise HTTPException(status_code=404, detail="Tag not found")
            return tag

        @self.app.put("/api/tags/{tag_id}", response_model=Tag)
        def update_tag(tag_id: int, tag: Tag, db: Session = Depends(self.get_db)):
            db_tag = db.get(Tag, tag_id)
            if not db_tag:
                raise HTTPException(status_code=404, detail="Tag not found")
            tag_data = tag.dict(exclude_unset=True)
            for key, value in tag_data.items():
                setattr(db_tag, key, value)
            db.add(db_tag)
            db.commit()
            db.refresh(db_tag)
            return db_tag

        @self.app.delete("/api/tags/{tag_id}")
        def delete_tag(tag_id: int, db: Session = Depends(self.get_db)):
            tag = db.get(Tag, tag_id)
            if not tag:
                raise HTTPException(status_code=404, detail="Tag not found")
            db.delete(tag)
            db.commit()
            return {"detail": "Tag deleted"}

        @self.app.post("/api/users/", response_model=User)
        def create_user(user: User, db: Session = Depends(self.get_db)):
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

        @self.app.get("/api/users/", response_model=list[User])
        def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(self.get_db)):
            statement = select(User).offset(skip).limit(limit)
            results = db.exec(statement)
            users = results.all()
            print('users', len(users))
            return users

        @self.app.get("/api/users/{user_id}", response_model=User)
        def read_user(user_id: int, db: Session = Depends(self.get_db)):
            user = db.get(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user

        @self.app.put("/api/users/{user_id}", response_model=User)
        def update_user(user_id: int, user: User, db: Session = Depends(self.get_db)):
            db_user = db.get(User, user_id)
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            user_data = user.dict(exclude_unset=True)
            for key, value in user_data.items():
                setattr(db_user, key, value)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user

        @self.app.delete("/api/users/{user_id}")
        def delete_user(user_id: int, db: Session = Depends(self.get_db)):
            user = db.get(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            db.delete(user)
            db.commit()
            return {"detail": "User deleted"}

        return self.app

    def get_db(self):
        db = self.session
        # try:
        #     yield db
        # finally:
        #     db.close()
        return db

    def run_app(self):
        uvicorn.run(self.start(), host="0.0.0.0", port=8080)

if __name__ == "__main__":
    engine = create_engine('sqlite:///test.db')
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        app_instance = Piro360rest(session)
        uvicorn.run(app_instance.start(), host="0.0.0.0", port=8080)
