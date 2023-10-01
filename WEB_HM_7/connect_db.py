from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import database connection config
from config import db_user, db_password, db_host, db_port, db_name

# running docker container
# docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=12345 -d postgres

# db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()
