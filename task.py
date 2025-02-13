      - name: Create Scripts
        run: |
          # 创建 task.py
          cat > task.py << 'EOL'
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
import argparse

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
    engine = create_engine(args.con, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    task = session.query(Task).filter(Task.status == "draft").first()
    if task:
        task.status = "published"
        session.commit()
        print(task.url)
    session.close()

def delete_task():
    engine = create_engine(args.con, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    keyword = "##" + args.name
    task = session.query(Task).filter(Task.url.like(f"%{keyword}")).first()
    if task:
        session.delete(task)
        session.commit()
    session.close()

if __name__ == "__main__":
    if args.opt == "query":
        find_one_and_update()
    elif args.opt == "delete":
        delete_task()
EOL

          # 创建 process_links.py
          cat > process_links.py << 'EOL'
import re
import sys

def process_links(input_links):
    # 删除指定的前缀
    cleaned_links = re.sub(r'https://pikpak\d\.sanxianianzi\d*\.ggff\.net/', '', input_links)
    # 分割链接并过滤掉空行
    links = [link.strip() for link in cleaned_links.split('https://vod-jo-') if link.strip()]
    # 添加前缀并准备输出
    formatted_links = [f'https://vod-jo-{link}' for link in links]
    return formatted_links

def main():
    if len(sys.argv) != 2:
        print("Usage: python process_links.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            input_links = file.read()
        formatted_links = process_links(input_links)
        with open('urls.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(formatted_links))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOL
