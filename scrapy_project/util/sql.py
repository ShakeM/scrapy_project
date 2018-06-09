from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.dialects.mysql import LONGTEXT
import arrow


class Database():
    Base = declarative_base()
    engine = create_engine('mysql+pymysql://root:56304931a@192.168.31.138:3306/stock?charset=utf8')
    DBSession = sessionmaker(bind=engine)

    def session(self):
        s = self.DBSession()
        return s

    def create_all(self):
        self.Base.metadata.create_all(self.engine)

    def drop_all(self):
        self.Base.metadata.drop_all(self.engine)


db = Database()


class Stock(db.Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    code = Column(String(20), nullable=False)
    symbol = Column(String(20), nullable=False)
    extra = Column(String(255), nullable=False)


class Index(db.Base):
    __tablename__ = 'index'
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(50), nullable=False)
    pc = Column(LONGTEXT, nullable=False)
    wise = Column(LONGTEXT, nullable=False)
    begin = Column(String(50), nullable=False)
    update_time = Column(String(50), nullable=False)


db.create_all()
# db.drop_all()

session = db.session()

for i in range(10):
    session.add(Index(word=str(i), pc='a', wise='a', begin='a',update_time='a'))

session.commit()
session.close()

# stock = {'code':"000001", 'name':"上证指数", 'symbol':"SH000001", 'extra':'["上证", "A股"]'}
#
# session = db.session()
# print(session.query(Stock).filter_by(**stock).all()[0].code)

# session = Database().session()
# words = session.query(Stock).all()
# print(words[1].code)
