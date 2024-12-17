from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, create_engine, Session, select

class PiroTagLink(SQLModel, table=True):
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    piro_id: Optional[int] = Field(default=None, foreign_key="piro.id", primary_key=True)

class PiroBase(SQLModel):
    title: str
    description: Optional[str] = None
    s3urltovideo: Optional[str] = None
    imagename: Optional[str] = None
    location: Optional[str] = None
    created: Optional[str] = None
    owner_id: int

class Piro(PiroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    tags: List["Tag"] = Relationship(back_populates="piros", link_model=PiroTagLink)
    owner: "User" = Relationship(back_populates="piros")

class TagBase(SQLModel):
    title: str
    description: Optional[str] = None
    owner_id: int

class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    piros: List[Piro] = Relationship(back_populates="tags", link_model=PiroTagLink)
    owner: "User" = Relationship(back_populates="tags")

class UserBase(SQLModel):
    email: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tags: List[Tag] = Relationship(back_populates="owner")
    piros: List[Piro] = Relationship(back_populates="owner")

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

# Function to populate the database with test data
def populate_db(engine):
    with Session(engine) as session:
        # # Create test users
        # user1 = User(email="user1@example.com", firstname="User", lastname="One")
        # user2 = User(email="user2@example.com", firstname="User", lastname="Two")
        # session.add(user1)
        # session.add(user2)
        # session.commit()
        # session.refresh(user1)
        # session.refresh(user2)

        # # Create test tags
        # tag1 = Tag(title="Tag1", description="Description for Tag1", owner_id=user1.id)
        # tag2 = Tag(title="Tag2", description="Description for Tag2", owner_id=user2.id)
        # session.add(tag1)
        # session.add(tag2)
        # session.commit()
        # session.refresh(tag1)
        # session.refresh(tag2)

        # Create test piros
        statement = select(User).where(User.id == 1)
        results = session.exec(statement)
        user1 = results.one()
        statement = select(User).where(User.id == 2)
        results = session.exec(statement)
        user2 = results.one()
        statement = select(Tag).where(Tag.id == 1)
        results = session.exec(statement)
        tag1 = results.one()
        statement = select(Tag).where(Tag.id == 2)
        results = session.exec(statement)
        tag2 = results.one()
        piro1 = Piro(title="Piro1", description="Description for Piro1", s3urltovideo="http://s3.com/video1", imagename="image1.jpg", location="Location1", created="2021-01-01", owner_id=user1.id, tags=[tag1])
        piro2 = Piro(title="Piro2", description="Description for Piro2", s3urltovideo="http://s3.com/video2", imagename="image2.jpg", location="Location2", created="2021-02-01", owner_id=user2.id, tags=[tag2])
        session.add(piro1)
        session.add(piro2)
        session.commit()
        session.refresh(piro1)
        session.refresh(piro2)

        # Associate piros with tags
        # tag1.piros.append(piro1)
        # tag2.piros.append(piro2)
        # session.commit()

if __name__ == "__main__":
# Database setup
    create_db_and_tables(engine)
    populate_db(engine)
