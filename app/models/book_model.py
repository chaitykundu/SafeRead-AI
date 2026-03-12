from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class BookScan(Base):

    __tablename__ = "book_scans"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String)
    title = Column(String)
    author = Column(String)

    violence = Column(String)
    profanity = Column(String)
    sexual_content = Column(String)

    summary = Column(Text)