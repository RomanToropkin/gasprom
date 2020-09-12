from kafka import KafkaConsumer, KafkaProducer
from kafka import TopicPartition

consumer = KafkaConsumer(bootstrap_servers=['gpbtask.fun:9092'], consumer_timeout_ms=1000)
consumer.assign([TopicPartition('input1',0)])

for msg in consumer:
    print(msg.value)

consumer.close()