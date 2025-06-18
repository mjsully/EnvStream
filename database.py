# from dotenv import load_dotenv

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, UniqueConstraint, create_engine, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
import os
from neologger import NeoLogger

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import IntegrityError

class VariableTypes:

    string = 0
    integer = 1
    boolean = 2

class Base(DeclarativeBase):
    pass

class ConfigurationVariables(Base):

    __tablename__ = "configuration_variables"

    id = Column(Integer, primary_key=True)
    application = Column(String, unique=True)
    name = Column(String)
    value = Column(String)
    type = Column(Integer)

    # def to_dict(self):

    #     return {
    #         column for column in self.__columns__
    #     }

class Handler:

    def __init__(self):

        load_dotenv()
        self.logger = NeoLogger("Handler")
        self.db_string = self.database_string()

    def database_string(self):

        postgres_username = os.getenv("POSTGRES_USERNAME", None)
        postgres_password = os.getenv("POSTGRES_PASSWORD", None)
        postgres_database = os.getenv("POSTGRES_DATABASE", None)
        postgres_host = os.getenv("POSTGRES_HOST", None)
        postgres_port = os.getenv("POSTGRES_PORT", None)
        database_string = f"postgresql+psycopg2://{postgres_username}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_database}"
        return database_string

    def get_engine_session(self):

        engine = create_engine(self.db_string)
        session = Session(bind=engine)
        return engine, session
    
    def create_tables(self):

        self.logger.log_this("Attempting to create tables")
        try:
            engine, _ = self.get_engine_session()
            Base.metadata.create_all(engine)
            self.logger.log_this_success("Created tables")
        except Exception as ex:
            self.logger.log_this_error(f"{type(ex)}: {ex}")