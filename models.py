from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.ext.declarative import declarative_base
from collections.abc import Iterator

# user와 model의 many to many relation을 위함
user_group_association = Table(
    'user_group_association',
    Base.metadata,
    Column('user_id', String, ForeignKey('user.id')),
    Column('group_invitationCode', String, ForeignKey('group.invitationCode'))
)

# 모델 정의


class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    pw = Column(String, nullable=False)
    email = Column(String, nullable=True)
    birthDay = Column(String, nullable=True)
    sheduleImg = image_attachment('UserImg', back_populates="user")
    groups = relationship(
        'Group', secondary=user_group_association, back_populates='users'
    )



class Group(Base):
    __tablename__ = "group"

    name = Column(String, nullable=False)
    invitationCode = Column(String, nullable=False, primary_key=True)
    pw = Column(String, nullable=False)
    users = relationship(
        'User', secondary=user_group_association, back_populates='groups')


class UserImg(Base, Image):
    __tablename__ = 'userImg'
    userId = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user = relationship('User', back_populates="sheduleImg")
