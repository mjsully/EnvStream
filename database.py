# from dotenv import load_dotenv

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, UniqueConstraint, create_engine, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
import os
from neologger import NeoLogger

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import IntegrityError

# def to_type(self, type, value):

#         if type == "STRING":
#             return str(value)
#         elif type == "INTEGER":
#             return int(value):
#         elif type == "FLOAT":
#             return float(value):
#         elif type == "BOOLEAN":
#             return bool(value)
#         else:
#             return str(value) 



# def from_type(self, type):

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
    type = Column(Integer)

    # def to_dict(self):

    #     return {
    #         column for column in self.__columns__
    #     }

class Handler:

    def __init__(self, application):

        self.logger = NeoLogger("Handler")
        self.application = application
        self.db_string = None

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

    def __type_enum__(self, enum, value):

        if enum == 0:
            return str(value)
        elif enum == 1:
            return int(value)
        elif enum == 2:
            return float(value)
        elif enum == 3:
            return bool(value)
        else:
            return None

    def __get_engine_session__(self):

        engine = create_engine(self.db_string)
        session = Session(bind=engine)
        return engine, session
    
    def __create_tables__(self):

        self.logger.log_this("Attempting to create tables")
        try:
            engine, _ = self.__get_engine_session__()
            Base.metadata.create_all(engine)
            self.logger.log_this_success("Created tables")
        except Exception as ex:
            self.logger.log_this_error(f"{type(ex)}: {ex}")

    def __set__(self, key, value, type):
        
        value = self.__type_enum__(type, value)
        setattr(self, key, value)

    def __get__(self, key):
        
        getattr(self, key, None)

    def __load_variables__(self):

        _, session = self.__get_engine_session__()
        results = session.query(
            ConfigurationVariables
        ).filter_by(
            application=self.application
        ).all()
        
        for value in results:
            self.__set__(value.name, value.value, value.type)

    def set_variable(self, key, value):

        print(vars(self))
        _, session = self.__get_engine_session__()

        variable = ConfigurationVariables(
            application=self.application,
            name=key,
            value=value,
            type=0
        )

        session.add(variable)
        session.commit()
        session.close()

        self.__load_variables__()

        # TODO: Implement set function
        pass

    def get_variables(self):

        variables = vars(self)
        # variables.pop("logger")
        # variables.pop("application")
        # variables.pop("db_string")

        return variables

    def get_variable(self, key):

        return self.__get__(key)

    def refresh(self):

        self.__load_variables__()