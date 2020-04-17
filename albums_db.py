import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Albums(Base):
    __tablename__ = "album"
    id = sa.Column(sa.INTEGER, primary_key = True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connection_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def get_albums(artist):
    ''' Ф-ция возвращает словарь с кол-вом и названием альбомов. '''
    albums_dict = {}
    session = connection_db()
    filter_data = session.query(Albums).filter(Albums.artist == artist).all()
    count = session.query(Albums).filter(Albums.artist == artist).count()
    albums = [album.album for album in filter_data]
    albums = "<br>".join(albums)
    albums_dict["count"] = str(count)
    albums_dict["albums"] = albums
    return albums_dict

def valid_data(artist, album):
    ''' Ф-ция проверки уникальности введенных данных (имя альбома и артиста). '''
    session = connection_db()
    filter_data = session.query(Albums).filter(Albums.artist == artist).filter(
        Albums.album == album).first()
    return filter_data

def save_data(data):
    ''' Ф-ция сохранения в Базу Данных. '''
    session = connection_db()
    session.add(data)
    session.commit()
    print("Данные сохранены")