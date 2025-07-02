# from dotenv import load_dotenv

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, UniqueConstraint, create_engine, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
import os
import json
from neologger import NeoLogger

from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import IntegrityError

class Base(DeclarativeBase):
    pass

class ConfigurationVariables(Base):

    __tablename__ = "configuration_variables"    
    __table_args__ = (
        UniqueConstraint("application", "name", name="configuration_variables_constraint_1"),
    )
    id = Column(Integer, primary_key=True)
    application = Column(String)
    name = Column(String)
    value = Column(String)
    type = Column(String)
    updated = Column(DateTime(timezone=True), server_default=func.now())

class EnvStream:

    def __init__(self, application, log_level="INFO"):

        self.logger = NeoLogger("Handler")
        self.application = application
        self.db_string = None
        self.__variables__ = {}
        self.log_level = log_level

    def setup_db(self, username, password, host, port, database):

        postgres_username = username
        postgres_password = password
        postgres_host = host
        postgres_port = port
        postgres_database = database
        database_string = f"postgresql+psycopg2://{postgres_username}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_database}"
        self.db_string = database_string
        self.__create_tables__()
        self.__load_variables__()

    def __type_enum__(self, value, type):

        if type == "str":
            return str(value)
        elif type == "int":
            return int(value)
        elif type == "float":
            return float(value)
        elif type == "bool":
            return value in ["true", 1]
        elif type == "dict":
            return json.loads(value)
        else:
            return None

    def __get_engine_session__(self):

        engine = create_engine(self.db_string)
        session = Session(bind=engine)
        return engine, session
    
    def __create_tables__(self):

        if self.log_level == "DEBUG":
            self.logger.log_this("Attempting to create tables")
        try:
            engine, _ = self.__get_engine_session__()
            Base.metadata.create_all(engine)
            if self.log_level == "DEBUG":
                self.logger.log_this_success("Created tables")
        except Exception as ex:
            self.logger.log_this_error(f"{type(ex)}: {ex}")

    def __set__(self, key, value, type):

        value = self.__type_enum__(value, type)
        setattr(self, key, value)
        self.__variables__[key] = value

    def __get__(self, key):
        
        getattr(self, key, None)

    def __load_variables__(self):

        _, session = self.__get_engine_session__()
        
        self.__variables__ = {}

        results = session.query(
            ConfigurationVariables
        ).filter_by(
            application=self.application
        ).all()
        
        for value in results:
            self.__set__(value.name, value.value, value.type)

    def set_variable(self, key, value):

        _, session = self.__get_engine_session__()

        self.__variables__[key] = value

        variable = ConfigurationVariables(
            application=self.application,
            name=key,
            value=value,
            type=type(value).__name__
        )

        try:
            session.add(variable)
            session.commit()
            if self.log_level == "DEBUG":
                self.logger.log_this_success(f"Added variable: {key}/{value}")
        except IntegrityError as e:
            session.rollback()
            config_var = session.execute(
                select(ConfigurationVariables)
                .where(ConfigurationVariables.name == key)
            ).scalar_one_or_none()
            config_var.value = value
            config_var.type = type(value).__name__
            config_var.updated = datetime.utcnow()
            session.commit()
            if self.log_level == "DEBUG":
                self.logger.log_this_success(f"Updated variable: {key}/{value}")
        session.close()

        self.__load_variables__()

    def get_variables(self):

        return self.__variables__

    def get_variable(self, key):

        return self.__get__(key)

    def remove_variable(self, key):

        _, session = self.__get_engine_session__()
        config_var = session.execute(
            select(ConfigurationVariables)
            .where(ConfigurationVariables.name == key)
        ).scalar_one_or_none()
        if config_var:
            session.delete(config_var)
            session.commit()
            if self.log_level == "DEBUG":
                self.logger.log_this_success(f"Removed variable: {key}")
        session.close()

        self.__load_variables__()

    def refresh(self):

        self.__load_variables__()