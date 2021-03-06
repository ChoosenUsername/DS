import hazelcast
import time

from hazelcast.util import validate_serializer


def pessimistic_blocking():
    client = hazelcast.HazelcastClient()
    map = client.get_map("my-distributed-map").blocking()

    key = 1
    map.put_if_absent(key,0)
    for i in range(100):
        print('i: ', i)
        map.lock(key)
        
        value = map.get(key)
        print(value)
        time.sleep(0.5)
        value += 1
        map.put(key, value)
        map.unlock(key)
    print('total', client.get_map("my-distributed-map").get(key).result())

if __name__ == "__main__":
    pessimistic_blocking()
