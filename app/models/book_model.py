from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON
from app.database import Base

class BookScan(Base):
    __tablename__ = "book_scans"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String, index=True)

    title = Column(String)
    author = Column(String)
    cover_image = Column(String)

    analysis = Column(JSON)   # NEW (store full AI result here)

    summary = Column(Text)