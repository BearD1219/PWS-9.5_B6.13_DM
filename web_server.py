from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request
import albums_db
from albums_db import Albums

# GET - запросы
@route("/albums/<artist>")
def show_albums(artist):
    ''' Вывод кол-ва и название альбомов переданного артиста '''
    albums_dict = albums_db.get_albums(artist)
    if not albums_dict["albums"]:
       result =  HTTPError(404, f"Альбомы {artist}, не найдены!")    
    else:
        count = f"Количество альбомов {artist}: {albums_dict['count']}<br><br>"
        result = count + albums_dict["albums"]
    return result

# POST - запросы
@route("/albums", method="POST")
def add_albums():
    ''' Создает и сохраняет новый экземпляр класс Albums, если он уникальный '''
    # Пример POST- запроса:
# http -f POST localhost:8080/albums artist=Queen album=Jazz genre="Art rock" year=1976
    new_album = Albums(
        artist=request.forms.get("artist"),
        album=request.forms.get("album"),
        genre=request.forms.get("genre"),
        year=request.forms.get("year"),
    )
    try:
        int(new_album.year)
    except ValueError:
        print("Неверное значение параметра year")
        return "Неверное значение параметра year"
    unique_data = albums_db.valid_data(new_album.artist, new_album.album)
    if unique_data:
        print("Данный альбом уже добавлен")
        return HTTPError(409, "Данный альбом уже добавлен")
    else:
        albums_db.save_data(new_album)
        return "SAVE"

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)