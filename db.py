import pymysql.cursors


class DB:

    def __init__(self) -> None:
        super().__init__()
        self._connection = pymysql.connect(host='gasprom.creativityprojectcenter.ru',
                                          user='gasprom',
                                          db='gasprom',
                                          password='mMnks1pJptaARPHoN8Bi',
                                          cursorclass=pymysql.cursors.DictCursor)

    def get_station_types(self):
        with self._connection.cursor() as cursor:

            sql = "SELECT name FROM station_type WHERE deleted = 0;"
            cursor.execute(sql)
            return cursor.fetchall()