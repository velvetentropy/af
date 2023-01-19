from datetime import datetime
from sqlalchemy import Column, func, Date, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import VARCHAR, TIMESTAMP, INTEGER
from metadata_db_constants import Base
from schema.user import User
from util.dict_util import to_dict


class UserRecord(Base):
    __tablename__ = "user"

    user_id = Column(INTEGER, primary_key=True)
    af_id = Column(INTEGER, ForeignKey("af.af_id"), unique=True, nullable=False)
    first_name = Column(VARCHAR, nullable=False)
    last_name = Column(VARCHAR, nullable=False)
    user_name = Column(VARCHAR, nullable=False, unique=True)
    birth_date = Column(Date, nullable=False)
    created_at = Column(
        TIMESTAMP, nullable=False, server_default=func.current_timestamp()
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    __table_args__ = (UniqueConstraint("user_name"),)

    def __init__(
        self,
        first_name: str,
        last_name: str,
        user_name: str,
        birth_date: datetime,
        af_id: str,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.birth_date = birth_date.date()
        self.af_id = af_id

    def __repr__(self):
        return "<UserRecord(id={self.id!r})>".format(self=self)


def insert(session, user: User):
    session.add(UserRecord(**to_dict(user)))
