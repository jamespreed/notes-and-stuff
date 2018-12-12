from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship, validates, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from dateutil.parser import parse

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    dob = Column(Date)
    books = relationship('Book', backref='author') # backref creates 'author' field in Book

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    #author = relationship('Author', back_populates='name')

    
if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    
    a1 = Author(name='J.R.R. Tolkien', dob=parse('3 Jan 1892'))
    a2 = Author(name='George R.R. Martin', dob=parse('20 Sep 1948'))
    a3 = Author(name='Patrick Rothfuss', dob=parse('June 6, 1973'))
    
    session.add_all([a1, a2, a3])
    session.commit()
    
    # b1 = Book(title='The Hobbit', 
        # author_id=(
            # session.query(Author)
                   # .filter(Author.name.like('j.r.r tolkien'))
                   # .first()
                   # .id
        # )
    b1 = Book(title='The Hobbit', author_id=a1.id)
    b2 = Book(title='Game of Thrones', author_id=a2.id)
    b3 = Book(title='A Clash of Kings', author_id=a2.id)
    b4 = Book(title='A Storm of Swords', author_id=a2.id)
    b5 = Book(title='The Name of the Wind', author_id=a3.id)
    
    session.add_all([b1, b2, b3, b4, b5])
    session.commit()
