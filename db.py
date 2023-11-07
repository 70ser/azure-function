from datetime import datetime
from enum import Enum
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Enum as EnumColumn
from sqlalchemy import select
#from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from os import getenv

load_dotenv()

connection_string = f"mysql+mysqlconnector://{getenv('DATABASE_USERNAME')}:{getenv('DATABASE_PASSWORD')}@{getenv('DATABASE_HOST')}:3306/{getenv('DATABASE')}"

engine = create_engine(connection_string, echo=True)

class Strtype(Enum):
    plain = 1
    url = 2

class Base(DeclarativeBase):
    pass

class File(Base):
    __tablename__ = 'file_list'
    # unsigned datatype was not part of the SQL standard(SQL-2003)
    # so we have to from sqlalchemy.dialects.mysql import INTEGER ,then INTEGER(unsigned=True)
    # instead of from sqlalchemy import INTEGER, INTEGER(), which is omitted below
    # for now we just leave it here as we will never run out of 2147483647
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String(255)) # for plain string, it is the first 10 characters
    create_time: Mapped[datetime] = mapped_column(DateTime) #
    type: Mapped[Strtype] = mapped_column(EnumColumn(Strtype)) #
    value: Mapped[str] = mapped_column(String(4095)) # 
    expire_time: Mapped[datetime] = mapped_column(DateTime)
    

def select_file(length:int) -> list[File]:
    with Session(engine) as session:
        res = select(File).order_by(File.id.desc()).limit(length)
        return session.scalars(res).all()

def insert_file(file:File) -> None:
    file.create_time = datetime.now()
    file.expire_time = datetime.now()
    with Session(engine) as session:
        session.add(file)
        session.commit()

def delete_file(file:File) -> None:
    with Session(engine) as session:
        session.query(File).filter(File.id == file.id).delete()
        # session.delete(file)
        session.commit()

# with engine.connect() as connection:
#     result = connection.execute(text("show tables"))
#     print(result.all())
# with Session(engine) as session:
#     res = select(File).order_by(File.id.desc())
#     print(session.scalars(res).all()[0].name)