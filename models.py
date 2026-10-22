from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class BookModel(Base):
    __tablename__= "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    category = Column(String, nullable=False)
    price = Column(String, nullable=False)
    rating = Column(String, nullable=False)

