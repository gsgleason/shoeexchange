from db import engine
from models import Base

def initdb():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

