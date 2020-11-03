from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from config import config

database_uri = "mysql+mysqldb://{username}:{password}@{hostname}/{database}".format(
	username=config['mysql']['username'],
	password=config['mysql']['password'],
	hostname=config['mysql']['hostname'],
	database=config['mysql']['database']
)

engine = create_engine(database_uri)

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
