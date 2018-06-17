from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine, Integer, MetaData
from sqlalchemy.dialects.mysql import LONGTEXT
import arrow


class Database:
    Base = declarative_base()

    def __init__(self, uri):
        self.engine = create_engine(uri)
        self.DBSession = sessionmaker(bind=self.engine)

    def session(self):
        s = self.DBSession()
        return s

    def create_all(self):
        self.Base.metadata.create_all(self.engine)

    def drop_all(self):
        self.Base.metadata.drop_all(self.engine)

    @property
    def tables(self):
        meta = MetaData()
        meta.reflect(bind=self.engine)
        keys = [key for key in meta.tables]
        return keys


db = Database('mysql+pymysql://root:56304931a@192.168.31.138:3306/stock?charset=utf8')


class Stock(db.Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    code = Column(String(20), nullable=False)
    symbol = Column(String(20), nullable=False)
    extra = Column(String(255), nullable=False)


from sqlalchemy.exc import InvalidRequestError


def update_tables(db):
    session = db.session()
    names = [name[0] for name in session.query(Stock.name).all()]
    codes = [code[0] for code in session.query(Stock.code).all()]
    extra = []
    for e in session.query(Stock.extra).all():
        extra += eval(e[0])

    all_tables = names + extra + codes

    for table in all_tables:
        name = str(table)
        try:
            type(name, (db.Base,), dict(__tablename__=name,
                                        id=Column(Integer, primary_key=True, autoincrement=True),
                                        period=Column(String(50), unique=True, nullable=False),
                                        word=Column(String(50), default=name),
                                        pc=Column(String(50), nullable=False),
                                        wise=Column(String(50), nullable=False),
                                        all=Column(String(50), nullable=False),
                                        update_time=Column(String(50), nullable=False)
                                        ))
        except InvalidRequestError as err:
            pass

    db.create_all()


# update_tables(db)
# db.drop_all()

# session = db.session()

# for i in range(10):
#     session.add(Index(word=str(i), pc='a', wise='a', begin='a', update_time='a'))

# session.commit()
# session.close()

# stock = {'code':"000001", 'name':"上证指数", 'symbol':"SH000001", 'extra':'["上证", "A股"]'}
#
# session = db.session()
# print(session.query(Stock).filter_by(**stock).all()[0].code)

# session = Database().session()
# words = session.query(Stock).all()
# print(words[1].code)
