import hazelcast
import time

from hazelcast.util import validate_serializer

def no_blocking():
    client = hazelcast.HazelcastClient()
    map = client.get_map("my-distributed-map").blocking()
    key = 1
    map.put(key,0)
    for i in range(1000):
        if (i % 100 == 0): print('i: ', i)
        value = map.get(key)
        time.sleep(0.01)
        value += 1
        map.put(key, value)
    print('total', client.get_map("my-distributed-map").get(key).result())

if __name__ == "__main__":
    no_blocking()
