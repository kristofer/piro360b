from sqlalchemy import Column, String, Integer, ForeignKey, Table, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Association table for many-to-many relationship between Tag and Piro
tag_piro_association = Table('tag_piro', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id')),
    Column('piro_id', Integer, ForeignKey('piro.id'))
)

class Piro(Base):
    __tablename__ = 'piro'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    s3urltovideo = Column(String)
    imagename = Column(String)
    location = Column(String)
    created = Column(Date)
    owner_id = Column(Integer, ForeignKey('user.id'))
    
    owner = relationship("User", back_populates="piros")
    tags = relationship("Tag", secondary=tag_piro_association, back_populates="piros")

class Tag(Base):
    __tablename__ = 'tag'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship("User", back_populates="tags")
    piros = relationship("Piro", secondary=tag_piro_association, back_populates="tags")

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    email = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    
    tags = relationship("Tag", back_populates="owner")
    piros = relationship("Piro", back_populates="owner")

# p: create a function which starts using a sqlite3 database for this schema

def start_sqlite_db(db_path):
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

    # Example usage
    # session = start_sqlite_db('/path/to/your/database.db')

# generate some User data for this database
def create_user(session):
    user = User(email="eat@joes.com", firstname="Joe", lastname="Smith")
    session.add(user)
    session.commit()
    return user

# generate some Tag data for this database
def create_tag(session):
    tag = Tag(title="Tag1", description="This is tag 1")
    session.add(tag)
    session.commit()
    return tag

# generate some Piro data for this database
def create_piro(session):
    piro = Piro(title="Piro1", description="This is piro 1", s3urltovideo="http://s3.com/video",
                imagename="image.jpg", location="New York", created="2021-01-01")
    session.add(piro)
    session.commit()
    return piro
