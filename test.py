import json
import datetime

from geopy.distance import geodesic

from kafka import KafkaConsumer
from kafka import TopicPartition

LAST_DATA = 400

consumer = KafkaConsumer(auto_offset_reset='latest', enable_auto_commit=False,
                         bootstrap_servers=['gpbtask.fun:9092'], consumer_timeout_ms=1000, api_version=(0, 10, 1),
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


def mean(arr):
    sum = 0
    for x in arr:
        sum += x[5]
    return sum / LAST_DATA



for val in consumer:
    fl = 30
    val = val.value
    client_id = val['client_id']
    time = val['time']
   
    if client_id in clients:
        clients[client_id].append(list(val.values()))
    else:
        clients[client_id] = [list(val.values())]
    # if (fl==client_id):
    if len(clients[client_id]) == LAST_DATA:
        time1 = clients[client_id][0][1]
        time2 = clients[client_id][-1][1]
        lat1 = clients[client_id][0][2]
        lon1 = clients[client_id][0][3]
        lat2 = clients[client_id][-1][2]
        lon2 = clients[client_id][-1][3]
        print(f'дата 1: {time1}')
        print(f'дата 2: {time2}')
        if (time1[12] == ':'):
            time1 = datetime.datetime(int(time1[6:10]), int(time1[3:5]), int(time1[0:2]), int(time1[11:12]), int(time1[14:15]), 0)
        else:
            time1 = datetime.datetime(int(time1[6:10]), int(time1[3:5]), int(time1[0:2]), int(time1[11:13]), int(time1[14:16]), 0)
        if (time2[12] == ':'):
            time2 = datetime.datetime(int(time2[6:10]), int(time2[3:5]), int(time2[0:2]), int(time2[11:12]), int(time2[14:15]), 0)
        else:
            time2 = datetime.datetime(int(time2[6:10]), int(time2[3:5]), int(time2[0:2]), int(time2[11:13]), int(time2[14:16]), 0)
        print (time2-time1)
        print(f'первоначальная точка: {lat1, lon1}')
        print(f'конечная точка: {lat2, lon2}')
        print(
            f'пройденное расстрояние: {geodesic((lat1, lon1),(lat2, lon2)).meters} метров ')
        
        speed = geodesic((lat1, lon1),(lat2, lon2)).meters
        speed/=(time2.timestamp() - time1.timestamp())
        speed*=3.6
        print(f'средняя скорость при неадекватных значениях: {speed}')
        print(f'средняя скорость: {mean(clients[client_id])}')
            
        
        print(f'клиент: {client_id}')
        # if (mean(clients[client_id])>160):
            
            # for i in clients[client_id]:
            #     print(i)
        
        print('---------------------------------///////////////////////---------------------------------')
        del clients[client_id]



consumer.close()