from typing import Optional
from datetime import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so

from sqlalchemy import Unicode, UnicodeText, ForeignKey
from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from app import db

class Account(db.Model):
    __tablename__ = "Account"
    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(Unicode(30),nullable=False,unique=True)
    email: Mapped[str] = mapped_column(String(30),nullable=False,unique=True)
    hash_passwd: Mapped[str] = mapped_column(Text)
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='author', cascade = "all, delete-orphan", lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.nickname)



class Comment(db.Model):
    __tablename__ = "Comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('Account.id'), nullable=False)
    text: Mapped[str] = mapped_column(UnicodeText)
    time: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    tag: Mapped[str] = mapped_column(String(50), nullable=False)
    author: Mapped['Account'] = relationship('Account', back_populates='comments')

class Utilities(db.Model):
    __tablename__ = 'Utilities'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Unicode(100), nullable=False)
    sub_text: Mapped[str] = mapped_column(UnicodeText, nullable=True)
    command: Mapped[str] = mapped_column(String(30), nullable=False)
    top: Mapped[int] = mapped_column(Integer, nullable=False, default=False)
    url_photo: Mapped[str] = mapped_column(String(250))
    url_official: Mapped[str] = mapped_column(String(250))
    full_text: Mapped[str | None] = mapped_column(UnicodeText)

class Guides(db.Model):
    __tablename__ = "Guides"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Unicode(100), nullable=False)
    sub_text: Mapped[str] = mapped_column(UnicodeText)
    url_origin: Mapped[str] = mapped_column(String(250))
    full_text: Mapped[str] = mapped_column(UnicodeText)
    url_local: Mapped[str | None] = mapped_column(String(250), nullable=True)
