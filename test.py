import json

import datetime
from geopy.distance import geodesic

from kafka import KafkaConsumer
from kafka import TopicPartition

consumer = KafkaConsumer(auto_offset_reset='latest', enable_auto_commit=False,
                         bootstrap_servers=['gpbtask.fun:9092'], consumer_timeout_ms=2000, api_version=(0, 10, 1),
                         value_deserializer=lambda m: json.loads(m.decode('ascii')))
partition = TopicPartition('input1', 0)
consumer.assign([partition])

clients = {}

patrols = [(55.554771, 37.924931), (60.765833, 28.808552), (55.798510, 37.534730),(55.848817, 36.805567),
           (53.041525, 158.637171)]

offices = [(55.558834, 37.815781),(55.900693, 37.478917),(56.359825, 37.542558),(53.064992, 158.619518),
           (55.847763, 37.636684)]

banks = [(55.728849, 37.620321),(56.342179, 37.523720),(56.007639, 37.484526),(55.782977, 37.640659),
         (53.019530, 158.647842),(55.630446, 37.658377),(55.633323, 37.650055),(55.909247, 37.590461)]

events = {}

first_time = datetime.datetime.now().timestamp()

def mean(arr):
    sum = 0
    for x in arr:
        sum += x[5]
    return sum / len(arr)


for val in consumer:
    val = list(val.value.values())
    lat = val[2]
    lon = val[3]
    time1 = val[1]
    if (time1[12] == ':'):
        text_time = time1[11:12]
        time1 = datetime.datetime(int(time1[6:10]), int(time1[3:5]), int(time1[0:2]), int(time1[11:12]),
                                  int(time1[13:15]), 0).timestamp()
    else:
        text_time = time1[11:13]
        time1 = datetime.datetime(int(time1[6:10]), int(time1[3:5]), int(time1[0:2]), int(time1[11:13]),
                                  int(time1[14:16]), 0).timestamp()
    if abs(time1 - first_time) < 300:
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
            print(f'средняя скорость при неадекватных значениях: {speed}')
            print(f'средняя скорость: {mean(clients[client_id])}')
            i = 1
            if (int(text_time) >= 8 and int(text_time) <= 20):
                if speed >= 20 and speed <= 110:
                    needed_dist = 1500
                else:
                    needed_dist = 500
                for pat in patrols:
                    dist = geodesic((lat2, lon2), (pat)).meters
                    if dist <= needed_dist:
                        print(f'Отработало событие! {val}, координаты колонки: {pat}, расстрояние: {dist}')
                        if client_id in events:
                            for client in events:
                                for event in events[client]:
                                    if 1 == event['id_station'] and time1 - event['time'] >= 86400:
                                        events[client_id].append({'time':time1,'id_station':1})
                                    elif 1 != event['id_station']:
                                        events[client_id].append({'time': time1, 'id_station': 1})
                        else:
                            events[client_id] = [{'time':time1,'id_station':1}]
                    print(f'Расстояние до колонки {i} - {dist} метров')
                    i += 1
                print()
                for pat in offices:
                    dist = geodesic((lat2, lon2), (pat)).meters
                    if dist <= needed_dist:
                        print(f'Отработало событие! {val}, координаты офиса: {pat}, расстрояние: {dist}')
                        if client_id in events:
                            for client in events:
                                for event in events[client]:
                                    if 2 == event['id_station'] and time1 - event['time'] >= 86400:
                                        events[client_id].append({'time': time1, 'id_station': 2})
                                    elif 2 != event['id_station']:
                                        events[client_id].append({'time': time1, 'id_station': 2})
                        else:
                            events[client_id] = [{'time': time1, 'id_station': 2}]
                    print(f'Расстояние до офиса {i} - {dist} метров')
                    i += 1
                print()
                for pat in banks:
                    dist = geodesic((lat2, lon2), (pat)).meters
                    if dist <= needed_dist:
                        print(f'Отработало событие! {val}, координаты банка: {pat}, расстрояние: {dist}')
                        if client_id in events:
                            for client in events:
                                for event in events[client]:
                                    if 3 == event['id_station'] and time1 - event['time'] >= 86400:
                                        events[client_id].append({'time': time1, 'id_station': 3})
                                    elif 3 != event['id_station']:
                                        events[client_id].append({'time': time1, 'id_station': 3})
                        else:
                            events[client_id] = [{'time': time1, 'id_station': 3}]
                    print(f'Расстояние до банка {i} - {dist} метров')
                    i += 1
            print('---------------------------------///////////////////////---------------------------------')
        print(events)
        first_time = time1
        clients = {}

consumer.close()