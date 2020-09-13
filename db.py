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

    def create_event(self, id_client, id_station_type, date, lat, lon,dist,speed):
        with self._connection.cursor() as cursor:
            sql = "INSERT INTO events (id_client, id_station_type, date, lat, lon,dist,speed) VALUE (%s,%s,%s,%s,%s,%s,%s);"
            cursor.execute(sql, (id_client, id_station_type, date, lat, lon,dist,speed))

            self._connection.commit()

    def get_last_event_by_client(self, id_client, id_station_type):
        with self._connection.cursor() as cursor:
            sql = "SELECT * FROM events WHERE id_client = %s AND id_station_type = %s ORDER BY date DESC limit 1;"
            cursor.execute(sql, (id_client, id_station_type))
            return cursor.fetchone()
