from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
import argparse
import sys
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 参数解析
parser = argparse.ArgumentParser(description="操作数据库")
parser.add_argument("--opt", help="操作", default="query")
parser.add_argument("--con", help="数据库链接地址", default="")
parser.add_argument("--name", help="文件名称", default="")

args = parser.parse_args()

Base = declarative_base()

class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, unique=True, primary_key=True)
    status = Column(String, index=True)
    sort = Column(Integer)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    url = Column(String)

def find_one_and_update():
    """查找并更新一个任务"""
    try:
        engine = create_engine(args.con, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # 查询任务
        task = session.query(Task).filter(Task.status == "draft").order_by(Task.sort.desc()).first()
        if task and task.url:
            task.status = "published"
            session.commit()
            print(task.url)  # 直接打印到标准输出
            logger.info(f"成功更新任务: {task.id}")
            return True
        else:
            logger.warning("没有找到待处理的任务")
            return True  # 返回 True 以避免工作流失败
    except Exception as e:
        logger.error(f"查询或更新失败: {str(e)}")
        return False
    finally:
        if 'session' in locals():
            session.close()

def delete_task():
    """删除指定的任务"""
    try:
        engine = create_engine(args.con, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        keyword = "##" + args.name
        task = session.query(Task).filter(Task.url.like(f"%{keyword}")).first()
        if task:
            session.delete(task)
            session.commit()
            logger.info(f"成功删除任务: {task.id}")
        else:
            logger.warning(f"未找到要删除的任务: {keyword}")
    except Exception as e:
        logger.error(f"删除任务失败: {str(e)}")
        return False
    finally:
        if 'session' in locals():
            session.close()
    return True

if __name__ == "__main__":
    try:
        if args.opt == "query":
            if not find_one_and_update():
                sys.exit(1)
        elif args.opt == "delete":
            if not delete_task():
                sys.exit(1)
        else:
            logger.error(f"未知的操作类型: {args.opt}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        sys.exit(1)
