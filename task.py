import json
import sys
import argparse
import os

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.sql import func

parser = argparse.ArgumentParser(description="操作数据库")
parser.add_argument("--opt", help="操作", default="query")
parser.add_argument("--con", help="数据库链接地址", default="")
parser.add_argument("--name", help="文件名称", default="")

args = parser.parse_args()

engine = create_engine(
    args.con,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
Base = declarative_base()

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, unique=True, primary_key=True)
    status = Column(String, index=True)
    sort = Column(Integer)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    url = Column(String)

def find_one_and_update():
    with Session(engine) as session:
        task = db.query(Task).filter(Task.status == "draft").first()
        if task is None:
            print("没有找到待处理的任务")
            sys.exit(1)
        task.status = "published"
        db.commit()
        db.refresh(task)
        return task

def delete_task():
    with Session(engine) as session:
        keyword = "##" + args.name
        task = db.query(Task).filter(Task.url.like(f"%{keyword}")).first()
        if task is not None:
            db.delete(task)
            db.commit()

if __name__ == "__main__":
    if args.opt == "query":
        task = find_one_and_update()
        if task is not None:
            print(task.url)
        sys.exit(0)
    if args.opt == "delete":
        delete_task()
