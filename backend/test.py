import json

import datetime
from geopy.distance import geodesic

from kafka import KafkaConsumer
from kafka import TopicPartition

from backend.db import DB

BOOTSTRAP_SERVER = 'gpbtask.fun:9092'
CAR_DISTANCE = 4000
DAY_START = 8
DAY_END = 20
MIN_SPEED = 30
MAX_SPEED = 100
NULL_TIME_SIZE = 10000000000
TIME_DIF = 66400
TOPIC = 'input10'
WALKER_DISTANCE = 1600
WINDOW_SIZE = 300

consumer = KafkaConsumer(auto_offset_reset='latest', enable_auto_commit=False,
                         bootstrap_servers=[BOOTSTRAP_SERVER], consumer_timeout_ms=2000, api_version=(0, 10, 1),
                         value_deserializer=lambda m: json.loads(m.decode('ascii')))
partition = TopicPartition(TOPIC, 0)
consumer.assign([partition])

clients = {}
db = DB()

patrols = db.get_station(1)
offices = db.get_station(2)
banks = db.get_station(3)

first_time = datetime.datetime.now().timestamp()


def mean(arr):
    speed_sum = 0
    for x in arr:
        speed_sum += x[5]
    return speed_sum / len(arr)


for val in consumer:
    val = list(val.value.values())
    lat = val[2]
    lon = val[3]
    time1 = val[1]
    if time1[12] == ':':
        text_time = time1[11:12]
        time1 = datetime.datetime(int(time1[6:10]), int(time1[3:5]), int(time1[0:2]), int(time1[11:12]),
                                  int(time1[13:15]), 0).timestamp()
    else:
        text_time = time1[11:13]
        time1 = datetime.datetime(int(time1[6:10]), int(time1[3:5]), int(time1[0:2]), int(time1[11:13]),
                                  int(time1[14:16]), 0).timestamp()
    if abs(time1 - first_time) < WINDOW_SIZE:
        if val[0] in clients:
            clients[val[0]].append(val)
        else:
            clients[val[0]] = [val]
    else:
        for client_id in clients:
            print(clients[client_id])
            lat1 = clients[client_id][0][2]
            lon1 = clients[client_id][0][3]
            lat2 = clients[client_id][-1][2]
            lon2 = clients[client_id][-1][3]
            print(f'первоначальная точка: {lat1, lon1}')
            print(f'конечная точка: {lat2, lon2}')
            print(
                f'пройденное расстрояние: {geodesic((lat1, lon1), (lat2, lon2)).meters} метров ')
            speed = geodesic((lat1, lon1), (lat2, lon2)).meters
            speed /= (time1 - first_time)
            speed *= 3.6
            print(f'средняя скорость: {mean(clients[client_id])}')
            if MIN_SPEED <= speed <= MAX_SPEED:
                needed_dist = CAR_DISTANCE
            else:
                needed_dist = WALKER_DISTANCE
            for pat in patrols:
                dist = geodesic((lat2, lon2), (pat['latitude'], pat['longitude'])).meters
                if dist <= needed_dist and MIN_SPEED <= speed <= MAX_SPEED:
                    print(f'Сработал тригер. {val}, координаты колонки: {pat}, расстрояние: {dist}')
                    note = db.get_last_event_by_client(client_id, 1)
                    if note:
                        last_client_note = note['date']
                    else:
                        last_client_note = NULL_TIME_SIZE
                    note = db.get_earliest_event_by_client(client_id, 1)
                    if note:
                        early_client_note = note['date']
                    else:
                        early_client_note = NULL_TIME_SIZE
                    print(last_client_note)
                    print(early_client_note)
                    print(abs(time1 - last_client_note), abs(time1 - early_client_note))
                    if abs(time1 - last_client_note) >= TIME_DIF \
                            and abs(time1 - early_client_note) >= TIME_DIF:
                        print('Добавили в базу событие!')
                        db.create_event(client_id, 1, time1, pat['latitude'], pat['longitude'], dist, speed)
                # print(f'Расстояние до колонки {i} - {dist} метров')
            # print()
            if DAY_START <= int(text_time) <= DAY_END:
                for pat in offices:
                    dist = geodesic((lat2, lon2), (pat['latitude'], pat['longitude'])).meters
                    if dist <= needed_dist:
                        print(f'Сработал тригер. {val}, координаты офиса: {pat}, расстрояние: {dist}')
                        note = db.get_last_event_by_client(client_id, 2)
                        if note:
                            last_client_note = note['date']
                        else:
                            last_client_note = NULL_TIME_SIZE
                        note = db.get_earliest_event_by_client(client_id, 2)
                        if note:
                            early_client_note = note['date']
                        else:
                            early_client_note = NULL_TIME_SIZE
                        print(last_client_note)
                        print(early_client_note)
                        print(abs(time1 - last_client_note), abs(time1 - early_client_note))
                        if abs(time1 - last_client_note) >= TIME_DIF \
                                and abs(time1 - early_client_note) >= TIME_DIF:
                            print('Добавили в базу событие!')
                            db.create_event(client_id, 2, time1, pat['latitude'], pat['longitude'], dist, speed)
                    # print(f'Расстояние до офиса {i} - {dist} метров')
                # print()
                for pat in banks:
                    dist = geodesic((lat2, lon2), (pat['latitude'], pat['longitude'])).meters
                    if dist <= needed_dist:
                        print(f'Сработал тригер. {val}, координаты банка: {pat}, расстрояние: {dist}')
                        note = db.get_last_event_by_client(client_id, 3)
                        if note:
                            last_client_note = note['date']
                        else:
                            last_client_note = NULL_TIME_SIZE
                        note = db.get_earliest_event_by_client(client_id, 3)
                        if note:
                            early_client_note = note['date']
                        else:
                            early_client_note = NULL_TIME_SIZE
                        print(last_client_note)
                        print(early_client_note)
                        print(abs(time1 - last_client_note), abs(time1 - early_client_note))
                        if abs(time1 - last_client_note) >= TIME_DIF \
                                and abs(time1 - early_client_note) >= TIME_DIF:
                            print('Добавили в базу событие!')
                            db.create_event(client_id, 3, time1, pat['latitude'], pat['longitude'], dist, speed)
                    # print(f'Расстояние до банка {i} - {dist} метров')
            print('---------------------------------///////////////////////---------------------------------')
        # print(events)
        first_time = time1
        clients = {}

consumer.close()
