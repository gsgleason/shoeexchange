from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime

class Listing(Base):

    __tablename__ = "listings"

    id = Column(Integer, primary_key=True)
    submission_id = Column(String(256))
    title = Column(String(256))
    permalink = Column(String(256))
    flair_text = Column(String(16))
    url = Column(String(256))
    redditor = Column(String(64))
    brand = Column(String(64))
    model = Column(String(64))
    size = Column(String(64))
    width = Column(String(64))
    last = Column(String(64))
    upper = Column(String(64))
    sole = Column(String(64))
    condition = Column(String(256))
    images = Column(String(256))
    notes = Column(String(1024))
    price = Column(String(256))
    country = Column(String(256))
    thumbnail_url = Column(String(256))
    created_utc = Column(DateTime)
    updated_utc = Column(DateTime, nullable=False, default=datetime.utcnow())

