# encoding: utf-8

from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    studentid = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)


class Preuser(db.Model):
    __tablename__ = 'preuser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    studentid = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)


class Sample(db.Model):
    __tablename__ = 'sample'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.Text, nullable=False)
    # now()获取的是服务器第一次运行的时间
    # now就是每次创建一个模型的时候，都获取当前的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('sample'))


class Exp(db.Model):
    __tablename__ = 'exp'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    result = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sample = db.relationship('Sample', backref=db.backref('exp', order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('exp'))
