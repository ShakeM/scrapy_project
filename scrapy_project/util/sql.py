from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine, Integer


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


db.create_all()
# db.drop_all()

# session = db.session()
#
# session.add(Stock(code="000001", name="上证指数", symbol="SH000001", extra='["上证", "A股"]'))
# session.add(Stock(code="000300", name="沪深300", symbol="SH000300", extra='["399300"]'))
# session.add(Stock(code="399001", name="深证成指", symbol="SZ399001", extra='["深圳指数"]'))
# session.add(Stock(code="399005", name="中小板指", symbol="SZ399005", extra='["中小板指数"]'))
# session.add(Stock(code="399006", name="创业板指", symbol="SZ399006", extra='["创业板指数"]'))
#
# session.commit()
# session.close()

# stock = {'code':"000001", 'name':"上证指数", 'symbol':"SH000001", 'extra':'["上证", "A股"]'}
#
# session = db.session()
# print(session.query(Stock).filter_by(**stock).all()[0].code)
