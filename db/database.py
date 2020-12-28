import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, select, insert, and_, update, delete
load_dotenv()

engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
connection = engine.connect()
metadata = MetaData()
Client = Table('client', metadata,
                  autoload=True, autoload_with=engine,extend_existing=True)
User = Table('user', metadata,
                  autoload=True, autoload_with=engine,extend_existing=True)