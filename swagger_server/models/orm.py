from sqlalchemy import Column, DateTime, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import UniqueConstraint

Base = declarative_base()


class Userinfo(Base):
    __tablename__ = 'users'
    id = Column(String(20),nullable=True)
    dao_username = Column(String(100),primary_key=True)
    dao_password = Column(String(128))
    dao_lastname = Column(String(128))
    dao_firstname = Column(String(128))
    dao_email = Column(String(128))
    __table_args__ = (
            UniqueConstraint("id", "dao_username","dao_email"),

        )


def init_db(uri):
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session